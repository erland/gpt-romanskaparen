# Romanskaparen 2.0 – arkitekturspecifikation

Status: låst målarkitektur för Prompt 1  
Branch: `romanskaparen-2.0`  
Bas: `main` vid commit `2bfe0c882d7d4a510aededb23f71a2302af20b5a`

## 1. Syfte

Romanskaparen 2.0 ska organiseras som en plattformsoberoende produktkärna med tunna distributioner. Custom GPT, ChatGPT Project och vanlig konversation är körmiljöer för samma Romanskapare, inte separata produkter.

Kärnan ska äga alla regler för:

- berättelseutveckling
- kapitelarbete och revision
- kontinuitet
- romanprojektets filstruktur
- ZIP-baserad versionssäkerhet
- projektmanifest, revisioner och hashkontroll
- legacy-migrering och reparation
- EPUB/PDF-export
- kapacitetsbaserad användning av tillgängliga verktyg

Distributionerna ska endast anpassa installation, instruktionstext, onboarding och filpaketering till respektive ChatGPT-miljö.

## 2. Låsta arkitekturprinciper

### 2.1 En kanonisk kärna

All aktiv produktlogik ska ha exakt en kanonisk källa under `core/`. En distributionsfil får duplicera kärninnehåll endast som en byggd eller tydligt härledd artefakt.

### 2.2 ZIP är obligatorisk baskapacitet

När filverktyg finns ska både GPT Edition och Project Edition kunna genomföra hela romanarbetsflödet med ZIP utan externa anslutningar.

### 2.3 Externa anslutningar är villkorliga

GitHub och andra externa lagringssystem får användas endast när aktuell miljö har verifierad användarspecifik läs-, skriv- och återläsningsförmåga.

### 2.4 Ett ChatGPT Project per roman

Project Edition rekommenderar ett separat ChatGPT Project för varje roman. ChatGPT-projektets minne och chattar ersätter aldrig romanprojektets manifest, revisionslogg eller kanoniska filer.

### 2.5 Ett romanprojekt per repository

När GitHub används bör repositoryt innehålla högst en roman. Repositoryt är kanonisk källa endast efter uttrycklig migration och godkänt förmågetest.

### 2.6 Tunna distributioner

`distributions/gpt/` och `distributions/project/` ska innehålla plattformsanpassade wrappers och byggda kopior av kärnans knowledge och projektbundle. Prompt 5 automatiserar genereringen och valideringen.

## 3. Slutlig katalogstruktur

```text
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
  templates/
    romanprojekt/
  prompts/
    default-starters.md

distributions/
  gpt/
    README.md
    INSTALL.md
    instructions.md
    conversation-starters.md
    knowledge/
    project-template-bundle.md
    distribution-manifest.json
  project/
    README.md
    INSTALL.md
    PROJECT-INSTRUCTIONS.md
    START-HERE.md
    knowledge/
    project-template-bundle.md
    distribution-manifest.json
  conversation/
    README.md
    START-PROMPT.md
    ATTACHMENTS.md

scripts/
  build_project_template_bundle.py
  build_distributions.py
  validate_distributions.py

docs/
  architecture.md
  custom-gpt-edition.md
  chatgpt-project-edition.md
  migration-from-1.x.md
  test-plan.md
  implementation-validation.md
```

## 4. Ansvarsfördelning

### `core/instructions/`

Äger identitet, övergripande beteende, absoluta källregler, revisionsskydd, kapitelarbete, exportprinciper och svarsstil.

### `core/knowledge/01–04`

Äger skrivprocess, berättelsehantverk, karaktärer, värld, kontinuitet och genreanpassning.

### `core/knowledge/05`

Äger ZIP-baserad projektstruktur, manifest, revisioner, hashkontroll, legacy-migrering, transaktioner, synk och export.

### `core/knowledge/06`

Äger kapacitetskontroll, villkorliga anslutningar, användarisolering, read-only-fall, lagringsbyte och avbrottsregler.

### `core/templates/romanprojekt/`

Äger det faktiska romanprojektformatet och integritetsverktyget. Befintligt 1.x-format bevaras initialt byte-identiskt för bakåtkompatibilitet.

### `distributions/gpt/`

Äger endast GPT Builder-installation, kompakt instruktion, starters och byggda knowledge-/bundle-artefakter. ZIP är garanterat; extern lagring är villkorlig.

### `distributions/project/`

Äger installation och onboarding för ett ChatGPT Project per roman. Flera chattar kan användas, men en gemensam kanonisk romanprojektkälla måste alltid väljas.

## 5. Bakåtkompatibilitet

Romanskaparen 2.0 ska fortsätta acceptera:

- verifierbara moderna 1.x-projekt utan formatmigrering
- äldre manifestlösa ZIP-projekt via befintligt `audit-legacy`-flöde
- nuvarande schema 1 och `project_integrity.py` under den första 2.0-versionen

Repositoryomstruktureringen får inte i sig ändra romanprojektets interna format, `project_id`, revision eller filhashar.

## 6. Genererade artefakter

Följande ska i slutläget betraktas som byggprodukter:

- `distributions/gpt/knowledge/*`
- `distributions/project/knowledge/*`
- båda distributionernas `project-template-bundle.md`
- plattformsanpassade instruktioner i den utsträckning de kan genereras deterministiskt
- distributionsmanifest

Prompt 3 skapar en första granskad GPT-distributionssnapshot. Prompt 5 ersätter manuellt underhåll med reproducerbar byggning och kontroll.

## 7. Övergångsregler

Gamla rotfiler och 1.x-kataloger lämnas kvar tills:

1. kärnan finns
2. GPT Edition finns
3. Project Edition finns
4. distributionerna kan byggas och valideras
5. dokumentationen är uppdaterad
6. inga aktiva sökvägar pekar på gamla filer

Historiska filer arkiveras i Prompt 6 och aktiva 1.x-filer kan då ersättas av produktöversikt eller kompatibilitetshänvisningar.

## 8. Genomförandestatus

- Prompt 1: klar
- Prompt 2: klar
- Prompt 3: klar
- Prompt 4–7: återstår

Arkitekturen ska inte ändras genom distributionsspecifika specialregler utan att detta dokument uppdateras uttryckligen.
