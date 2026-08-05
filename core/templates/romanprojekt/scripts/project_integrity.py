#!/usr/bin/env python3
"""Versions- och integritetskontroll för Romanskaparens projektpaket.

Exempel:
  python scripts/project_integrity.py init . --slug min-roman
  python scripts/project_integrity.py verify .

  # Granska en äldre zip innan den packas upp eller ändras.
  python /tmp/project_integrity.py audit-legacy min-roman-gammal.zip \
      --output /tmp/min-roman-legacy-audit.json

  # Efter säker uppackning: kopiera den aktuella scriptversionen till projektet
  # och skapa den första revisionslåsta baslinjen.
  python scripts/project_integrity.py init . \
      --slug min-roman \
      --revision 1 \
      --zip-name min-roman-r0001-migrerad.zip \
      --source-zip-name min-roman-gammal.zip \
      --legacy-migration \
      --legacy-audit /tmp/min-roman-legacy-audit.json \
      --operation "Migrerade äldre projekt till revisionslåst format"

  python scripts/project_integrity.py commit . \
      --operation "Skapade kapitel 5" \
      --zip-name min-roman-r0002-kapitel-05.zip \
      --allow 'kapitel/kapitel-05.md' \
      --allow 'kapitelplan.md' \
      --allow 'projektstatus.md' \
      --allow 'arbetslogg.md' \
      --allow 'tidslinje.md' \
      --allow 'kontinuitetsanteckningar.md' \
      --allow 'kapitelnoteringar.md' \
      --allow 'project-index.md'
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

MANIFEST_NAME = "project-manifest.json"
REVISION_LOG = "revision-log.md"
IGNORED_PARTS = {".DS_Store", "__MACOSX", ".git"}
CANONICAL_CHAPTER_RE = re.compile(r"kapitel/kapitel-(\d{2,})\.md$")
CHAPTER_CANDIDATE_RE = re.compile(r"kapitel[-_ ]?(\d+)(.*)\.md$", re.IGNORECASE)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def should_track(relative: Path) -> bool:
    if relative.as_posix() == MANIFEST_NAME:
        return False
    if any(part in IGNORED_PARTS for part in relative.parts):
        return False
    return True


def inventory(root: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if not should_track(relative):
            continue
        result[relative.as_posix()] = {
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
    return result


def chapter_number(path: str) -> int | None:
    match = re.fullmatch(r"kapitel/kapitel-(\d{2,})\.md", path)
    return int(match.group(1)) if match else None


def chapter_summary(files: dict[str, dict[str, Any]]) -> dict[str, Any]:
    numbers: list[int] = []
    hashes: dict[str, str] = {}
    for path, info in files.items():
        number = chapter_number(path)
        if number is None:
            continue
        numbers.append(number)
        hashes[path] = str(info["sha256"])
    numbers.sort()
    missing: list[int] = []
    if numbers:
        present = set(numbers)
        missing = [number for number in range(numbers[0], numbers[-1] + 1) if number not in present]
    return {
        "count": len(numbers),
        "first": numbers[0] if numbers else None,
        "latest": numbers[-1] if numbers else None,
        "missing": missing,
        "hashes": hashes,
    }


def manifest_path(root: Path) -> Path:
    return root / MANIFEST_NAME


def load_manifest(root: Path) -> dict[str, Any]:
    path = manifest_path(root)
    if not path.exists():
        raise ValueError(f"Saknar {MANIFEST_NAME}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Ogiltig JSON i {MANIFEST_NAME}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{MANIFEST_NAME} måste innehålla ett JSON-objekt")
    return value


def save_manifest(root: Path, manifest: dict[str, Any]) -> None:
    manifest_path(root).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def validate_manifest_shape(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version": int,
        "project_id": str,
        "project_slug": str,
        "revision": int,
        "parent_revision": (int, type(None)),
        "created_at": str,
        "updated_at": str,
        "canonical_zip_name": str,
        "tracked_files": dict,
        "chapters": dict,
        "last_operation": dict,
    }
    for key, expected in required.items():
        if key not in manifest:
            errors.append(f"Manifestet saknar fältet {key}")
        elif not isinstance(manifest[key], expected):
            errors.append(f"Manifestfältet {key} har fel typ")
    if isinstance(manifest.get("revision"), int) and manifest["revision"] < 0:
        errors.append("Revision får inte vara negativ")
    if "migration" in manifest and not isinstance(manifest["migration"], (dict, type(None))):
        errors.append("Manifestfältet migration måste vara objekt eller null")
    return errors


def compare_inventory(
    expected: dict[str, dict[str, Any]], actual: dict[str, dict[str, Any]]
) -> tuple[list[str], list[str], list[str]]:
    expected_paths = set(expected)
    actual_paths = set(actual)
    added = sorted(actual_paths - expected_paths)
    removed = sorted(expected_paths - actual_paths)
    changed = sorted(
        path
        for path in expected_paths & actual_paths
        if expected[path].get("sha256") != actual[path].get("sha256")
        or expected[path].get("bytes") != actual[path].get("bytes")
    )
    return added, removed, changed


def matches_any(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def ensure_root(root_value: str) -> Path:
    root = Path(root_value).resolve()
    if not root.is_dir():
        raise ValueError(f"Projektkatalogen finns inte: {root}")
    return root


def write_log_header(root: Path) -> None:
    path = root / REVISION_LOG
    if path.exists():
        return
    path.write_text(
        "# Revisionslogg\n\n"
        "Denna logg uppdateras av `scripts/project_integrity.py`. "
        "Revisionerna avser projektpaketets kanoniska tillstånd.\n\n"
        "| Revision | Tidpunkt (UTC) | Åtgärd | Ändrade filer | Zip-fil |\n"
        "|---:|---|---|---|---|\n",
        encoding="utf-8",
    )


def append_log(root: Path, revision: int, operation: str, changed: list[str], zip_name: str) -> None:
    write_log_header(root)
    safe_operation = operation.replace("|", "\\|").replace("\n", " ")
    safe_files = ", ".join(f"`{path}`" for path in changed) if changed else "Inga"
    safe_zip = zip_name.replace("|", "\\|")
    with (root / REVISION_LOG).open("a", encoding="utf-8") as handle:
        handle.write(f"| {revision} | {utc_now()} | {safe_operation} | {safe_files} | `{safe_zip}` |\n")


def normalize_zip_name(name: str) -> str:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or any(part == ".." for part in path.parts):
        raise ValueError(f"Osäker sökväg i zip: {name}")
    return path.as_posix().lstrip("./")


def relevant_zip_files(archive: zipfile.ZipFile) -> list[tuple[zipfile.ZipInfo, str]]:
    result: list[tuple[zipfile.ZipInfo, str]] = []
    for info in archive.infolist():
        if info.is_dir():
            continue
        normalized = normalize_zip_name(info.filename)
        parts = PurePosixPath(normalized).parts
        if not normalized or any(part in IGNORED_PARTS for part in parts):
            continue
        result.append((info, normalized))
    return result


def detect_project_prefix(paths: list[str]) -> str:
    if not paths:
        return ""
    split = [PurePosixPath(path).parts for path in paths]
    first_parts = {parts[0] for parts in split if parts}
    if len(first_parts) == 1 and all(len(parts) > 1 for parts in split):
        return next(iter(first_parts)) + "/"
    return ""


def strip_prefix(path: str, prefix: str) -> str:
    return path[len(prefix) :] if prefix and path.startswith(prefix) else path


def looks_empty_or_template(data: bytes) -> bool:
    text = data.decode("utf-8", errors="replace").strip()
    lowered = text.lower()
    return (
        len(text) < 80
        or "[kapiteltext]" in lowered
        or re.search(r"^#\s*x\.", text, flags=re.IGNORECASE | re.MULTILINE) is not None
    )


def cmd_audit_legacy(args: argparse.Namespace) -> int:
    source = Path(args.source_zip).resolve()
    if not source.is_file():
        print(f"FEL: Zip-filen finns inte: {source}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    duplicate_paths: list[str] = []
    alternative_candidates: dict[str, list[str]] = {}
    chapter_files: dict[str, dict[str, Any]] = {}

    try:
        with zipfile.ZipFile(source, "r") as archive:
            try:
                entries = relevant_zip_files(archive)
            except ValueError as exc:
                errors.append(str(exc))
                entries = []

            normalized_paths = [path for _, path in entries]
            seen: set[str] = set()
            for path in normalized_paths:
                if path in seen:
                    duplicate_paths.append(path)
                seen.add(path)
            if duplicate_paths:
                errors.append("Zipen innehåller dubbla filsökvägar: " + ", ".join(sorted(set(duplicate_paths))))

            chapter_root_prefixes: set[str] = set()
            chapter_anywhere_re = re.compile(r"(?:^|/)kapitel/kapitel-\d{2,}\.md$")
            for path in normalized_paths:
                match = chapter_anywhere_re.search(path)
                if match:
                    raw_prefix = path[: match.start()].rstrip("/")
                    chapter_root_prefixes.add((raw_prefix + "/") if raw_prefix else "")
            if len(chapter_root_prefixes) > 1:
                errors.append(
                    "Zipen verkar innehålla flera projektträd med kanoniska kapitel: "
                    + ", ".join(sorted(value or "<ziprot>" for value in chapter_root_prefixes))
                )
                prefix = ""
            elif len(chapter_root_prefixes) == 1:
                prefix = next(iter(chapter_root_prefixes))
            else:
                prefix = detect_project_prefix(normalized_paths)

            relative_entries = [(info, strip_prefix(path, prefix)) for info, path in entries]
            canonical_numbers: dict[int, str] = {}

            for info, relative in relative_entries:
                if relative == MANIFEST_NAME:
                    errors.append(
                        "Zipen innehåller project-manifest.json och är därför inte ett manifestlöst äldre projekt. "
                        "Kör verify/reparation i stället för legacy-migrering."
                    )

                match = CANONICAL_CHAPTER_RE.fullmatch(relative)
                if match:
                    number = int(match.group(1))
                    if number in canonical_numbers:
                        errors.append(
                            f"Flera kanoniska kapitelfiler motsvarar kapitel {number}: "
                            f"{canonical_numbers[number]}, {relative}"
                        )
                        continue
                    canonical_numbers[number] = relative
                    data = archive.read(info)
                    chapter_files[relative] = {
                        "number": number,
                        "sha256": sha256_bytes(data),
                        "bytes": len(data),
                        "looks_empty_or_template": looks_empty_or_template(data),
                    }
                    if chapter_files[relative]["looks_empty_or_template"]:
                        warnings.append(f"Kapitelfilen verkar tom eller vara malltext: {relative}")
                    continue

                parts = PurePosixPath(relative).parts
                if len(parts) >= 2 and parts[-2] == "kapitel":
                    candidate_match = CHAPTER_CANDIDATE_RE.fullmatch(parts[-1])
                    if candidate_match:
                        number = str(int(candidate_match.group(1)))
                        alternative_candidates.setdefault(number, []).append(relative)

            for number_text, candidates in sorted(alternative_candidates.items(), key=lambda item: int(item[0])):
                number = int(number_text)
                if number in canonical_numbers or len(candidates) > 1:
                    errors.append(
                        f"Konkurrerande kapitelversioner för kapitel {number}: "
                        + ", ".join(([canonical_numbers[number]] if number in canonical_numbers else []) + candidates)
                    )
                else:
                    errors.append(
                        f"Möjlig kapitelfil har icke-kanoniskt namn och måste avgöras före migrering "
                        f"(kapitel {number}): {candidates[0]}"
                    )

            if not chapter_files:
                warnings.append("Inga kanoniska kapitelfiler hittades under kapitel/kapitel-NN.md")

    except zipfile.BadZipFile as exc:
        print(f"FEL: Ogiltig zip-fil: {exc}", file=sys.stderr)
        return 2

    chapter_hashes = {path: info["sha256"] for path, info in sorted(chapter_files.items())}
    numbers = sorted(int(info["number"]) for info in chapter_files.values())
    missing: list[int] = []
    if numbers:
        present = set(numbers)
        missing = [number for number in range(numbers[0], numbers[-1] + 1) if number not in present]
        if missing:
            warnings.append("Kapitelnummer saknas i serien: " + ", ".join(str(value) for value in missing))

    payload = {
        "audit_schema_version": 1,
        "audit_type": "legacy_project_zip",
        "audited_at": utc_now(),
        "source_zip_name": source.name,
        "source_zip_sha256": sha256_file(source),
        "source_manifest_present": any("project-manifest.json" in error for error in errors),
        "project_root_prefix": locals().get("prefix", ""),
        "can_migrate": not errors,
        "errors": errors,
        "warnings": warnings,
        "duplicate_paths": sorted(set(duplicate_paths)),
        "alternative_chapter_candidates": alternative_candidates,
        "chapters": {
            "count": len(numbers),
            "first": numbers[0] if numbers else None,
            "latest": numbers[-1] if numbers else None,
            "missing": missing,
            "hashes": chapter_hashes,
            "files": chapter_files,
        },
    }

    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).resolve().write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if payload["can_migrate"] else 1


def load_legacy_audit(path_value: str) -> dict[str, Any]:
    path = Path(path_value).resolve()
    if not path.is_file():
        raise ValueError(f"Legacy-auditfilen finns inte: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Ogiltig JSON i legacy-auditfilen: {exc}") from exc
    if not isinstance(value, dict) or value.get("audit_type") != "legacy_project_zip":
        raise ValueError("Legacy-auditfilen har fel format")
    if value.get("can_migrate") is not True:
        raise ValueError("Legacy-auditen innehåller blockerande fel; migrering får inte fortsätta")
    return value


def verify_legacy_chapters(root: Path, audit: dict[str, Any]) -> tuple[bool, list[str]]:
    actual_files = inventory(root)
    actual_hashes = chapter_summary(actual_files)["hashes"]
    expected_hashes = audit.get("chapters", {}).get("hashes", {})
    if not isinstance(expected_hashes, dict):
        return False, ["Legacy-auditen saknar giltiga kapitelhashar"]
    problems: list[str] = []
    expected_paths = set(expected_hashes)
    actual_paths = set(actual_hashes)
    for path in sorted(expected_paths - actual_paths):
        problems.append(f"Kapitelfil saknas efter uppackning/migrering: {path}")
    for path in sorted(actual_paths - expected_paths):
        problems.append(f"Ny eller oväntad kapitelfil har tillkommit: {path}")
    for path in sorted(expected_paths & actual_paths):
        if expected_hashes[path] != actual_hashes[path]:
            problems.append(f"Kapitelhash har ändrats sedan legacy-auditen: {path}")
    return not problems, problems


def cmd_init(args: argparse.Namespace) -> int:
    root = ensure_root(args.root)
    path = manifest_path(root)
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(
                f"FEL: {MANIFEST_NAME} finns men är skadat eller oläsbart ({exc}). "
                "Detta är inte ett legacy-projekt och manifestet får inte skrivas över med init.",
                file=sys.stderr,
            )
            return 2
        is_template = isinstance(existing, dict) and str(existing.get("project_id", "")).startswith("TEMPLATE-")
        if not is_template:
            print(
                f"FEL: {MANIFEST_NAME} finns redan. Kör verify eller gör en uttrycklig reparationsrevision; "
                "init får inte skriva över ett befintligt modernt manifest.",
                file=sys.stderr,
            )
            return 2
        if args.legacy_migration:
            print(
                f"FEL: Legacy-migrering kräver att {MANIFEST_NAME} saknas helt. "
                "Ta inte bort ett befintligt manifest för att kringgå verifiering.",
                file=sys.stderr,
            )
            return 2

    migration: dict[str, Any] | None = None
    if args.legacy_migration:
        if args.revision != 1:
            print("FEL: Den första revisionslåsta legacy-baslinjen ska vara revision 1.", file=sys.stderr)
            return 2
        if not args.source_zip_name:
            print("FEL: --source-zip-name krävs vid legacy-migrering.", file=sys.stderr)
            return 2
        if not args.legacy_audit:
            print("FEL: --legacy-audit krävs vid legacy-migrering.", file=sys.stderr)
            return 2
        try:
            audit = load_legacy_audit(args.legacy_audit)
        except ValueError as exc:
            print(f"FEL: {exc}", file=sys.stderr)
            return 2
        if audit.get("source_zip_name") != Path(args.source_zip_name).name:
            print(
                "FEL: Legacy-auditen avser en annan källzip än --source-zip-name.",
                file=sys.stderr,
            )
            return 2
        preserved, problems = verify_legacy_chapters(root, audit)
        if not preserved:
            for problem in problems:
                print(f"FEL: {problem}", file=sys.stderr)
            print("FEL: Befintliga kapitel är inte byte-identiska med den auditerade källzipen.", file=sys.stderr)
            return 1
        migration = {
            "migrated_from_legacy_project": True,
            "source_zip_name": audit["source_zip_name"],
            "source_zip_sha256": audit["source_zip_sha256"],
            "source_manifest_present": False,
            "chapter_files_preserved": True,
            "source_chapter_count": audit.get("chapters", {}).get("count", 0),
            "source_chapter_hashes": audit.get("chapters", {}).get("hashes", {}),
            "audit_schema_version": audit.get("audit_schema_version", 1),
            "migrated_at": utc_now(),
        }

    zip_name = args.zip_name or f"{args.slug}-r{args.revision:04d}.zip"
    files_before_log = inventory(root)
    append_log(root, args.revision, args.operation, sorted(files_before_log), zip_name)
    files = inventory(root)
    now = utc_now()
    parent_revision = None if args.legacy_migration or args.revision == 0 else args.revision - 1
    operation_type = "legacy_migration" if args.legacy_migration else "init"
    manifest = {
        "schema_version": 1,
        "project_id": args.project_id or str(uuid.uuid4()),
        "project_slug": args.slug,
        "revision": args.revision,
        "parent_revision": parent_revision,
        "created_at": now,
        "updated_at": now,
        "canonical_zip_name": zip_name,
        "tracked_files": files,
        "chapters": chapter_summary(files),
        "migration": migration,
        "last_operation": {
            "type": operation_type,
            "description": args.operation,
            "changed_files": sorted(files),
            "source_zip_name": args.source_zip_name or None,
            "source_revision": None,
        },
    }
    save_manifest(root, manifest)
    print(
        f"OK: initierade projekt {manifest['project_id']} revision {manifest['revision']} "
        f"med {len(files)} spårade filer och {manifest['chapters']['count']} kapitel."
    )
    if args.legacy_migration:
        print("OK: samtliga befintliga kapitelfiler är byte-identiska med den auditerade äldre zipen.")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    root = ensure_root(args.root)
    try:
        manifest = load_manifest(root)
    except ValueError as exc:
        print(f"FEL: {exc}", file=sys.stderr)
        return 2

    errors = validate_manifest_shape(manifest)
    if errors:
        for error in errors:
            print(f"FEL: {error}", file=sys.stderr)
        return 2

    actual = inventory(root)
    expected = manifest["tracked_files"]
    added, removed, changed = compare_inventory(expected, actual)
    chapter_actual = chapter_summary(actual)

    if added or removed or changed:
        if added:
            print("FEL: Oregistrerade nya filer: " + ", ".join(added), file=sys.stderr)
        if removed:
            print("FEL: Registrerade filer saknas: " + ", ".join(removed), file=sys.stderr)
        if changed:
            print("FEL: Filer med fel hash/storlek: " + ", ".join(changed), file=sys.stderr)
        return 1

    if manifest.get("chapters") != chapter_actual:
        print("FEL: Kapitelöversikten i manifestet stämmer inte med filinventeringen.", file=sys.stderr)
        return 1

    migration = manifest.get("migration")
    if isinstance(migration, dict) and migration.get("migrated_from_legacy_project"):
        source_hashes = migration.get("source_chapter_hashes", {})
        current_hashes = chapter_actual.get("hashes", {})
        for path, source_hash in source_hashes.items():
            if path not in current_hashes:
                print(f"FEL: Migrerat ursprungskapitel saknas: {path}", file=sys.stderr)
                return 1
            # Senare explicita kapitelrevisioner får ändra dessa hashvärden. Därför är detta
            # endast en historisk migrationsuppgift, inte ett evigt lås efter revision 1.
            if manifest["revision"] == 1 and current_hashes[path] != source_hash:
                print(f"FEL: Ursprungskapitlet ändrades i migrationsrevisionen: {path}", file=sys.stderr)
                return 1

    print(
        f"OK: revision {manifest['revision']} är verifierad. "
        f"{len(actual)} spårade filer, {chapter_actual['count']} kapitel, "
        f"senaste kapitel {chapter_actual['latest']}."
    )
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = ensure_root(args.root)
    try:
        manifest = load_manifest(root)
    except ValueError as exc:
        print(f"FEL: {exc}", file=sys.stderr)
        return 2
    errors = validate_manifest_shape(manifest)
    if errors:
        for error in errors:
            print(f"FEL: {error}", file=sys.stderr)
        return 2
    actual = inventory(root)
    added, removed, changed = compare_inventory(manifest["tracked_files"], actual)
    payload = {
        "project_id": manifest["project_id"],
        "project_slug": manifest["project_slug"],
        "revision": manifest["revision"],
        "canonical_zip_name": manifest["canonical_zip_name"],
        "migration": manifest.get("migration"),
        "chapters": chapter_summary(actual),
        "pending_changes": {
            "added": added,
            "removed": removed,
            "changed": changed,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def cmd_commit(args: argparse.Namespace) -> int:
    root = ensure_root(args.root)
    try:
        manifest = load_manifest(root)
    except ValueError as exc:
        print(f"FEL: {exc}", file=sys.stderr)
        return 2

    errors = validate_manifest_shape(manifest)
    if errors:
        for error in errors:
            print(f"FEL: {error}", file=sys.stderr)
        return 2

    old_revision = manifest["revision"]
    if args.expected_revision is not None and old_revision != args.expected_revision:
        print(
            f"FEL: Förväntade revision {args.expected_revision}, men manifestet är revision {old_revision}.",
            file=sys.stderr,
        )
        return 1

    current_before_log = inventory(root)
    added, removed, changed = compare_inventory(manifest["tracked_files"], current_before_log)
    all_changes = sorted(set(added + removed + changed))
    disallowed = [path for path in all_changes if not matches_any(path, args.allow)]
    if disallowed:
        print(
            "FEL: Följande ändringar ligger utanför tillåten ändringslista: " + ", ".join(disallowed),
            file=sys.stderr,
        )
        print("Tillåtna mönster: " + ", ".join(args.allow), file=sys.stderr)
        return 1

    new_revision = old_revision + 1
    append_log(root, new_revision, args.operation, all_changes, args.zip_name)
    final_files = inventory(root)
    # Revisionsloggen ändras av verktyget självt och räknas alltid som intern, godkänd ändring.
    final_changes = sorted(set(all_changes + [REVISION_LOG]))
    manifest.update(
        {
            "schema_version": 1,
            "revision": new_revision,
            "parent_revision": old_revision,
            "updated_at": utc_now(),
            "canonical_zip_name": args.zip_name,
            "tracked_files": final_files,
            "chapters": chapter_summary(final_files),
            "last_operation": {
                "type": "commit",
                "description": args.operation,
                "changed_files": final_changes,
                "source_zip_name": args.source_zip_name or manifest.get("canonical_zip_name"),
                "source_revision": old_revision,
            },
        }
    )
    save_manifest(root, manifest)

    # Slutkontroll efter att manifestet skrivits.
    actual_after = inventory(root)
    added2, removed2, changed2 = compare_inventory(manifest["tracked_files"], actual_after)
    if added2 or removed2 or changed2:
        print("FEL: Intern slutkontroll misslyckades efter commit.", file=sys.stderr)
        return 1

    print(
        f"OK: skapade revision {new_revision} från revision {old_revision}. "
        f"Ändrade filer: {', '.join(final_changes) if final_changes else 'inga'}. "
        f"Kapitel: {manifest['chapters']['count']}, senaste: {manifest['chapters']['latest']}."
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser(
        "audit-legacy",
        help="Granska en äldre manifestlös projektzip och lås kapitlens ursprungshashar",
    )
    audit_parser.add_argument("source_zip")
    audit_parser.add_argument("--output", help="Skriv auditresultatet till en JSON-fil utanför projektet")
    audit_parser.set_defaults(func=cmd_audit_legacy)

    init_parser = subparsers.add_parser("init", help="Skapa ett nytt manifest eller en verifierad legacy-baslinje")
    init_parser.add_argument("root")
    init_parser.add_argument("--slug", required=True)
    init_parser.add_argument("--project-id")
    init_parser.add_argument("--revision", type=int, default=0)
    init_parser.add_argument("--zip-name")
    init_parser.add_argument("--source-zip-name")
    init_parser.add_argument("--operation", default="Projektets integritetsmanifest skapades")
    init_parser.add_argument("--legacy-migration", action="store_true")
    init_parser.add_argument(
        "--legacy-audit",
        help="JSON från audit-legacy; obligatorisk tillsammans med --legacy-migration",
    )
    init_parser.set_defaults(func=cmd_init)

    verify_parser = subparsers.add_parser("verify", help="Verifiera alla spårade filer mot manifestet")
    verify_parser.add_argument("root")
    verify_parser.set_defaults(func=cmd_verify)

    status_parser = subparsers.add_parser("status", help="Visa revision, kapitel och väntande filändringar")
    status_parser.add_argument("root")
    status_parser.set_defaults(func=cmd_status)

    commit_parser = subparsers.add_parser("commit", help="Kontrollera ändringslistan och skapa nästa revision")
    commit_parser.add_argument("root")
    commit_parser.add_argument("--operation", required=True)
    commit_parser.add_argument("--zip-name", required=True)
    commit_parser.add_argument("--source-zip-name")
    commit_parser.add_argument("--expected-revision", type=int)
    commit_parser.add_argument(
        "--allow",
        action="append",
        required=True,
        help="Tillåten sökväg eller glob. Kan anges flera gånger.",
    )
    commit_parser.set_defaults(func=cmd_commit)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(f"FEL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
