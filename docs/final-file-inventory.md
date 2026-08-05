# Romanskaparen 2.0 – slutlig filinventering

Status: Prompt 7

## Aktiv produktstruktur

```text
README.md
SETUP.md

core/
  instructions/
    romanskaparen-core.md
  knowledge/
    01-arbetsflode-och-nyborjarstod.md
    02-berattelsehantverk.md
    03-karaktarer-varld-och-kontinuitet.md
    04-genreguider.md
    05-projektstruktur-och-synk.md
    06-verktyg-och-lagringskapaciteter.md
  prompts/
    default-starters.md
  templates/
    romanprojekt/

distributions/
  gpt/
    README.md
    INSTALL.md
    instructions.md
    conversation-starters.md
    distribution-manifest.json
    knowledge/
    project-template-bundle.md
  project/
    README.md
    INSTALL.md
    PROJECT-INSTRUCTIONS.md
    START-HERE.md
    distribution-manifest.json
    knowledge/
    project-template-bundle.md

scripts/
  build.sh
  validate.sh
  build_distributions.py
  build_project_template_bundle.py
  validate_distributions.py

.github/workflows/
  sync-distributions.yml
  validate-distributions.yml

docs/
  architecture.md
  build-and-validation.md
  chatgpt-project-edition.md
  custom-gpt-edition.md
  file-movement-matrix.md
  implementation-validation.md
  migration-from-1.x.md
  romanskaparen-2.0-plan.md
  test-plan.md
  final-file-inventory.md
  archive/README.md
```

## Kanoniska och genererade filer

### Kanoniska

- allt under `core/`
- plattformsspecifika wrapper- och installationsfiler i respektive distribution
- bygg- och valideringsscripts
- dokumentationen

### Genererade

- `distributions/gpt/knowledge/*.md`
- `distributions/project/knowledge/*.md`
- båda `project-template-bundle.md`
- normaliserade delar av båda `distribution-manifest.json`
- GPT-distributionens `conversation-starters.md`

Genererade filer ska inte ändras manuellt. Ändra kärnan och kör byggsystemet.

## Custom GPT-uppladdning

Följande sju filer används som Knowledge:

```text
distributions/gpt/knowledge/01-arbetsflode-och-nyborjarstod.md
distributions/gpt/knowledge/02-berattelsehantverk.md
distributions/gpt/knowledge/03-karaktarer-varld-och-kontinuitet.md
distributions/gpt/knowledge/04-genreguider.md
distributions/gpt/knowledge/05-projektstruktur-och-synk.md
distributions/gpt/knowledge/06-verktyg-och-lagringskapaciteter.md
distributions/gpt/project-template-bundle.md
```

Instruktionen hämtas separat från `distributions/gpt/instructions.md`.

## ChatGPT Project-uppladdning

Följande sju filer används som projektunderlag:

```text
distributions/project/knowledge/01-arbetsflode-och-nyborjarstod.md
distributions/project/knowledge/02-berattelsehantverk.md
distributions/project/knowledge/03-karaktarer-varld-och-kontinuitet.md
distributions/project/knowledge/04-genreguider.md
distributions/project/knowledge/05-projektstruktur-och-synk.md
distributions/project/knowledge/06-verktyg-och-lagringskapaciteter.md
distributions/project/project-template-bundle.md
```

Projektinstruktionen hämtas separat från `distributions/project/PROJECT-INSTRUCTIONS.md`.

## Borttagna aktiva 1.x-källor

Följande finns inte längre som aktiva parallella källor i roten:

- `gpt-instructions.md`
- `conversation-starters.md`
- `knowledge-upload/`
- `templates/`
- `project-template-bundle.md`
- äldre jämförelse- och förändringsdokument

De finns kvar i Git-historiken vid den dokumenterade 1.x-bascommitten.
