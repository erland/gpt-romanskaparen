# Romanskaparen 2.0 – filflyttningsmatris

Status: beslutad destination per nuvarande fil  
Princip: inga stora flyttar genomförs i Prompt 1

## Teckenförklaring

- **Flytta** – blir kanonisk fil på ny plats.
- **Generera** – skapas från kanoniska kärnfiler.
- **Plattformsanpassa** – skrivs som tunn distributionsfil.
- **Arkivera** – historiskt värde men inte aktiv regelkälla.
- **Ersätt** – rotfilen ersätts senare av ny dokumentation eller hänvisning.

## Rotfiler

| Nuvarande fil | Klass | Destination | Åtgärd | Motivering |
|---|---|---|---|---|
| `README.md` | GPT-dokumentation | `README.md` | Ersätt | Ny produktöversikt ska presentera Core, GPT och Project. |
| `SETUP.md` | GPT-installation | `distributions/gpt/INSTALL.md` | Plattformsanpassa | Setup gäller GPT Builder och ska inte ligga som generell rotmanual. |
| `gpt-instructions.md` | Blandad kärna/GPT | `core/instructions/romanskaparen-core.md` + `distributions/gpt/instructions.md` | Dela upp | Kärnregler separeras från Builder-wrapper. |
| `conversation-starters.md` | GPT-distribution | `core/prompts/default-starters.md` och `distributions/gpt/conversation-starters.md` | Flytta/generera | Grundstarter ägs av kärnan; GPT-format genereras. |
| `project-template-bundle.md` | Genererad artefakt | `distributions/gpt/project-template-bundle.md` och `distributions/project/project-template-bundle.md` | Generera | Ska byggas från `core/templates/romanprojekt/`. |
| `ANDRINGAR-FILSAKER-VERSION.md` | Historik | `docs/archive/ANDRINGAR-FILSAKER-VERSION.md` | Arkivera | Viktig bakgrund men inte aktiv instruktion. |
| `JAMFORELSE-MED-URSPRUNGSINSTRUKTION.md` | Historik | `docs/archive/JAMFORELSE-MED-URSPRUNGSINSTRUKTION.md` | Arkivera | Jämförelsedokument för 1.x. |

## Knowledge-filer

| Nuvarande fil | Klass | Destination | Åtgärd |
|---|---|---|---|
| `knowledge-upload/01-arbetsflode-och-nyborjarstod.md` | Kärna | `core/knowledge/01-arbetsflode-och-nyborjarstod.md` | Flytta och plattformsneutralisera |
| `knowledge-upload/02-berattelsehantverk.md` | Kärna | `core/knowledge/02-berattelsehantverk.md` | Flytta |
| `knowledge-upload/03-karaktarer-varld-och-kontinuitet.md` | Kärna | `core/knowledge/03-karaktarer-varld-och-kontinuitet.md` | Flytta |
| `knowledge-upload/04-genreguider.md` | Kärna | `core/knowledge/04-genreguider.md` | Flytta |
| `knowledge-upload/05-projektstruktur-och-synk.md` | Kärna | `core/knowledge/05-projektstruktur-och-synk.md` | Flytta och renodla ZIP/integritet |
| Ny fil | Kärna | `core/knowledge/06-verktyg-och-lagringskapaciteter.md` | Skapa i Prompt 2 |

`distributions/gpt/knowledge/` och `distributions/project/knowledge/` ska genereras från `core/knowledge/`. De är inte manuella källor.

## Dokumentation

| Nuvarande fil | Klass | Destination | Åtgärd |
|---|---|---|---|
| `docs/romanskaparen-2.0-plan.md` | Genomförandeplan | Samma plats | Behåll |
| `docs/architecture.md` | Arkitektur | Samma plats | Skapad i Prompt 1 |
| `docs/migration-from-1.x.md` | Migration | Samma plats | Första utkast i Prompt 1, färdigställ i Prompt 6 |
| `docs/file-movement-matrix.md` | Arkitekturunderlag | Samma plats | Skapad i Prompt 1 |

## Projektmall – rot

Alla följande filer blir kanoniska under `core/templates/romanprojekt/` med samma relativa sökväg.

| Nuvarande fil | Destination | Åtgärd |
|---|---|---|
| `templates/romanprojekt/README.md` | `core/templates/romanprojekt/README.md` | Flytta |
| `templates/romanprojekt/arbetslogg.md` | `core/templates/romanprojekt/arbetslogg.md` | Flytta |
| `templates/romanprojekt/kapitelnoteringar.md` | `core/templates/romanprojekt/kapitelnoteringar.md` | Flytta |
| `templates/romanprojekt/kapitelplan.md` | `core/templates/romanprojekt/kapitelplan.md` | Flytta |
| `templates/romanprojekt/kontinuitetsanteckningar.md` | `core/templates/romanprojekt/kontinuitetsanteckningar.md` | Flytta |
| `templates/romanprojekt/project-index.md` | `core/templates/romanprojekt/project-index.md` | Flytta |
| `templates/romanprojekt/project-manifest.json` | `core/templates/romanprojekt/project-manifest.json` | Flytta byte-identiskt i första steg |
| `templates/romanprojekt/projektstatus.md` | `core/templates/romanprojekt/projektstatus.md` | Flytta |
| `templates/romanprojekt/revision-log.md` | `core/templates/romanprojekt/revision-log.md` | Flytta |
| `templates/romanprojekt/revisionsonskemal.md` | `core/templates/romanprojekt/revisionsonskemal.md` | Flytta |
| `templates/romanprojekt/roman-bibel.md` | `core/templates/romanprojekt/roman-bibel.md` | Flytta |
| `templates/romanprojekt/stilguide.md` | `core/templates/romanprojekt/stilguide.md` | Flytta |
| `templates/romanprojekt/synopsis.md` | `core/templates/romanprojekt/synopsis.md` | Flytta |
| `templates/romanprojekt/tidslinje.md` | `core/templates/romanprojekt/tidslinje.md` | Flytta |

## Projektmall – kapitel och karaktärer

| Nuvarande fil | Destination | Åtgärd |
|---|---|---|
| `templates/romanprojekt/kapitel/kapitelmall.md` | `core/templates/romanprojekt/kapitel/kapitelmall.md` | Flytta |
| `templates/romanprojekt/karaktarer/huvudperson.md` | `core/templates/romanprojekt/karaktarer/huvudperson.md` | Flytta |
| `templates/romanprojekt/karaktarer/antagonist.md` | `core/templates/romanprojekt/karaktarer/antagonist.md` | Flytta |
| `templates/romanprojekt/karaktarer/bifigurer.md` | `core/templates/romanprojekt/karaktarer/bifigurer.md` | Flytta |

## Projektmall – exports

| Nuvarande fil | Destination | Åtgärd |
|---|---|---|
| `templates/romanprojekt/exports/README.md` | `core/templates/romanprojekt/exports/README.md` | Flytta |
| `templates/romanprojekt/exports/exportlogg.md` | `core/templates/romanprojekt/exports/exportlogg.md` | Flytta |

## Projektmall – publishing

| Nuvarande fil | Destination | Åtgärd |
|---|---|---|
| `templates/romanprojekt/publishing/build-notes.md` | `core/templates/romanprojekt/publishing/build-notes.md` | Flytta |
| `templates/romanprojekt/publishing/epub.css` | `core/templates/romanprojekt/publishing/epub.css` | Flytta |
| `templates/romanprojekt/publishing/fix-epub-after-pandoc.py` | `core/templates/romanprojekt/publishing/fix-epub-after-pandoc.py` | Flytta, behåll körbarhet |
| `templates/romanprojekt/publishing/metadata.yaml` | `core/templates/romanprojekt/publishing/metadata.yaml` | Flytta |
| `templates/romanprojekt/publishing/pdf-template.tex` | `core/templates/romanprojekt/publishing/pdf-template.tex` | Flytta |

## Projektmall – integritetsverktyg

| Nuvarande fil | Destination | Åtgärd |
|---|---|---|
| `templates/romanprojekt/scripts/project_integrity.py` | `core/templates/romanprojekt/scripts/project_integrity.py` | Flytta byte-identiskt i Prompt 2 |

Integritetsverktyget ska inte flyttas till repositoryts globala `scripts/`, eftersom det är en del av varje genererat romanprojekt. Globala bygg- och valideringsscripts ligger separat under rotens `scripts/`.

## Nya distributionsfiler

Följande har ingen 1.x-motsvarighet och skapas senare:

### GPT Edition

- `distributions/gpt/README.md`
- `distributions/gpt/INSTALL.md`
- `distributions/gpt/instructions.md`
- `distributions/gpt/conversation-starters.md`
- `distributions/gpt/knowledge/*`
- `distributions/gpt/project-template-bundle.md`
- `distributions/gpt/distribution-manifest.json`

### Project Edition

- `distributions/project/README.md`
- `distributions/project/INSTALL.md`
- `distributions/project/PROJECT-INSTRUCTIONS.md`
- `distributions/project/START-HERE.md`
- `distributions/project/knowledge/*`
- `distributions/project/project-template-bundle.md`
- `distributions/project/distribution-manifest.json`

### Conversation Edition

- `distributions/conversation/README.md`
- `distributions/conversation/START-PROMPT.md`
- `distributions/conversation/ATTACHMENTS.md`

### Bygg och validering

- `scripts/build_project_template_bundle.py`
- `scripts/build_distributions.py`
- `scripts/validate_distributions.py`

## Borttagningsregler

Ingen nuvarande aktiv fil tas bort i Prompt 2 innan en fungerande ersättare finns.

Gamla filer får tas bort eller ersättas först när:

1. kärnan finns
2. båda huvuddistributionerna har byggts
3. bundle och knowledge har validerats
4. GPT-instruktionen håller storleksgränsen
5. Project Edition har en komplett installationsväg
6. inga aktiva dokument refererar till gamla sökvägar

## Sammanfattning

Varje nuvarande fil har nu en beslutad destination eller arkiveringsmotivering. Projektmallen flyttas relativt oförändrad. Knowledge och instruktion separeras i kärna respektive distribution. Bundlen upphör att vara manuell källa och blir en byggprodukt.
