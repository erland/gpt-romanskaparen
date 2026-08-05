# Bygg och validering av Romanskaparen-distributioner

`core/` är den kanoniska källan. Filer under `distributions/gpt/` och `distributions/project/` är genererade eller plattformsanpassade distributionsartefakter.

## Lokal byggning

```bash
python3 scripts/build_distributions.py
python3 scripts/validate_distributions.py
```

Alternativt:

```bash
bash scripts/build.sh
```

## Kontroll utan ändring

```bash
python3 scripts/build_distributions.py --check
bash scripts/validate.sh
```

Kontrollen misslyckas om knowledge-filer, bundle-filer eller distributionsmanifest inte motsvarar kärnan.

## Vad som genereras

- `core/knowledge/*.md` synkas byte-identiskt till båda distributionernas `knowledge/`.
- `core/prompts/default-starters.md` synkas till GPT-distributionens conversation starters.
- `core/templates/romanprojekt/` byggs deterministiskt till båda distributionernas `project-template-bundle.md`.
- distributionsmanifest normaliseras och markeras som genererade.

Plattformsspecifika instruktioner och installationsfiler underhålls separat eftersom de är tunna wrappers, inte kopior av kärninstruktionen.

## Valideringar

Validatorn kontrollerar bland annat:

- att båda distributionerna har exakt samma knowledge-filer som kärnan
- att knowledge-innehållet är byte-identiskt
- att båda bundle-filerna är aktuella och identiska
- att GPT-instruktionen håller distributionsmanifestets teckengräns
- att knowledge-filantalet håller angiven gräns
- att deklarerat och faktiskt knowledge-filantal överensstämmer
- att distributionsmanifest är markerade som genererade

## GitHub Actions

`sync-distributions.yml` bygger, validerar och committar genererade distributionsändringar på `romanskaparen-2.0` när kärnan eller byggskripten ändras.

`validate-distributions.yml` kör valideringen på push och pull requests. Det gör att manuellt redigerade eller stale distributionsartefakter upptäcks innan merge.
