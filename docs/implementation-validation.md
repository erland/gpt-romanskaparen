# Romanskaparen 2.0 – implementeringsvalidering

Status: slutlig repositoryvalidering för Prompt 7

## Sammanfattning

Romanskaparen 2.0 har en plattformsoberoende kärna, två installationbara distributioner och ett automatiserat bygg- och valideringsflöde. Repositorystrukturen är konsekvent och redo för praktiska accepteranstester i ChatGPT.

## Verifierade delar

### Kärna

- `core/instructions/romanskaparen-core.md` är plattformsoberoende.
- `core/knowledge/` innehåller sex bindande manualer.
- `core/templates/romanprojekt/` är kanonisk projektmall.
- `core/prompts/default-starters.md` är kanonisk källa för standardstarter.

### Custom GPT Edition

- finns under `distributions/gpt/`
- använder en kompakt GPT Builder-instruktion
- använder sex knowledge-filer och en projektbundle, totalt sju knowledge-filer
- ZIP är fullständig filbaserad fallback
- externa lagringsformer är villkorliga

### ChatGPT Project Edition

- finns under `distributions/project/`
- är avsedd för ett separat ChatGPT Project per roman
- innehåller projektinstruktion, installationsguide och onboarding
- använder samma knowledge-underlag och bundle som GPT Edition
- Project Memory ersätter inte kanoniska projektfiler

### Byggning och validering

Följande är implementerat:

```text
scripts/build_project_template_bundle.py
scripts/build_distributions.py
scripts/validate_distributions.py
scripts/build.sh
scripts/validate.sh
.github/workflows/sync-distributions.yml
.github/workflows/validate-distributions.yml
```

GitHub Actions har framgångsrikt:

- byggt om de genererade distributionerna
- validerat det genererade resultatet
- committat den deterministiska regenereringen
- kört slutlig distributionsvalidering efter dokumentations- och 1.x-städningen

## Konsistenskontroll

Följande relationer är verifierade av validatorn:

- distributionsknowledge motsvarar kärnknowledge
- GPT- och Project-bundles är identiska
- bundle-innehållet motsvarar kärnmallen
- distributionsmanifesten är genererade och aktuella
- deklarerat knowledge-filantal motsvarar faktiskt antal
- GPT-instruktionen håller den angivna storleksgränsen

## Bakåtkompatibilitet

Romanskaparen 2.0 förändrar distributionen, inte formatet för ett fungerande romanprojekt. Befintliga verifierbara projekt kan fortsätta med samma:

- `project_id`
- revision och `parent_revision`
- kapitelstruktur och filnamn
- fil- och kapitelhashar
- revisionslogg
- projekt- och publiceringsmetadata

Manifestlösa äldre projekt följer legacy-migrering. Ett modernt projekt med trasigt manifest ska fortfarande stoppas och behandlas som reparationsfall.

## 1.x-städning

Aktiva 1.x-kopior har tagits bort från repositoryts rot. Historiken finns kvar i Git och dokumenteras i `docs/archive/README.md`. Detta förhindrar att två parallella regeluppsättningar vidareutvecklas.

## Kvarstående begränsningar

Följande kan inte slutgiltigt bevisas enbart genom repository- och CI-validering:

1. faktisk installation och beteende i GPT Builder
2. faktisk installation och beteende i ChatGPT Projects
3. aktuella plattformsgränser och tillgång till externa appar
4. full EPUB/PDF-rendering i varje tillgänglig körmiljö
5. användarspecifik GitHub-läsning och skrivning, som beror på den aktuella ChatGPT-miljön

Därför ska externa anslutningar alltid kapacitetstestas och ZIP vara fallback.

## Rekommenderade manuella accepteranstester

Följ `docs/test-plan.md`. Prioritera:

1. ny Custom GPT med ett litet ZIP-projekt
2. fortsättning och riktad kapitelrevision
3. legacy- och trasigt-manifest-fall
4. EPUB/PDF-export
5. ett separat ChatGPT Project per roman
6. användarspecifikt kapacitetstest för eventuell extern lagring

## Slutbedömning

Repositoryimplementationen är redo för merge efter praktiskt grundtest eller för en PR där de praktiska testerna dokumenteras under granskningen. Inga kända strukturella blockerare återstår.
