# Romanskaparen 2.0 – omstruktureringsplan

Status: plan för genomförande  
Källbranch: `main`  
Arbetsbranch: `romanskaparen-2.0`  
Källcommit: `2bfe0c882d7d4a510aededb23f71a2302af20b5a`

## 1. Målbild

Romanskaparen ska inte längre vara organiserad som ett repository enbart för en Custom GPT. Repositoryt ska i stället innehålla en gemensam produktkärna och separata distributionspaket för olika ChatGPT-användningsformer.

Första versionen av 2.0 ska stödja:

1. **Custom GPT Edition** – ZIP-baserat romanarbete med GPT Builder-instruktion och knowledge-filer.
2. **ChatGPT Project Edition** – ett ChatGPT Project per roman, med projektinstruktioner, gemensamma underlagsfiler och möjlighet att använda användarens vanliga anslutna verktyg i projektchatten.
3. **Vanlig konversation** – ett enklare manuellt läge där samma instruktioner och underlag kan bifogas i en vanlig chatt, utan garanti för beständig projektkontext.

Kärnreglerna för berättelsearbete, projektstruktur, ZIP-revisioner, integritet, kontinuitet och export ska vara gemensamma. Plattformsspecifika skillnader ska ligga i distributionslagret.

## 2. Arkitekturprinciper

### 2.1 En gemensam kärna

Allt innehåll som beskriver vad Romanskaparen är och hur romanprojekt hanteras ska ha en kanonisk källa under `core/`.

### 2.2 Tunna distributioner

`distributions/gpt/` och `distributions/project/` ska huvudsakligen bestå av genererade eller tunna plattformsanpassningar. Samma regler ska inte underhållas manuellt på flera ställen.

### 2.3 ZIP är obligatorisk baskapacitet

Custom GPT Edition ska fungera fullt ut med ZIP-filer utan GitHub-beroende.

### 2.4 GitHub är en tillgänglig verktygskapacitet, inte ett krav

Project Edition får använda GitHub när användarens vanliga ChatGPT-projektchatt faktiskt har tillgång till en GitHub-anslutning med nödvändiga rättigheter. Saknas den kapaciteten ska ZIP-läget fortfarande fungera.

### 2.5 Ett ChatGPT Project per roman

Project Edition ska rekommendera ett separat ChatGPT Project för varje roman. Det isolerar projektinstruktioner, chattar, källfiler, romanunderlag och eventuell repositorykoppling.

### 2.6 Genererade distributionsartefakter

Bundle-, instruktion- och installationsfiler ska så långt möjligt genereras från kärnfiler och valideras med scripts, så att GPT Edition och Project Edition inte divergerar.

## 3. Föreslagen slutstruktur

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
  project/
    README.md
    INSTALL.md
    PROJECT-INSTRUCTIONS.md
    START-HERE.md
    knowledge/
    project-template-bundle.md
  conversation/
    README.md
    START-PROMPT.md

scripts/
  build_distributions.py
  build_project_template_bundle.py
  validate_distributions.py

docs/
  architecture.md
  custom-gpt-edition.md
  chatgpt-project-edition.md
  migration-from-1.x.md
  test-plan.md
```

Den exakta strukturen får justeras under implementationen, men principen med `core/` och tunna `distributions/` ska behållas.

## 4. Indelning i promptar och steg

Varje steg ska genomföras som en separat, granskningsbar commitserie på `romanskaparen-2.0`. Ingen PR mot `main` bör öppnas förrän minst steg 1–4 är konsistenta; därefter kan samma PR uppdateras genom resterande steg.

---

## Prompt 1 – Inventering och målarkitektur

Status: **Genomförd**

### Uppdrag

Inventera hela nuvarande repositoryt och skapa den slutliga arkitekturspecifikationen för Romanskaparen 2.0.

### Leverabler

- `docs/architecture.md`
- `docs/migration-from-1.x.md` som första utkast
- `docs/file-movement-matrix.md`

---

## Prompt 2 – Skapa Romanskaparen Core

Status: **Genomförd**

### Leverabler

- `core/instructions/romanskaparen-core.md`
- `core/knowledge/01–06`
- `core/templates/romanprojekt/`
- `core/prompts/default-starters.md`

---

## Prompt 3 – Custom GPT Edition

Status: **Genomförd**

### Leverabler

- `distributions/gpt/instructions.md`
- `distributions/gpt/conversation-starters.md`
- `distributions/gpt/knowledge/`
- `distributions/gpt/project-template-bundle.md`
- `distributions/gpt/INSTALL.md`
- `distributions/gpt/README.md`
- `distributions/gpt/distribution-manifest.json`

### Resultat

- Instruktionen är kompakt och avsedd för GPT Builder.
- Distributionen använder sex knowledge-filer plus projektbundle, totalt sju knowledge-filer.
- ZIP-flödet fungerar utan externa anslutningar.
- GitHub och andra externa lagringsformer är uttryckligen villkorliga.
- Prompt 5 ska automatisera generering och validering så att distributionsartefakterna inte behöver underhållas manuellt.

---

## Prompt 4 – ChatGPT Project Edition

### Uppdrag

Skapa en distribution avsedd för ett separat ChatGPT Project per roman.

### Ska omfatta

- skapa `distributions/project/`
- skapa `PROJECT-INSTRUCTIONS.md` anpassad för Project Instructions
- skapa `START-HERE.md` som första prompt och onboarding
- skapa installationsguide för att skapa ett projekt per roman
- beskriva hur flera chattar kan användas för planering, kapitel, redaktion och export
- beskriva vilka underlagsfiler som ska laddas upp till projektet
- formulera GitHub-stöd kapacitetsbaserat och användarspecifikt
- förklara att projektets egna romanprojektfiler eller repository är kanoniska, inte ChatGPT-projektets allmänna minne

### Rekommenderad användarmodell

```text
Ett ChatGPT Project = en roman
Ett romanrepository = högst en roman
Flera chattar får arbeta mot samma kanoniska romanprojekt
```

### Leverabler

- `distributions/project/PROJECT-INSTRUCTIONS.md`
- `distributions/project/START-HERE.md`
- `distributions/project/INSTALL.md`
- `distributions/project/README.md`
- `distributions/project/knowledge/`
- `distributions/project/project-template-bundle.md`

---

## Prompt 5 – Bygg- och valideringsscripts

### Uppdrag

Automatisera genereringen av distributionsfiler från kärnan och förhindra divergens.

### Leverabler

- `scripts/build_project_template_bundle.py`
- `scripts/build_distributions.py`
- `scripts/validate_distributions.py`
- dokumenterade bygg- och valideringskommandon

---

## Prompt 6 – Dokumentation och migrationsguide

### Uppdrag

Skriv om repositoryts publika dokumentation så att Romanskaparen presenteras som en produkt med flera distributionsformer.

### Leverabler

- ny `README.md`
- `docs/custom-gpt-edition.md`
- `docs/chatgpt-project-edition.md`
- färdig `docs/migration-from-1.x.md`
- eventuellt `docs/archive/`

---

## Prompt 7 – Slutlig konsistensgranskning och accepteranstest

### Uppdrag

Gör en fullständig kvalitetskontroll och testa båda distributionerna.

### Leverabler

- `docs/test-plan.md`
- `docs/implementation-validation.md`
- slutlig filinventering
- lista över kvarstående begränsningar

## 5. Rekommenderad PR-strategi

### Commitindelning

1. `Define Romanskaparen 2.0 architecture`
2. `Create platform-independent core`
3. `Add Custom GPT distribution`
4. `Add ChatGPT Project distribution`
5. `Automate distribution builds and validation`
6. `Update product documentation and migration guide`
7. `Complete Romanskaparen 2.0 validation`

### PR

Öppna en PR från `romanskaparen-2.0` mot `main` när Prompt 4 är genomförd och både GPT Edition och Project Edition finns som sammanhängande distributionspaket.
