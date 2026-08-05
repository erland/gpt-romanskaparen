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
- kapacitetsbaserad verktygsanvändning

Distributionerna ska endast beskriva hur kärnan installeras och används i respektive ChatGPT-miljö.

## 2. Inventering av nuläget

Repositoryt är i 1.x-format och är byggt runt en Custom GPT:

- `gpt-instructions.md` är en GPT Builder-instruktion nära 8 000-teckensgränsen.
- `knowledge-upload/01–05` innehåller arbetsflöde, hantverk, kontinuitet, genre och projektmanual.
- `project-template-bundle.md` är en manuellt underhållen distributionsartefakt på cirka 50 KB.
- `templates/romanprojekt/` är den kanoniska projektmallen och innehåller även integritets- och publiceringsverktyg.
- `README.md`, `SETUP.md` och `conversation-starters.md` är GPT-specifika.
- `ANDRINGAR-FILSAKER-VERSION.md` och `JAMFORELSE-MED-URSPRUNGSINSTRUKTION.md` är historiska beslutsdokument.
- `docs/romanskaparen-2.0-plan.md` är genomförandeplanen för 2.0.

### 2.1 Styrkor att bevara

- robust ZIP-transaktion med exakt en kanonisk indata-ZIP
- manifest med project-id, revision och SHA-256
- strikt tillåten ändringslista
- skydd av oförändrade kapitel
- separat revisionslogg
- legacy-audit med byte-identiska befintliga kapitel
- tydlig skillnad mellan skadat modernt projekt och legacy
- konsekvent projektstruktur
- etablerade EPUB/PDF-regler

### 2.2 Problem som 2.0 ska lösa

- kärnregler och plattformsinstruktion är blandade i `gpt-instructions.md`
- repositoryts rot presenterar Romanskaparen som en GPT, inte som en produkt
- `knowledge-upload/` är både kanonisk källa och distributionskatalog
- bundlen är en parallell kopia av projektmallen
- samma innehåll riskerar att behöva underhållas separat för GPT och Project
- GitHub eller andra verktyg kan inte antas finnas i alla miljöer
- ett långvarigt romanprojekt behöver bättre stöd för flera chattar och isolerad projektkontext

## 3. Låsta arkitekturprinciper

### 3.1 En kanonisk kärna

Varje regelområde ska ha exakt en redigerbar källa under `core/`.

Filer under `distributions/` får vara:

- genererade kopior
- korta plattformsspecifika wrappers
- installationsguider
- startprompter

De får inte bli alternativa manuellt underhållna versioner av kärnmanualerna.

### 3.2 ZIP är obligatorisk baskapacitet

Både GPT Edition och Project Edition ska fungera fullständigt i ZIP-läge när filskapande och Python/Code Interpreter är tillgängligt.

GitHub får aldrig vara ett krav för Romanskaparens kärnfunktion.

### 3.3 Verktyg används kapacitetsbaserat

Kärnan ska inte anta att en GitHub-connector, webbsökning, bildgenerering eller en viss exportmotor finns.

Före ett verktygsberoende arbetsflöde ska Romanskaparen kontrollera att den aktuella miljön faktiskt har nödvändiga läs-, skriv- och återläsningsfunktioner.

Om kapaciteten saknas ska Romanskaparen:

- inte låtsas att funktionen finns
- inte ändra projektets kanoniska lagringsläge
- använda ZIP eller ett manuellt filflöde som fallback

### 3.4 Ett ChatGPT Project per roman

Project Edition ska rekommendera:

```text
Ett ChatGPT Project = en roman
Ett romanrepository = högst en roman
Flera chattar får arbeta mot samma kanoniska romanprojekt
```

ChatGPT-projektets minne och chattkontext är hjälpmedel. Romanprojektets filer, verifierade ZIP eller repository är fortsatt kanonisk källa.

### 3.5 Projektformatet ändras inte i Prompt 2

Nuvarande romanprojektformat ska flyttas till kärnan utan att dess externa struktur eller manifestschema bryts.

Romanskaparen 2.0 ska kunna fortsätta arbeta med ZIP-projekt skapade av 1.x utan obligatorisk formatmigrering, förutsatt att projektet verifierar.

## 4. Slutlig katalogstruktur

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
  file-movement-matrix.md
  migration-from-1.x.md
  custom-gpt-edition.md
  chatgpt-project-edition.md
  test-plan.md
  implementation-validation.md
  archive/

README.md
LICENSE (om licens senare väljs)
```

## 5. Ansvarsfördelning

### 5.1 `core/instructions/romanskaparen-core.md`

Kort, bindande roll- och prioriteringsinstruktion som fungerar i alla miljöer. Den ska:

- identifiera assistenten som Romanskaparen
- hänvisa till kärnmanualerna
- definiera källprioritet
- kräva entydig kanonisk projektkälla
- kräva kapacitetskontroll
- inte nämna GPT Builder eller ChatGPT Project som identitet

Den ska inte ensam bära hela projektmanualen.

### 5.2 `core/knowledge/01–05`

Nuvarande kunskapsområden flyttas hit och blir kanoniska.

- 01: arbetsflöde och pedagogiskt stöd
- 02: berättelsehantverk
- 03: karaktärer, värld och kontinuitet
- 04: genreguider
- 05: projektstruktur, ZIP, integritet, revision och export

### 5.3 `core/knowledge/06-verktyg-och-lagringskapaciteter.md`

Ny manual för miljöberoende funktioner. Den ska definiera:

- kapacitetsinventering före verktygsanvändning
- ZIP som säker standard
- GitHub som villkorlig användarspecifik kapacitet
- read-only kontra read/write
- krav på återläsning och verifiering
- fallback när verktyg saknas
- att lagringsbyte aldrig sker implicit

Den ska inte hårdkoda en viss connector eller abonnemangsplan.

### 5.4 `core/templates/romanprojekt/`

Kanonisk projektmall. Alla nuvarande mallfiler, Pythonverktyg och publiceringsresurser ska finnas här.

Distributionernas bundle genereras från denna katalog.

### 5.5 Distributionerna

#### GPT Edition

- kompakt Builder-instruktion under 8 000 tecken
- högst 20 knowledge-filer
- ZIP som garanterat arbetsflöde
- externa verktyg endast som villkorliga
- conversation starters anpassade för en Custom GPT

#### Project Edition

- projektinstruktion anpassad för ett ChatGPT Project per roman
- onboarding som förklarar vilka filer som ska bifogas
- stöd för flera specialiserade chattar
- användarens vanliga anslutningar kan nyttjas efter förmågetest
- ZIP förblir fullständig fallback

#### Conversation Edition

- minimal startprompt och lista över filer som måste bifogas
- inga löften om beständig kontext
- avsedd för test eller tillfälligt arbete

## 6. Kanoniska källor och genererade filer

### 6.1 Manuellt redigerade kanoniska filer

- allt under `core/instructions/`
- allt under `core/knowledge/`
- allt under `core/templates/`
- allt under `core/prompts/`
- installations- och README-filer som är uttryckligen plattformsspecifika
- arkitektur- och migrationsdokument

### 6.2 Genererade filer

- `distributions/gpt/knowledge/*`
- `distributions/project/knowledge/*`
- båda `project-template-bundle.md`
- plattformsinstruktioner om de kan byggas deterministiskt från kärna + wrapper
- conversation starters om de genereras från kärnans standardstarter
- `distribution-manifest.json`

Genererade filer ska märkas med en kommentar som anger källa och byggkommando där filformatet tillåter det.

## 7. Duplicerade och GPT-specifika formuleringar

Följande typer av formuleringar ska flyttas ur kärnan eller generaliseras:

- ”klistra in i GPT Builder”
- ”GPT Knowledge”
- ”conversation starters” som plattformsfält
- antaganden om exakt antal knowledge-filer
- antaganden om Canvas eller en specifik connector
- instruktioner som säger att användaren alltid måste ladda upp samma filer i varje körmiljö

Kärnan får däremot behålla termer som:

- kanonisk projektkälla
- verifierad ZIP
- projektmanifest
- kapitelhash
- revisionskvittens
- export

## 8. Bakåtkompatibilitet

### 8.1 Befintliga romanprojekt

- `project_id` bevaras.
- Nuvarande manifest och revisionskedja bevaras.
- Projektmappens sökvägar bevaras.
- `scripts/project_integrity.py` flyttas byte-identiskt i första kärnsteget om ingen nödvändig sökvägsändring krävs.
- En 1.x-ZIP ska kunna öppnas och verifieras i 2.0 utan innehållsmigrering.

### 8.2 Repositoryts distributionsfiler

Under övergången får gamla rotfiler ligga kvar till dess att GPT- och Project-distributionerna är byggda och validerade.

De ska därefter antingen:

- tas bort
- ersättas av korta hänvisningsfiler
- flyttas till `docs/archive/`

Ingen gammal fil får fortsätta vara en dold andra kanonisk källa.

## 9. Project Edition – operativ modell

Ett nytt projekt installeras genom att användaren:

1. skapar ett ChatGPT Project med romanens namn
2. klistrar in `PROJECT-INSTRUCTIONS.md`
3. bifogar de genererade knowledge-filerna och projektbundlen
4. startar med `START-HERE.md`
5. väljer eller skapar romanprojektets kanoniska källa

Rekommenderade chattar:

- Planering
- Kapitelarbete
- Redaktör
- Kontinuitet
- Export och omslag

Alla chattar ska följa samma kanoniska projektfiler. De får inte skapa parallella romanversioner baserat på projektminnet.

## 10. Skillnad mellan GPT och Project

| Område | GPT Edition | Project Edition |
|---|---|---|
| Primär användning | Enkel färdig assistent | Långvarigt romanarbete |
| Rekommenderad lagring | ZIP | ZIP eller verifierat tillgängligt verktyg |
| Kontext | En GPT-konversation | Flera chattar i ett romanprojekt |
| Installation | GPT Builder | ChatGPT Project-inställningar |
| Externa anslutningar | Kan saknas | Kan finnas användarspecifikt |
| ZIP-stöd | Obligatoriskt | Obligatoriskt |
| GitHub-stöd | Endast efter förmågetest | Endast efter förmågetest |

## 11. Beslut låsta av Prompt 1

- Romanskaparen Core är produktens enda kanoniska regelkälla.
- GPT, Project och Conversation är distributioner.
- ZIP är obligatorisk baskapacitet.
- GitHub och andra externa verktyg är villkorliga kapaciteter.
- Ett ChatGPT Project per roman rekommenderas.
- Nuvarande romanprojektformat ska vara bakåtkompatibelt.
- Projektbundlen är en genererad artefakt.
- Gamla rotfiler får inte vara permanenta parallella källor.
- Inga stora filflyttar görs förrän Prompt 2.

## 12. Nästa steg

Prompt 2 ska skapa `core/`, flytta kanoniska kunskapsfiler och projektmall dit samt lägga till den nya kapacitetsmanualen. Gamla distributionsfiler lämnas tillfälligt kvar tills Prompt 3–5 kan bygga och validera ersättarna.
