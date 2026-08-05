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

### Uppdrag

Inventera hela nuvarande repositoryt och skapa den slutliga arkitekturspecifikationen för Romanskaparen 2.0.

### Ska omfatta

- klassificera alla nuvarande filer som kärna, GPT-distribution, projektmall, dokumentation, historik eller genererad artefakt
- identifiera duplicerade och GPT-specifika formuleringar
- definiera kanoniska källfiler
- definiera vilka filer som ska genereras
- låsa slutlig katalogstruktur
- definiera bakåtkompatibilitet med nuvarande ZIP-projekt
- definiera hur ett ChatGPT Project per roman ska fungera
- definiera skillnaden mellan Custom GPT Edition och Project Edition

### Leverabler

- `docs/architecture.md`
- `docs/migration-from-1.x.md` som första utkast
- en filflyttningsmatris från nuvarande struktur till 2.0-strukturen

### Ska inte göras ännu

- inga stora filflyttar
- ingen omskrivning av huvudinstruktionen
- ingen ändring av projektmallen

### Godkännandekriterier

- varje nuvarande fil har en beslutad destination eller borttagningsmotivering
- endast en kanonisk källa finns för varje regelområde
- GPT och Project beskrivs som distributioner, inte separata produkter

---

## Prompt 2 – Skapa Romanskaparen Core

### Uppdrag

Skapa `core/` och flytta eller omarbeta gemensamma instruktioner, knowledge-filer och projektmallar till kanoniska kärnfiler.

### Ska omfatta

- skapa `core/instructions/romanskaparen-core.md`
- flytta gemensamma knowledge-filer till `core/knowledge/`
- flytta projektmallen till `core/templates/romanprojekt/`
- ta bort direkta hänvisningar till GPT Builder ur kärnan
- formulera verktygsregler kapacitetsbaserat: använd endast verktyg som faktiskt finns i aktuell miljö
- behålla ZIP-lägets befintliga integritets- och revisionsmodell
- behålla nuvarande projektformat bakåtkompatibelt

### Viktigt designbeslut

Kärnan ska säga ungefär:

> Du är Romanskaparen. Följ kärnmanualerna och projektets kanoniska källa. Använd endast lagrings- och verktygskapaciteter som är verifierat tillgängliga i den aktuella miljön.

Den ska inte säga att den är en Custom GPT eller ett ChatGPT Project.

### Leverabler

- `core/instructions/romanskaparen-core.md`
- `core/knowledge/01–06`
- `core/templates/romanprojekt/`
- `core/prompts/default-starters.md`

### Godkännandekriterier

- kärnan kan läsas utan kännedom om GPT Builder
- ZIP-flödet är fortfarande fullständigt
- inga regler är dubblerade mellan gamla och nya kärnfiler
- gamla filer lämnas tillfälligt kvar eller ersätts med tydliga övergångsmarkörer tills distributionsbygget finns

---

## Prompt 3 – Custom GPT Edition

### Uppdrag

Skapa en komplett Custom GPT-distribution som bygger på kärnan och som garanterat fungerar i ZIP-läge.

### Ska omfatta

- skapa `distributions/gpt/`
- skapa en kompakt `instructions.md` under GPT Builders gräns
- skapa GPT-anpassade conversation starters
- generera eller kopiera exakt de knowledge-filer som ska laddas upp
- skapa eller generera `project-template-bundle.md`
- dokumentera vilka capabilities som ska aktiveras
- beskriva GitHub eller andra externa verktyg endast som villkorliga kapaciteter, inte som garanterade funktioner

### Leverabler

- `distributions/gpt/instructions.md`
- `distributions/gpt/conversation-starters.md`
- `distributions/gpt/knowledge/`
- `distributions/gpt/project-template-bundle.md`
- `distributions/gpt/INSTALL.md`
- `distributions/gpt/README.md`

### Godkännandekriterier

- instruktionen ryms under 8 000 tecken
- antalet knowledge-filer är högst 20
- ZIP-flödet fungerar utan externa anslutningar
- inga kärnregler underhålls manuellt endast i GPT-distributionen

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

### Godkännandekriterier

- installationen kan följas utan GPT Builder
- instruktionen fungerar som Project Instructions
- användaren förstår att skapa ett projekt per roman
- GitHub erbjuds endast om aktuell projektchatt faktiskt kan läsa och skriva till användarens repository
- ZIP fungerar som fullständig fallback

---

## Prompt 5 – Bygg- och valideringsscripts

### Uppdrag

Automatisera genereringen av distributionsfiler från kärnan och förhindra divergens.

### Ska omfatta

- generalisera befintlig bundle-generator
- skapa `scripts/build_distributions.py`
- skapa `scripts/validate_distributions.py`
- kontrollera GPT-instruktionens teckengräns
- kontrollera antalet knowledge-filer
- kontrollera att distributionsfiler motsvarar kärnkällorna
- kontrollera att bundle motsvarar projektmallen
- kontrollera att inga gamla filvägar finns kvar i aktiva instruktioner
- skapa ett maskinläsbart distributionsmanifest om det behövs

### Leverabler

- byggscript
- valideringsscript
- dokumenterade kommandon
- regenererade GPT- och Project-distributioner

### Godkännandekriterier

Följande ska fungera:

```bash
python scripts/build_distributions.py
python scripts/validate_distributions.py
```

Valideringen ska stoppa merge om:

- GPT-instruktionen är för lång
- knowledge-gränsen överskrids
- bundle är osynkad
- en distribution refererar till en saknad fil
- kärn- och distributionsversioner divergerar

---

## Prompt 6 – Dokumentation och migrationsguide

### Uppdrag

Skriv om repositoryts publika dokumentation så att Romanskaparen presenteras som en produkt med flera distributionsformer.

### Ska omfatta

- ny rot-`README.md`
- installationsguider för GPT och Project
- jämförelse mellan distributionsformerna
- rekommendation: Project Edition för långvariga romanprojekt och användarspecifika anslutningar; GPT Edition för enkel ZIP-baserad användning
- migreringsguide från nuvarande 1.x-repository
- guide för att flytta ett befintligt ZIP-projekt till ett ChatGPT Project utan att ändra romanprojektets interna format
- städa eller arkivera historiska jämförelse- och ändringsdokument

### Leverabler

- ny `README.md`
- `docs/custom-gpt-edition.md`
- `docs/chatgpt-project-edition.md`
- färdig `docs/migration-from-1.x.md`
- eventuellt `docs/archive/` för historiska dokument

### Godkännandekriterier

- en ny användare kan välja rätt distributionsform
- installationsvägen är tydlig för både GPT och Project
- inget dokument lovar GitHub-stöd där verktyget inte är verifierat tillgängligt

---

## Prompt 7 – Slutlig konsistensgranskning och accepteranstest

### Uppdrag

Gör en fullständig kvalitetskontroll och testa båda distributionerna.

### Minsta testmatris

#### Gemensam kärna

1. nytt romanprojekt från idé
2. skapa projektstruktur
3. skriv första kapitlet
4. fortsätt från verifierad revision
5. revidera exakt ett kapitel
6. exportera EPUB/PDF
7. legacy-migrera manifestlöst ZIP-projekt
8. stoppa skadat modernt manifest

#### Custom GPT Edition

1. instruktion under 8 000 tecken
2. högst 20 knowledge-filer
3. nytt ZIP-projekt
4. fortsatt ZIP-arbete
5. inga antaganden om GitHub

#### ChatGPT Project Edition

1. installation i ett tomt ChatGPT Project
2. ett Project per roman
3. flera chattar med samma projektinstruktion
4. ZIP som kanonisk källa
5. GitHub-förmågetest när anslutning finns
6. korrekt fallback när GitHub saknas eller bara är read-only
7. ingen sammanblandning mellan två romanprojekt

### Leverabler

- `docs/test-plan.md`
- `docs/implementation-validation.md`
- slutlig filinventering
- lista över kvarstående begränsningar

### Godkännandekriterier

- båda distributionerna är byggda från samma kärna
- ZIP-läget fungerar i båda
- GitHub är uttryckligen villkorligt
- inga aktiva dokument använder gamla, felaktiga sökvägar
- distributionsbygget och valideringen är reproducerbara

## 5. Rekommenderad PR-strategi

### Commitindelning

1. `Define Romanskaparen 2.0 architecture`
2. `Create platform-independent core`
3. `Add Custom GPT distribution`
4. `Add ChatGPT Project distribution`
5. `Automate distribution builds and validation`
6. `Rewrite documentation for multiple editions`
7. `Complete Romanskaparen 2.0 validation`

### Pull request

Öppna en PR från `romanskaparen-2.0` till `main` efter prompt 4, när kärnan och båda distributionerna finns. Uppdatera därefter samma PR genom prompt 5–7.

## 6. Risker att bevaka

### Dubblerad instruktionstext

Den största arkitekturrisken är att GPT- och Project-instruktioner utvecklas separat. Därför ska distributionsfiler genereras eller byggas av tydligt avgränsade kärnblock.

### Projektinstruktionernas praktiska gränser

ChatGPT Projects kan ha andra praktiska begränsningar än GPT Builder. Project Edition ska därför hålla instruktionen kompakt och lägga detaljer i projektfilerna.

### Kunskapsfiler kontra romanprojektfiler

Romanskaparens underlagsfiler beskriver verktyget. Romanens egna filer beskriver det specifika bokprojektet. Dokumentationen måste tydligt skilja dessa två kategorier.

### GitHub-tillgänglighet

GitHub får aldrig behandlas som garanterat. Förmågan ska testas i den aktuella chatten innan repositoryt görs till kanonisk källa.

### Bakåtkompatibilitet

Nuvarande ZIP-projekt och manifest får inte behöva konverteras enbart för att Romanskaparen går från 1.x till 2.0.

## 7. Rekommenderat nästa steg

Nästa prompt bör vara **Prompt 1 – Inventering och målarkitektur**. Den ska utgå från denna plan, inventera repositoryt fil för fil och låsa den slutliga 2.0-strukturen innan några större flyttar görs.
