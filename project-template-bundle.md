# Romanprojektmall – revisionslåst ZIP/GitHub-version

Detta är den samlade projektmallen för Romanskaparen. Den genereras deterministiskt från `templates/romanprojekt/` och innehåller schema 2, ZIP/GitHub-lagringsmetadata och det filsystembaserade integritetsverktyget.

Nya projekt initieras i valt kanoniskt lagringsläge. ZIP- och GitHub-projekt använder samma interna revisioner, manifest, SHA-256-hashar och kapitelskydd. GitHub-API, branchlås, commits och pull requests hanteras av GPT-arbetsflödet, inte av integritetsverktyget.

Mallen `kapitel/kapitelmall.md` finns från början, men numeriska kapitelfiler skapas först när kapiteltext finns.

## `README.md`

````markdown
# Romanprojekt

Detta projekt använder revisionslås, manifest och SHA-256-kontroll för att skydda kapitelversionerna.

Detta är projektarkivet för en roman som utvecklas steg för steg. Projektet har exakt ett kanoniskt lagringsläge åt gången: ZIP eller GitHub.

## Metadata att fastställa tidigt
- Titel
- Undertitel
- Författare
- Genre
- Målgrupp
- Om omslagsbild/framsida ska skapas
- Kanoniskt lagringsläge: ZIP eller GitHub

## Rekommenderat arbetsflöde
1. Planera romankärnan: huvudperson, mål, hinder, insats och förändring.
2. Fastställ titel, undertitel och författare.
3. Avgör om omslagsbild ska skapas nu eller senare.
4. Skapa synopsis, kapitelplan, romanbibel och stilguide.
5. Skriv ett kapitel i taget i chatten.
6. Justera kapitlet tills användaren är nöjd.
7. Uppdatera projektfilerna och projektstatus.
8. Spara och slutverifiera enligt valt lagringsläge.
9. Fortsätt med nästa kapitel, revision eller export.

## Säker filhantering

- `project-manifest.json` anger projekt-id, revision, lagringsläge och hash för varje fil.
- `revision-log.md` visar projektets interna revisioner.
- `scripts/project_integrity.py` verifierar projektet före och efter ändringar.
- Verktygets `audit-legacy`-läge granskar äldre manifestlösa ZIP-filer innan migrering.
- Varje arbetssteg ska utgå från exakt en uttryckligen vald och låst projektkälla.
- ZIP- och GitHub-källor får aldrig blandas i samma operation.
- En ändring är inte sparad förrän den finns i en slutverifierad ZIP eller Git-commit enligt det kanoniska lagringsläget.

### ZIP-läge

- En uttryckligen vald projekt-ZIP är kanonisk källa.
- Varje sparad ändring levereras som nästa verifierade ZIP-revision.
- `canonical_zip_name` anger den aktuella kanoniska ZIP-filen.

### GitHub-läge

- Repository, projektrot, default branch, arbetsbranch och commit-SHA låser källan.
- Repositoryts default branch är basbranch.
- Standardarbetsbranch är `development`, om användaren inte väljer annat.
- Ändringar committas på arbetsbranchen och en PR skapas eller återanvänds mot default branch.
- Användaren ansvarar normalt för merge. Ingen automatisk merge eller force push används.
- Git-SHA lagras inte som obligatoriskt manifestfält; den redovisas i revisionskvittensen och Git-historiken.

Grundkommandon:

```bash
python scripts/project_integrity.py verify .
python scripts/project_integrity.py status .
```

## Viktiga filer
- `projektstatus.md` visar nuvarande fas, lagringsläge, senaste godkända kapitel och nästa rekommenderade steg.
- `project-index.md` visar projektkälla, revision, synk och integritetsstatus.
- `roman-bibel.md` innehåller projektets centrala fakta.
- `synopsis.md` sammanfattar hela handlingen.
- `kapitelplan.md` är färdplanen för romanen.
- `stilguide.md` håller språk, ton och perspektiv konsekvent.
- `tidslinje.md` håller ordning på händelser.
- `kontinuitetsanteckningar.md` fångar fakta som inte får motsägas.
- `revisionsonskemal.md` samlar planerade förbättringar.
- `arbetslogg.md` visar vad som har gjorts.
- `kapitel/` innehåller kapitelutkast och godkända kapitel.
- `exports/exportlogg.md` visar skapade EPUB/PDF- och ZIP-exporter.

## Byte av lagringsläge

Byte mellan ZIP och GitHub är en uttrycklig migreringsoperation. `project_id` ska bevaras, projektrevisionen ska vara sammanhängande och endast ett läge får vara kanoniskt efter migreringen. En ZIP som exporteras från GitHub byter inte automatiskt lagringsläge.

## Publicering
- `publishing/` innehåller metadata och sättningsregler för EPUB/PDF.
- `kapitelnoteringar.md` innehåller anteckningar som inte ska exporteras som boktext.
````

## `project-manifest.json`

```json
{
  "canonical_zip_name": "ERSATT-VID-PROJEKTSKAPANDE.zip",
  "chapters": {
    "count": 0,
    "first": null,
    "hashes": {},
    "latest": null,
    "missing": []
  },
  "created_at": "ERSATT-VID-PROJEKTSKAPANDE",
  "last_operation": {
    "changed_files": [],
    "description": "Kör scripts/project_integrity.py init när projektet skapas",
    "source_revision": null,
    "source_zip_name": null,
    "type": "template"
  },
  "migration": null,
  "parent_revision": null,
  "project_id": "TEMPLATE-ERSATT-MED-UUID",
  "project_slug": "ersatt-med-projektnamn",
  "revision": 0,
  "schema_version": 2,
  "storage": {
    "base_branch": null,
    "mode": "zip",
    "project_root": "/",
    "repository": null,
    "working_branch": null
  },
  "tracked_files": {},
  "updated_at": "ERSATT-VID-PROJEKTSKAPANDE"
}
```

## `revision-log.md`

```markdown
# Revisionslogg

Denna logg uppdateras av `scripts/project_integrity.py`. Revisionerna avser projektpaketets kanoniska tillstånd.

| Revision | Tidpunkt (UTC) | Åtgärd | Ändrade filer | Zip-fil |
|---:|---|---|---|---|
```

## `project-index.md`

```markdown
# Project Index

## Projekt
- Project-id:
- Revision: 0
- Källrevision: ingen
- Kanoniskt lagringsläge: ZIP / GitHub
- Kanonisk ZIP-fil:
- GitHub-repository:
- Projektrot: /
- Basbranch:
- Arbetsbranch:
- Titel:
- Undertitel:
- Författare:
- Senast uppdaterad:
- Nuvarande fas:
- Senast godkända kapitel:
- Nästa kapitel:
- Omslagsbild: Planerad / Skapad / Saknas

Fyll endast i lagringsmetadata som gäller för valt kanoniskt läge. Commit-SHA hör till arbetsstegets revisionskvittens och Git-historik och ska inte behandlas som beständig manifestmetadata.

## Kapitelinventering
| Kapitel | Fil | Titel | Status |
|---|---|---|---|

## Kanoniska projektfiler
| Fil | Syfte | Status |
|---|---|---|
| README.md | Start och arbetsflöde | OK |
| project-manifest.json | Revision, lagringsläge, filinventering och SHA-256 | Ej initierad |
| revision-log.md | Intern revisionshistorik | OK |
| roman-bibel.md | Centrala fakta | OK |
| synopsis.md | Handlingsöversikt | OK |
| kapitelplan.md | Kapitelplan och status | OK |
| stilguide.md | Språk, ton och perspektiv | OK |
| tidslinje.md | Händelser i romanen | OK |
| projektstatus.md | Senaste status och nästa steg | OK |
| kontinuitetsanteckningar.md | Fakta och öppna trådar | OK |
| revisionsonskemal.md | Revisionsidéer | OK |
| arbetslogg.md | Projektändringar | OK |
| karaktarer/huvudperson.md | Huvudperson | OK |
| karaktarer/antagonist.md | Motkraft | OK |
| karaktarer/bifigurer.md | Bifigurer | OK |
| kapitel/kapitelmall.md | Kapitelmall | OK |
| exports/README.md | Exportinformation | OK |
| exports/exportlogg.md | Logg över genererade exporter | OK |
| scripts/project_integrity.py | Deterministisk integritetskontroll | OK |

## Lagringskontroll
- Aktivt läge: ZIP / GitHub
- Källan entydigt vald: Nej
- ZIP-källa: [filnamn eller ej tillämpligt]
- GitHub-källa: [repository, projektrot, branch eller ej tillämpligt]
- Öppen PR: [nummer/status eller ej tillämpligt]
- Resultat: Ej initierad

## Integritetskontroll
- Manifest verifierat: Nej, initiera vid projektskapande
- Oförändrade kapitel hashverifierade: Ej tillämpligt
- Senaste verifieringsresultat:

## Synkkontroll
- Kapitel i `kapitel/`: 0
- Senaste kapitel i `kapitelplan.md`: inget
- Senaste kapitel i `projektstatus.md`: inget
- Senaste kapitel i `arbetslogg.md`: inget
- Senaste export: ingen
- Resultat: Synkad

## Publicering
- `publishing/` innehåller metadata och sättningsregler för EPUB/PDF.
- `kapitelnoteringar.md` innehåller anteckningar som inte ska exporteras som boktext.
```

## `arbetslogg.md`

```markdown
# Arbetslogg

## Logg

| Datum | Ändring | Kommentar |
|---|---|---|
|  | Projekt skapat |  |

## Nästa rekommenderade steg

- Fyll i romanbibel.
- Skapa synopsis.
- Skapa kapitelplan.
```

## `kapitelplan.md`

```markdown
# Kapitelplan

## Översikt

| Kapitel | Titel | Syfte | Viktiga händelser | Status |
|---|---|---|---|---|
| 1 |  | Introducera huvudperson och startläge |  | Ej skrivet |

## Kapitelanteckningar

### Kapitel 1
- Mål:
- Konflikt:
- Slutpunkt:
```

## `projektstatus.md`

```markdown
# Projektstatus

## Projektmetadata
- Project-id:
- Revision: 0
- Kanoniskt lagringsläge: ZIP / GitHub
- Kanonisk ZIP-fil:
- GitHub-repository:
- Projektrot: /
- Basbranch:
- Arbetsbranch:
- Pull request:
- Titel:
- Undertitel:
- Författare:
- Omslagsbild: Planerad / Skapad / Saknas

Fyll endast i de ZIP- eller GitHub-fält som gäller för projektets kanoniska lagringsläge. Aktuella commit-SHA:n redovisas i revisionskvittensen och hämtas alltid på nytt inför en GitHub-operation.

## Nuvarande fas
Planering / Kapitelutkast / Revision / Slutputs / Export

## Senast godkända kapitel eller del
- Senast godkända: [exempel: Kapitel 1]
- Senast ändrad: [exempel: Kapitel 2, ej godkänt]

## Nästa rekommenderade steg
[Beskriv nästa konkreta steg, till exempel: Skriv kapitel 3 enligt kapitelplanen eller revidera dialogen i kapitel 2.]

## Lagrings- och synkstatus
- Senaste kanoniska projektrevision:
- Senaste lagringsoperation: ZIP levererad / Git-commit publicerad / Ingen
- GitHub-brancher synkade: Ja / Nej / Ej tillämpligt
- Öppen PR: [nummer/status eller ej tillämpligt]
- Extern ändring upptäckt: Nej / Ja, kräver analys

## Viktiga öppna beslut
- [Beslut 1]
- [Beslut 2]

## Risker att bevaka
- [Exempel: Huvudpersonen behöver agera mer aktivt.]
- [Exempel: För mycket bakgrundsinformation kommer för tidigt.]
- [Exempel: Mysteriets ledtrådar behöver planteras rättvist.]
- [Exempel: Default branch och arbetsbranch har ändrat samma kanoniska fil.]

## Kontinuitet som måste följas upp snart
- [Punkt 1]
- [Punkt 2]

## Användarens aktuella önskemål
- [Ton, stil, ändringar eller prioriteringar]
```

## `roman-bibel.md`

```markdown
# Romanbibel

## Titel

## Undertitel

## Författare

## Arbetstitel

## Genre

## Målgrupp

## Ton och känsla

## Omslagsbild/framsida
- Status:
- Önskad stil eller motiv:

## Premiss

## Huvudkonflikt

## Teman

## Huvudperson

## Antagonist eller motkraft

## Viktiga bifigurer

## Miljö och värld

## Centrala regler och begränsningar

## Viktiga återkommande motiv

## Slutets riktning
```

## `synopsis.md`

```markdown
# Synopsis

## Titel

## Undertitel

## Författare

## Kort baksidestext

## Sammanfattning av hela handlingen

## Början

## Mitt

## Slut

## Viktiga vändpunkter

## Viktiga avslöjanden

## Saker som måste planteras tidigt
```

## `stilguide.md`

```markdown
# Stilguide

## Språk

## Berättarperspektiv

## Tempus

## Meningslängd och rytm

## Dialogstil

## Beskrivningsnivå

## Ton

## Saker att undvika

## Exempel på önskad känsla
```

## `tidslinje.md`

```markdown
# Tidslinje

## Före romanens början

## Under romanen

| Tidpunkt | Händelse | Berörda karaktärer | Kapitel |
|---|---|---|---|

## Efter romanens slut
```

## `kontinuitetsanteckningar.md`

```markdown
# Kontinuitetsanteckningar

## Fasta fakta

## Karaktärsfakta

## Relationsutveckling

## Miljöfakta

## Ledtrådar och planteringar

## Öppna frågor

## Saker som måste följas upp

## Saker som inte får motsägas
```

## `revisionsonskemal.md`

```markdown
# Revisionsönskemål

Här samlas saker som ska förbättras senare men inte behöver stoppa framåtskrivandet.

| Plats | Önskad ändring | Prioritet | Status |
|---|---|---|---|
```

## `kapitelnoteringar.md`

```markdown
# Kapitelnoteringar

Kapitelnoteringar sparas här och ska inte ligga i kapitelfilerna.

## Kapitel 1 – Kapitelrubrik
- Kort sammanfattning:
- Nya fakta/ledtrådar:
- Kontinuitetsrisker:
- Öppna frågor:
- Nästa skrivsteg:
```

## `karaktarer/huvudperson.md`

```markdown
# Huvudperson

## Namn

## Roll

## Yttre mål

## Inre behov

## Rädsla

## Styrkor

## Svagheter

## Relationer

## Hemlighet eller konflikt

## Utveckling genom romanen
```

## `karaktarer/antagonist.md`

```markdown
# Antagonist eller motkraft

## Namn eller beskrivning

## Roll

## Mål

## Motivation

## Metoder

## Koppling till huvudpersonen

## Varför motkraften är trovärdig

## Utveckling genom romanen
```

## `karaktarer/bifigurer.md`

```markdown
# Bifigurer

## Bifigur 1

- Namn:
- Funktion i berättelsen:
- Relation till huvudpersonen:
- Viktig utveckling:

## Bifigur 2

- Namn:
- Funktion i berättelsen:
- Relation till huvudpersonen:
- Viktig utveckling:
```

## `kapitel/kapitelmall.md`

```markdown
# X. [Kapitelrubrik]

[Kapiteltext]
```

## `scripts/project_integrity.py`

```python
#!/usr/bin/env python3
"""Versions- och integritetskontroll för Romanskaparens projekt.

Verktyget arbetar endast med projektfiler på lokalt filsystem. GitHub-anrop,
branchlås och pull requests hanteras av Romanskaparen. Lagringsläget registreras
och verifieras i manifestet.
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
STORAGE_MODES = {"zip", "github"}


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
    return relative.as_posix() != MANIFEST_NAME and not any(
        part in IGNORED_PARTS for part in relative.parts
    )


def inventory(root: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            relative = path.relative_to(root)
            if should_track(relative):
                result[relative.as_posix()] = {
                    "sha256": sha256_file(path),
                    "bytes": path.stat().st_size,
                }
    return result


def chapter_number(path: str) -> int | None:
    match = CANONICAL_CHAPTER_RE.fullmatch(path)
    return int(match.group(1)) if match else None


def chapter_summary(files: dict[str, dict[str, Any]]) -> dict[str, Any]:
    numbers: list[int] = []
    hashes: dict[str, str] = {}
    for path, info in files.items():
        number = chapter_number(path)
        if number is not None:
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


def normalized_storage(manifest: dict[str, Any]) -> dict[str, Any]:
    storage = manifest.get("storage")
    if isinstance(storage, dict):
        return storage
    return {
        "mode": "zip",
        "repository": None,
        "project_root": "/",
        "base_branch": None,
        "working_branch": None,
    }


def validate_storage(storage: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    mode = storage.get("mode")
    if mode not in STORAGE_MODES:
        return ["storage.mode måste vara zip eller github"]
    if not isinstance(storage.get("project_root", "/"), str):
        errors.append("storage.project_root måste vara sträng")
    for key in ("repository", "base_branch", "working_branch"):
        if storage.get(key) is not None and not isinstance(storage.get(key), str):
            errors.append(f"storage.{key} måste vara sträng eller null")
    if mode == "github":
        for key in ("repository", "base_branch", "working_branch"):
            if not storage.get(key):
                errors.append(f"storage.{key} krävs i GitHub-läge")
        if storage.get("project_root", "/") != "/":
            errors.append("Första GitHub-versionen kräver storage.project_root = /")
    return errors


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
    schema = manifest.get("schema_version")
    if isinstance(schema, int) and schema not in (1, 2):
        errors.append("Endast manifest schema_version 1 och 2 stöds")
    if isinstance(manifest.get("revision"), int) and manifest["revision"] < 0:
        errors.append("Revision får inte vara negativ")
    if "migration" in manifest and not isinstance(manifest["migration"], (dict, type(None))):
        errors.append("Manifestfältet migration måste vara objekt eller null")
    if schema == 2:
        if not isinstance(manifest.get("storage"), dict):
            errors.append("Schema 2 kräver manifestfältet storage")
        else:
            errors.extend(validate_storage(manifest["storage"]))
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


def storage_label(storage: dict[str, Any], zip_name: str) -> str:
    if storage.get("mode") == "zip":
        return zip_name
    return f"{storage.get('repository')}:{storage.get('working_branch')}"


def write_log_header(root: Path) -> None:
    path = root / REVISION_LOG
    if path.exists():
        return
    path.write_text(
        "# Revisionslogg\n\n"
        "Denna logg uppdateras av `scripts/project_integrity.py`. "
        "Revisionerna avser projektets kanoniska tillstånd.\n\n"
        "| Revision | Tidpunkt (UTC) | Åtgärd | Ändrade filer | Lagringsreferens |\n"
        "|---:|---|---|---|---|\n",
        encoding="utf-8",
    )


def append_log(root: Path, revision: int, operation: str, changed: list[str], reference: str) -> None:
    write_log_header(root)
    safe_operation = operation.replace("|", "\\|").replace("\n", " ")
    safe_files = ", ".join(f"`{path}`" for path in changed) if changed else "Inga"
    safe_reference = reference.replace("|", "\\|")
    with (root / REVISION_LOG).open("a", encoding="utf-8") as handle:
        handle.write(
            f"| {revision} | {utc_now()} | {safe_operation} | {safe_files} | `{safe_reference}` |\n"
        )


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
        if normalized and not any(part in IGNORED_PARTS for part in parts):
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
    prefix = ""
    try:
        with zipfile.ZipFile(source, "r") as archive:
            entries = relevant_zip_files(archive)
            normalized_paths = [path for _, path in entries]
            seen: set[str] = set()
            for path in normalized_paths:
                if path in seen:
                    duplicate_paths.append(path)
                seen.add(path)
            if duplicate_paths:
                errors.append(
                    "Zipen innehåller dubbla filsökvägar: "
                    + ", ".join(sorted(set(duplicate_paths)))
                )
            chapter_root_prefixes: set[str] = set()
            chapter_anywhere_re = re.compile(r"(?:^|/)kapitel/kapitel-\d{2,}\.md$")
            for path in normalized_paths:
                match = chapter_anywhere_re.search(path)
                if match:
                    raw_prefix = path[: match.start()].rstrip("/")
                    chapter_root_prefixes.add((raw_prefix + "/") if raw_prefix else "")
            if len(chapter_root_prefixes) > 1:
                errors.append("Zipen verkar innehålla flera projektträd med kanoniska kapitel")
            elif len(chapter_root_prefixes) == 1:
                prefix = next(iter(chapter_root_prefixes))
            else:
                prefix = detect_project_prefix(normalized_paths)
            canonical_numbers: dict[int, str] = {}
            for info, path in entries:
                relative = strip_prefix(path, prefix)
                if relative == MANIFEST_NAME:
                    errors.append(
                        "Zipen innehåller project-manifest.json och är inte ett manifestlöst äldre projekt"
                    )
                match = CANONICAL_CHAPTER_RE.fullmatch(relative)
                if match:
                    number = int(match.group(1))
                    data = archive.read(info)
                    if number in canonical_numbers:
                        errors.append(f"Flera kanoniska kapitelfiler motsvarar kapitel {number}")
                        continue
                    canonical_numbers[number] = relative
                    chapter_files[relative] = {
                        "number": number,
                        "sha256": sha256_bytes(data),
                        "bytes": len(data),
                        "looks_empty_or_template": looks_empty_or_template(data),
                    }
                    if chapter_files[relative]["looks_empty_or_template"]:
                        warnings.append(f"Kapitelfilen verkar tom eller vara malltext: {relative}")
                else:
                    parts = PurePosixPath(relative).parts
                    if len(parts) >= 2 and parts[-2] == "kapitel":
                        candidate = CHAPTER_CANDIDATE_RE.fullmatch(parts[-1])
                        if candidate:
                            alternative_candidates.setdefault(str(int(candidate.group(1))), []).append(relative)
            for number_text, candidates in alternative_candidates.items():
                errors.append(
                    f"Möjlig eller konkurrerande icke-kanonisk kapitelfil för kapitel {int(number_text)}: "
                    + ", ".join(candidates)
                )
            if not chapter_files:
                warnings.append("Inga kanoniska kapitelfiler hittades")
    except (zipfile.BadZipFile, ValueError) as exc:
        print(f"FEL: {exc}", file=sys.stderr)
        return 2
    numbers = sorted(int(info["number"]) for info in chapter_files.values())
    missing: list[int] = []
    if numbers:
        present = set(numbers)
        missing = [number for number in range(numbers[0], numbers[-1] + 1) if number not in present]
        if missing:
            warnings.append("Kapitelnummer saknas i serien: " + ", ".join(map(str, missing)))
    payload = {
        "audit_schema_version": 1,
        "audit_type": "legacy_project_zip",
        "audited_at": utc_now(),
        "source_zip_name": source.name,
        "source_zip_sha256": sha256_file(source),
        "source_manifest_present": any("project-manifest" in error for error in errors),
        "project_root_prefix": prefix,
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
            "hashes": {path: info["sha256"] for path, info in sorted(chapter_files.items())},
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
    value = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(value, dict)
        or value.get("audit_type") != "legacy_project_zip"
        or value.get("can_migrate") is not True
    ):
        raise ValueError("Legacy-auditfilen är ogiltig eller blockerad")
    return value


def verify_legacy_chapters(root: Path, audit: dict[str, Any]) -> tuple[bool, list[str]]:
    actual_hashes = chapter_summary(inventory(root))["hashes"]
    expected_hashes = audit.get("chapters", {}).get("hashes", {})
    problems: list[str] = []
    for path in sorted(set(expected_hashes) - set(actual_hashes)):
        problems.append(f"Kapitelfil saknas: {path}")
    for path in sorted(set(actual_hashes) - set(expected_hashes)):
        problems.append(f"Oväntad kapitelfil: {path}")
    for path in sorted(set(expected_hashes) & set(actual_hashes)):
        if expected_hashes[path] != actual_hashes[path]:
            problems.append(f"Kapitelhash har ändrats: {path}")
    return not problems, problems


def storage_from_args(args: argparse.Namespace) -> dict[str, Any]:
    storage = {
        "mode": args.storage_mode,
        "repository": None,
        "project_root": "/",
        "base_branch": None,
        "working_branch": None,
    }
    if args.storage_mode == "github":
        storage.update(
            {
                "repository": args.repository,
                "base_branch": args.base_branch,
                "working_branch": args.working_branch,
            }
        )
    errors = validate_storage(storage)
    if errors:
        raise ValueError("; ".join(errors))
    return storage


def cmd_init(args: argparse.Namespace) -> int:
    root = ensure_root(args.root)
    path = manifest_path(root)
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"FEL: Manifest finns men är skadat ({exc})", file=sys.stderr)
            return 2
        if not (
            isinstance(existing, dict)
            and str(existing.get("project_id", "")).startswith("TEMPLATE-")
        ):
            print("FEL: Manifest finns redan; init får inte skriva över det.", file=sys.stderr)
            return 2
        if args.legacy_migration:
            print("FEL: Legacy-migrering kräver att manifest saknas helt.", file=sys.stderr)
            return 2
    try:
        storage = storage_from_args(args)
    except ValueError as exc:
        print(f"FEL: {exc}", file=sys.stderr)
        return 2
    migration: dict[str, Any] | None = None
    if args.legacy_migration:
        if args.revision != 1 or not args.source_zip_name or not args.legacy_audit:
            print(
                "FEL: Legacy-migrering kräver revision 1, source-zip-name och legacy-audit.",
                file=sys.stderr,
            )
            return 2
        audit = load_legacy_audit(args.legacy_audit)
        if audit.get("source_zip_name") != Path(args.source_zip_name).name:
            print("FEL: Auditen avser annan källzip.", file=sys.stderr)
            return 2
        preserved, problems = verify_legacy_chapters(root, audit)
        if not preserved:
            for problem in problems:
                print("FEL: " + problem, file=sys.stderr)
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
    append_log(
        root,
        args.revision,
        args.operation,
        sorted(files_before_log),
        storage_label(storage, zip_name),
    )
    files = inventory(root)
    now = utc_now()
    manifest = {
        "schema_version": 2,
        "project_id": args.project_id or str(uuid.uuid4()),
        "project_slug": args.slug,
        "revision": args.revision,
        "parent_revision": None if args.legacy_migration or args.revision == 0 else args.revision - 1,
        "created_at": now,
        "updated_at": now,
        "canonical_zip_name": zip_name,
        "storage": storage,
        "tracked_files": files,
        "chapters": chapter_summary(files),
        "migration": migration,
        "last_operation": {
            "type": "legacy_migration" if args.legacy_migration else "init",
            "description": args.operation,
            "changed_files": sorted(files),
            "source_zip_name": args.source_zip_name or None,
            "source_revision": None,
        },
    }
    save_manifest(root, manifest)
    print(
        f"OK: initierade {manifest['project_id']} revision {manifest['revision']} "
        f"i {storage['mode']}-läge."
    )
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
            print("FEL: " + error, file=sys.stderr)
        return 2
    actual = inventory(root)
    added, removed, changed = compare_inventory(manifest["tracked_files"], actual)
    chapters = chapter_summary(actual)
    if added or removed or changed:
        if added:
            print("FEL: Oregistrerade nya filer: " + ", ".join(added), file=sys.stderr)
        if removed:
            print("FEL: Registrerade filer saknas: " + ", ".join(removed), file=sys.stderr)
        if changed:
            print("FEL: Filer med fel hash/storlek: " + ", ".join(changed), file=sys.stderr)
        return 1
    if manifest.get("chapters") != chapters:
        print("FEL: Kapitelöversikten stämmer inte.", file=sys.stderr)
        return 1
    migration = manifest.get("migration")
    if (
        isinstance(migration, dict)
        and migration.get("migrated_from_legacy_project")
        and manifest["revision"] == 1
    ):
        for path, source_hash in migration.get("source_chapter_hashes", {}).items():
            if chapters["hashes"].get(path) != source_hash:
                print(
                    f"FEL: Ursprungskapitlet ändrades i migrationsrevisionen: {path}",
                    file=sys.stderr,
                )
                return 1
    storage = normalized_storage(manifest)
    print(
        f"OK: revision {manifest['revision']} är verifierad i {storage['mode']}-läge. "
        f"{len(actual)} filer, {chapters['count']} kapitel."
    )
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = ensure_root(args.root)
    manifest = load_manifest(root)
    errors = validate_manifest_shape(manifest)
    if errors:
        for error in errors:
            print("FEL: " + error, file=sys.stderr)
        return 2
    actual = inventory(root)
    added, removed, changed = compare_inventory(manifest["tracked_files"], actual)
    payload = {
        "project_id": manifest["project_id"],
        "project_slug": manifest["project_slug"],
        "revision": manifest["revision"],
        "schema_version": manifest["schema_version"],
        "storage": normalized_storage(manifest),
        "canonical_zip_name": manifest["canonical_zip_name"],
        "migration": manifest.get("migration"),
        "chapters": chapter_summary(actual),
        "pending_changes": {"added": added, "removed": removed, "changed": changed},
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def cmd_commit(args: argparse.Namespace) -> int:
    root = ensure_root(args.root)
    manifest = load_manifest(root)
    errors = validate_manifest_shape(manifest)
    if errors:
        for error in errors:
            print("FEL: " + error, file=sys.stderr)
        return 2
    old_revision = manifest["revision"]
    if args.expected_revision is not None and old_revision != args.expected_revision:
        print(
            f"FEL: Förväntade revision {args.expected_revision}, men manifestet är {old_revision}.",
            file=sys.stderr,
        )
        return 1
    storage = normalized_storage(manifest)
    if args.storage_mode and args.storage_mode != storage["mode"]:
        print(
            "FEL: --storage-mode matchar inte manifestet; lagringsbyte kräver migration.",
            file=sys.stderr,
        )
        return 1
    current = inventory(root)
    added, removed, changed = compare_inventory(manifest["tracked_files"], current)
    all_changes = sorted(set(added + removed + changed))
    disallowed = [path for path in all_changes if not matches_any(path, args.allow)]
    if disallowed:
        print(
            "FEL: Ändringar utanför tillåten lista: " + ", ".join(disallowed),
            file=sys.stderr,
        )
        return 1
    new_revision = old_revision + 1
    previous_zip_name = manifest.get("canonical_zip_name")
    zip_name = args.zip_name or previous_zip_name or f"{manifest['project_slug']}-r{new_revision:04d}.zip"
    append_log(
        root,
        new_revision,
        args.operation,
        all_changes,
        storage_label(storage, zip_name),
    )
    final_files = inventory(root)
    final_changes = sorted(set(all_changes + [REVISION_LOG]))
    manifest.update(
        {
            "schema_version": 2,
            "revision": new_revision,
            "parent_revision": old_revision,
            "updated_at": utc_now(),
            "canonical_zip_name": zip_name,
            "storage": storage,
            "tracked_files": final_files,
            "chapters": chapter_summary(final_files),
            "last_operation": {
                "type": "commit",
                "description": args.operation,
                "changed_files": final_changes,
                "source_zip_name": args.source_zip_name
                or (previous_zip_name if storage["mode"] == "zip" else None),
                "source_revision": old_revision,
            },
        }
    )
    save_manifest(root, manifest)
    added2, removed2, changed2 = compare_inventory(
        manifest["tracked_files"], inventory(root)
    )
    if added2 or removed2 or changed2:
        print("FEL: Intern slutkontroll misslyckades.", file=sys.stderr)
        return 1
    print(
        f"OK: skapade revision {new_revision} från {old_revision} i {storage['mode']}-läge. "
        f"Ändrade: {', '.join(final_changes)}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit_parser = subparsers.add_parser("audit-legacy")
    audit_parser.add_argument("source_zip")
    audit_parser.add_argument("--output")
    audit_parser.set_defaults(func=cmd_audit_legacy)
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("root")
    init_parser.add_argument("--slug", required=True)
    init_parser.add_argument("--project-id")
    init_parser.add_argument("--revision", type=int, default=0)
    init_parser.add_argument("--zip-name")
    init_parser.add_argument("--source-zip-name")
    init_parser.add_argument("--operation", default="Projektets integritetsmanifest skapades")
    init_parser.add_argument("--legacy-migration", action="store_true")
    init_parser.add_argument("--legacy-audit")
    init_parser.add_argument("--storage-mode", choices=sorted(STORAGE_MODES), default="zip")
    init_parser.add_argument("--repository")
    init_parser.add_argument("--base-branch")
    init_parser.add_argument("--working-branch")
    init_parser.set_defaults(func=cmd_init)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("root")
    verify_parser.set_defaults(func=cmd_verify)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("root")
    status_parser.set_defaults(func=cmd_status)
    commit_parser = subparsers.add_parser("commit")
    commit_parser.add_argument("root")
    commit_parser.add_argument("--operation", required=True)
    commit_parser.add_argument("--zip-name")
    commit_parser.add_argument("--source-zip-name")
    commit_parser.add_argument("--storage-mode", choices=sorted(STORAGE_MODES))
    commit_parser.add_argument("--expected-revision", type=int)
    commit_parser.add_argument("--allow", action="append", required=True)
    commit_parser.set_defaults(func=cmd_commit)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.func(args))
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"FEL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `publishing/metadata.yaml`

```yaml
---
title: "[Titel]"
subtitle: "[Undertitel]"
author: "[Författare]"
lang: sv-SE
rights: "© [År] [Författare]"
publisher: ""
identifier: ""
cover-image: "omslag/cover.jpg"
toc-depth: 1
---
```

## `publishing/epub.css`

```css
/* Romanskaparen EPUB-standard v4 */
body {
  line-height: 1.45;
  margin: 0;
  padding: 0;
  widows: 2;
  orphans: 2;
}

/* Varje kapitel ligger normalt i en egen XHTML-fil. Lägg därför INTE
   page-break-before/break-before på kapitelrubriken i EPUB, eftersom
   TOC-länkar då kan öppna en tom sida före kapitlet i flera läsare. */
section.level1 > h1,
h1.chapter-heading,
h1 {
  text-align: center;
  font-weight: normal;
  line-height: 1.08;
  margin-top: 0.8em;
  margin-bottom: 0.35em;
  page-break-before: auto;
  break-before: auto;
}

.chapter-number {
  display: block;
  text-align: center;
  font-size: 1.45em;
  letter-spacing: 0.06em;
  line-height: 1.05;
  margin: 0 0 0.08em 0;
  font-weight: normal;
}

.chapter-title,
.chapter-name {
  display: block;
  text-align: center;
  font-size: 1.30em;
  line-height: 1.12;
  margin: 0 0 0.20em 0;
  font-weight: normal;
}

.titlepage {
  text-align: center;
  margin-top: 25vh;
}

.titlepage h1,
.titlepage .subtitle,
.titlepage .author,
.book-title,
.book-subtitle,
.book-author {
  text-align: center;
  text-indent: 0;
}

p {
  margin: 0 0 0.8em 0;
  text-indent: 0;
}

hr {
  border: 0;
  text-align: center;
  margin: 1.2em 0;
}

hr::after {
  content: "* * *";
  letter-spacing: 0.4em;
}
```

## `publishing/pdf-template.tex`

```latex
% Romanskaparen PDF-standard för Pandoc/LaTeX.
% Målet är en kompakt kapitelstart: nummer centrerat på första raden,
% rubrik centrerad på andra raden, och TOC-post i formen "1. Kapitelrubrik".

\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{longtable}
\usepackage{array}
\usepackage{booktabs}
\usepackage{tabularx}

\titleformat{\chapter}[display]
  {\normalfont\huge\filcenter}
  {\thechapter}
  {0.25em}
  {\Huge}
\titlespacing*{\chapter}{0pt}{1.5em}{1.0em}

\setcounter{tocdepth}{1}
\hypersetup{hidelinks}
```

## `publishing/build-notes.md`

```markdown
# Build-notes

## Standard
- Källformat: Markdown i `kapitel/`.
- Exportverktyg: Pandoc i första hand.
- EPUB: navigerbar TOC ska finnas i EPUB-läsarens index. `nav.xhtml` ska inte visas som vanlig sida i bokflödet om användaren inte uttryckligen ber om synlig innehållsförteckning; använd helst `linear="no"` för nav-spineposten.
- PDF: klickbar TOC om användaren ber om synlig innehållsförteckning.
- Kapitelstart: nummer och rubrik på två centrerade rader med kompakt spacing.
- TOC-post: `1. Kapitelrubrik`.
- Kapitelnoteringar exporteras inte.

## EPUB-kontroll efter Pandoc
Efter att EPUB skapats ska paketet kontrolleras eller efterbearbetas:
1. `nav.xhtml` ska finnas kvar som navigeringsdokument så EPUB-läsaren visar innehållsförteckning/index. Om `EPUB/content.opf` har nav i `<spine>` ska itemref normalt vara `linear="no"` så sidan inte visas i läsflödet.
2. Kapitelrubriker i EPUB-CSS får inte använda `page-break-before: always` eller `break-before: page`; varje kapitel är redan en egen XHTML-fil. Annars kan TOC-länkar öppna en tom sida före kapitlet.
3. Kapitelrubriken ska vara större än brödtext men kompakt: ungefär `.chapter-number font-size:1.45em`, `.chapter-title font-size:1.30em`, `h1 margin-top:0.8em`, `h1 margin-bottom:0.35em`, `.chapter-number margin-bottom:0.08em`.

## Senaste export
- Datum:
- Format:
- Kommando/metod:
- Kommentar:
```

## `publishing/fix-epub-after-pandoc.py`

```python
#!/usr/bin/env python3
"""Efterbearbetar en Pandoc-EPUB enligt Romanskaparens standard v4.

Mål:
1. Behåll den navigerbara EPUB-TOC:en/nav.xhtml som index i läsaren.
2. Visa inte nav.xhtml som en vanlig innehållsförteckningssida i bokflödet.
3. Neutralisera CSS-regler som kan skapa tom sida före kapitelrubriken.

Viktigt: Ta normalt inte bort nav-itemref helt. Sätt hellre linear="no" för
bättre kompatibilitet med EPUB-läsare som förväntar sig nav i spine men inte
ska visa den i den linjära läsordningen.
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


def find_nav_ids(opf_text: str) -> set[str]:
    ids: set[str] = set()
    item_re = re.compile(r"<item\b[^>]*>", re.IGNORECASE)
    id_re = re.compile(r'\bid=["\']([^"\']+)["\']', re.IGNORECASE)
    prop_re = re.compile(r'\bproperties=["\'][^"\']*\bnav\b[^"\']*["\']', re.IGNORECASE)
    href_nav_re = re.compile(r'\bhref=["\'][^"\']*(?:nav|toc)[^"\']*\.xhtml["\']', re.IGNORECASE)
    for m in item_re.finditer(opf_text):
        item = m.group(0)
        if prop_re.search(item) or href_nav_re.search(item):
            id_m = id_re.search(item)
            if id_m:
                ids.add(id_m.group(1))
    if not ids:
        ids.add("nav")
    return ids


def hide_nav_in_spine(opf_text: str) -> str:
    nav_ids = find_nav_ids(opf_text)
    for nav_id in nav_ids:
        # itemref self-closing without linear: add linear="no"
        opf_text = re.sub(
            rf'(<itemref\b(?=[^>]*\bidref=["\']{re.escape(nav_id)}["\'])(?![^>]*\blinear=)[^>]*)/?>',
            lambda m: m.group(1).rstrip().rstrip('/') + ' linear="no"/>',
            opf_text,
            flags=re.IGNORECASE,
        )
        # itemref with linear yes/true: change to no
        opf_text = re.sub(
            rf'(<itemref\b(?=[^>]*\bidref=["\']{re.escape(nav_id)}["\'])[^>]*\blinear=)["\'](?:yes|true|1)["\']',
            r'\1"no"',
            opf_text,
            flags=re.IGNORECASE,
        )
    return opf_text


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: fix-epub-after-pandoc.py input.epub [output.epub]")
        return 2

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) == 3 else src
    if not src.exists():
        print(f"Missing file: {src}")
        return 2

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        with zipfile.ZipFile(src) as zf:
            zf.extractall(tmp)

        for opf in tmp.rglob("*.opf"):
            text = opf.read_text(encoding="utf-8")
            text = hide_nav_in_spine(text)
            opf.write_text(text, encoding="utf-8")

        for css in tmp.rglob("*.css"):
            text = css.read_text(encoding="utf-8")
            text = text.replace("page-break-before: always;", "page-break-before: auto;")
            text = text.replace("break-before: page;", "break-before: auto;")
            css.write_text(text, encoding="utf-8")

        out = dst
        if out == src:
            backup = src.with_suffix(src.suffix + ".bak")
            shutil.copy2(src, backup)
        if out.exists():
            out.unlink()
        with zipfile.ZipFile(out, "w") as zf:
            mimetype = tmp / "mimetype"
            if mimetype.exists():
                zf.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
            for path in sorted(tmp.rglob("*")):
                if path.is_file() and path.name != "mimetype":
                    zf.write(path, path.relative_to(tmp).as_posix(), compress_type=zipfile.ZIP_DEFLATED)

    print(f"Fixed EPUB: {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `exports/README.md`

```markdown
# Exporter

Denna katalog innehåller metadata om genererade exporter, till exempel EPUB och PDF.

Exporter är inte romanens kanoniska källtext. De kan återskapas från `kapitel/kapitel-XX.md`.

EPUB- och PDF-filer behöver normalt inte ligga i projektzipen. När användaren begär export kan de ges som separata nedladdningsfiler.

Före export ska underlaget normaliseras så att rubriker, listor, fetstil, kursiv stil och andra markdown-strukturer renderas korrekt och att råa markdown-markörer inte lämnas kvar synliga i slutdokumentet.

Layout och metadata styrs i `publishing/`. Exporter ska kunna återskapas från kapitelfilerna och publiceringsfilerna.
```

## `exports/exportlogg.md`

```markdown
# Exportlogg

| Datum | Format | Filnamn | Inkluderade kapitel | Titel | Författare | Kommentar |
|---|---|---|---|---|---|---|
```
## Obligatoriskt lagringsbeteende

- Välj och lås exakt en kanonisk projektkälla per operation.
- Kör `verify` före ändring.
- Använd förväntad revision och strikt `--allow`-lista vid intern commit.
- Vid nytt kapitel får inga befintliga kapitelfiler ändras.
- Vid revision av ett kapitel får inga andra kapitelfiler ändras.
- ZIP-läge: paketera, återöppna och verifiera leverans-ZIP:en.
- GitHub-läge: kontrollera branch-head igen före publicering, använd aldrig force push och skapa eller återanvänd PR mot default branch.
- Leverera en lagringsanpassad revisionskvittens.
