# GitHub Storage Design Specification

Status: Designförslag för steg 1  
Målrepository: ett romanprojekt per repository  
Standardbasbranch: repositoryts default branch  
Standardarbetsbranch: `development`

## 1. Syfte

Romanskaparen ska kunna arbeta mot två alternativa lagringslägen:

1. **ZIP-läge** – nuvarande arbetssätt där användaren laddar upp en projekt-ZIP och får tillbaka en ny verifierad projekt-ZIP efter varje sparad ändring.
2. **GitHub-läge** – projektets kanoniska filer ligger i ett GitHub-repository och Romanskaparen läser, verifierar, ändrar och committar dem på en arbetsbranch samt skapar eller uppdaterar en pull request mot repositoryts default branch.

GitHub-stödet ska läggas till utan att försvaga eller förändra det befintliga ZIP-lägets säkerhetsregler.

## 2. Grundprincip

GitHub ska behandlas som ett alternativt lagringslager, inte som ett separat innehållsarbetsflöde.

Båda lägena följer samma logiska transaktion:

1. välj och lås en kanonisk projektkälla
2. verifiera projektet
3. fastställ uttryckligen tillåtna ändringar
4. genomför endast den beställda ändringen
5. uppdatera projektets interna revision, manifest och revisionslogg
6. verifiera att otillåtna filer är oförändrade
7. spara resultatet i valt lagringslager
8. läs tillbaka och slutverifiera den sparade versionen
9. lämna en fullständig revisionskvittens

Skillnaden ligger i steg 7:

- ZIP-läge: skapa och leverera en ny verifierad ZIP.
- GitHub-läge: skapa en Git-commit på arbetsbranchen och skapa eller uppdatera en pull request.

## 3. Avgränsningar och antaganden

Den första GitHub-versionen utgår från följande:

- ett repository innehåller exakt ett romanprojekt
- romanprojektets rot är repositoryts rot
- repositoryt har en default branch, vanligen `main` eller `master`
- Romanskaparen arbetar på `development` om användaren inte anger ett annat branchnamn
- användaren ansvarar normalt för att granska och merga pull requesten
- Romanskaparen använder inte force push
- Romanskaparen merger inte automatiskt till default branch
- GitHub-repositoryt måste vara åtkomligt via användarens anslutna GitHub-konto och användaren måste ha nödvändiga läs- och skrivbehörigheter

Stöd för flera romaner eller valfri projektunderkatalog ligger utanför första versionen.

## 4. Val av lagringsläge

När ett nytt projekt har planerats färdigt och projektfilerna ska skapas ska Romanskaparen fråga:

> Hur vill du lagra och versionshantera projektet?
>
> 1. Projekt-ZIP
> 2. GitHub-repository

### 4.1 ZIP-läge

ZIP-läget fortsätter fungera enligt nuvarande regler och befintlig manual.

### 4.2 GitHub-läge

Användaren anger ett repository som URL eller `owner/repository`.

Romanskaparen ska därefter kontrollera:

- att repositoryt finns och kan läsas
- att användaren har skrivbehörighet
- repositoryts default branch
- om `development` eller användarens valda arbetsbranch redan finns
- om repositoryt är tomt eller redan innehåller ett romanprojekt
- om en öppen pull request redan finns från arbetsbranchen till default branch

Romanskaparen ska redovisa den upptäckta konfigurationen före den första skrivningen:

```text
Repository: owner/repository
Basbranch: main
Arbetsbranch: development
Projektrot: /
```

## 5. Kanonisk projektkälla i GitHub-läge

Motsvarigheten till ZIP-lägets entydigt valda indata-ZIP är följande låsta fyrdelade källidentitet:

- repository
- projektrot
- branch
- exakt commit-SHA

Före varje filbaserad åtgärd ska Romanskaparen låsa minst:

```text
repository = owner/repository
project_root = /
working_branch = development
source_head_sha = <aktuell SHA>
base_branch = <default branch>
base_head_sha = <aktuell SHA>
```

Ingen filändring får baseras på en branchversion som endast antas från tidigare chatthistorik, tidigare svar eller manifestmetadata. Aktuella branch-SHA:n ska hämtas på nytt från GitHub inför varje operation.

## 6. Branchmodell

### 6.1 Basbranch

Basbranchen ska alltid hämtas från repositoryts aktuella default branch. Namnet får inte hårdkodas till `main` eller `master`.

### 6.2 Arbetsbranch

Standardnamnet är:

```text
development
```

Användaren kan välja ett annat namn när GitHub-läget initieras.

### 6.3 Om arbetsbranchen saknas

Romanskaparen ska:

1. läsa aktuell head-SHA för default branch
2. skapa arbetsbranchen från exakt denna SHA
3. verifiera att branchen skapades korrekt
4. genomföra projektoperationen på arbetsbranchen

### 6.4 Om arbetsbranchen redan finns

Romanskaparen ska aldrig återställa, flytta eller återskapa den utan analys. Den befintliga arbetsbranchen kan innehålla användarens eller andra verktygs ändringar.

## 7. Pull request-modell

Efter den första sparade GitHub-operationen ska Romanskaparen skapa en pull request från arbetsbranchen till default branch.

Om det redan finns en öppen pull request för samma head- och base-branch:

- skapa inte en konkurrerande PR
- lägg den nya committen på samma arbetsbranch
- PR:n uppdateras automatiskt
- uppdatera PR-beskrivningen vid behov med aktuell projektrevision och sammanfattning

Om tidigare PR är mergad eller stängd och arbetsbranchen senare får nya commits ska Romanskaparen skapa en ny PR, förutsatt att branchen skiljer sig från default branch.

PR-beskrivningen bör minst innehålla:

- projektoperationens syfte
- källrevision och ny revision
- ändrade filer
- verifieringsresultat
- eventuella kända risker eller manuella granskningspunkter

## 8. Projektets interna revisioner

GitHub-commits ersätter inte projektets interna revisionssystem.

Följande ska behållas:

- `project-manifest.json`
- monoton projektrevision
- `parent_revision`
- filhashar
- kapitelhashar
- `revision-log.md`
- tillåtna ändringslistor
- verifiering av oförändrade kapitel

En Git-commit motsvarar normalt exakt en avslutad projektoperation och en intern revisionsökning med 1.

Projektets revision används för Romanskaparens logiska historik. Git-SHA används för repositoryts exakta versionsidentitet.

Aktuell commits egen SHA ska inte skrivas in i samma commit som skapar SHA:n, eftersom det skulle ge ett cirkulärt beroende. Commit-SHA redovisas därför i chattens revisionskvittens och i GitHub/PR-metadata, inte som obligatoriskt fält i manifestet.

## 9. Samtidiga och externa ändringar

Romanskaparen måste räkna med att användaren eller någon annan kan ändra både default branch och arbetsbranch mellan två arbetssteg eller under ett pågående arbetssteg.

Ingen branch ska därför betraktas som exklusivt ägd av Romanskaparen.

### 9.1 Optimistiskt skrivlås

Före innehållsändringen låses arbetsbranchens `source_head_sha`.

Omedelbart före publicering ska Romanskaparen läsa arbetsbranchens head-SHA på nytt.

Om aktuell SHA inte längre är identisk med `source_head_sha`:

- skriv inte över branchen
- använd inte force push
- publicera inte den lokalt förberedda ändringen
- läs om projektet från den nya branch-headen
- verifiera projektet på nytt
- jämför de externa ändringarna med den planerade operationen
- börja om från den nya verifierade baslinjen eller avbryt vid konflikt

### 9.2 Default branch har ändrats

Om default branch har nya commits medan arbetsbranchen är oförändrad ska Romanskaparen avgöra om arbetsbranchen behöver synkas före nästa projektoperation.

Romanskaparen ska jämföra ändringar från senaste gemensamma bas eller annan tillförlitlig jämförelsepunkt.

Tre utfall finns:

#### A. Ingen relevant överlappning

Exempel:

- README ändrad på default branch
- nästa kapitel skapas på development

Romanskaparen kan föra in default branch i arbetsbranchen eller skapa en motsvarande säker uppdatering, därefter verifiera projektet och fortsätta.

#### B. Överlappning utan semantisk konflikt

Exempel:

- metadatafält har kompletterats på default branch
- development innehåller andra projektfiler

Romanskaparen får endast integrera ändringarna om resultatet kan verifieras entydigt och projektets interna revisionskedja förblir giltig.

#### C. Möjlig eller faktisk konflikt

Exempel:

- samma kapitel har ändrats på båda brancherna
- manifest eller revisionslogg har utvecklats olika
- båda brancherna har skapat samma nästa revisionsnummer

Romanskaparen ska avbryta automatisk publicering och redovisa konflikten. Den får inte kreativt slå ihop två kapitelversioner eller välja vinnare utan ett uttryckligt användarbeslut.

### 9.3 Arbetsbranchen har ändrats

Om någon annan har pushat till arbetsbranchen ska den nya headen behandlas som ny potentiell kanonisk källa.

Romanskaparen ska:

1. läsa om hela den relevanta projektkontexten
2. verifiera manifest och revision
3. kontrollera vilka filer som ändrats
4. kontrollera att revisionskedjan är monoton och sammanhängande
5. fortsätta endast från denna nya verifierade branch-head

Om den externa committen har brutit manifestet, återanvänt ett revisionsnummer eller ändrat skyddade kapitel utan korrekt projektcommit ska fallet klassificeras som skadat modernt projekt eller konfliktfall.

### 9.4 Båda brancherna har ändrats

Romanskaparen ska jämföra:

- ändringar på default branch sedan gemensam bas
- ändringar på arbetsbranchen sedan gemensam bas

Om filuppsättningarna är disjunkta och projektets revisionsmodell kan förenas säkert kan en automatisk synk vara möjlig.

Om samma kanoniska filer har ändrats på båda sidor, särskilt:

- `project-manifest.json`
- `revision-log.md`
- `projektstatus.md`
- samma `kapitel/kapitel-XX.md`
- samma kontinuitets- eller tidslinjefiler

ska Romanskaparen normalt stoppa och begära ett användarbeslut eller en uttrycklig konfliktlösningsoperation.

## 10. Konfliktprinciper

Följande är förbjudet som standard:

- force push
- automatisk borttagning av andras commits
- hård återställning av arbetsbranchen till default branch
- automatisk merge av två olika versioner av samma kapitel
- återanvändning av projektets revisionsnummer
- automatisk reparation genom att ta bort eller initiera om ett befintligt manifest
- fortsatt skrivande ovanpå ett projekt som inte verifierar

Vid konflikt ska Romanskaparen redovisa:

- berörda brancher och SHA:n
- berörda filer
- varför automatisk sammanslagning inte är säker
- möjliga handlingsalternativ

## 11. GitHub-transaktion för en projektändring

### Fas A – anslut och lås

1. verifiera repository och behörigheter
2. läs default branch
3. läs eller skapa arbetsbranch
4. läs aktuell head-SHA för båda brancherna
5. identifiera öppen PR
6. lås arbetsbranchens käll-SHA

### Fas B – läs och verifiera

1. läs projektets kanoniska filer från exakt den låsta committen
2. verifiera `project-manifest.json`
3. kontrollera projekt-id, revision och filhashar
4. kontrollera kapitelantal och dubbletter
5. klassificera projektet som verifierbart modernt, äldre manifestlöst eller skadat modernt

### Fas C – planera och ändra

1. skapa en explicit tillåten ändringslista
2. genomför endast beställd ändring
3. uppdatera synkfiler enligt befintliga regler
4. kör intern projektcommit så att revisionen ökar exakt med 1
5. kontrollera att skyddade filer är oförändrade

### Fas D – kontrollera samtidighet

1. läs arbetsbranchens aktuella head-SHA igen
2. jämför med den låsta käll-SHA:n
3. om SHA skiljer sig: avbryt publicering och analysera externa ändringar
4. kontrollera om default branch förändrats och om detta påverkar operationen

### Fas E – publicera

1. skapa Git-commit på arbetsbranchen
2. flytta arbetsbranchens ref endast som fast-forward från förväntad head
3. skapa PR om ingen öppen PR finns
4. annars låt befintlig PR uppdateras och uppdatera dess beskrivning vid behov

### Fas F – läs tillbaka och slutverifiera

1. läs tillbaka de berörda filerna från den nya commit-SHA:n
2. kör projektverifiering igen
3. kontrollera projektets nya revision och filhashar
4. kontrollera att PR:n pekar på rätt head och base
5. redovisa revisionskvittens

## 12. Revisionskvittens i GitHub-läge

Efter varje sparad ändring ska svaret minst innehålla:

```text
Lagringsläge: GitHub
Repository: owner/repository
Projektrot: /
Basbranch: main
Arbetsbranch: development
Källcommit: abc123...
Ny commit: def456...
Källrevision: r0012
Ny revision: r0013
Project-id: <id>
Ändrade filer:
- kapitel/kapitel-12.md
- kapitelplan.md
- projektstatus.md
- arbetslogg.md
Verifiering: Godkänd
Pull request: #4, skapad eller uppdaterad
```

Om något steg avbröts ska svaret tydligt ange att ingen commit publicerades.

## 13. Nya och befintliga repositoryn

### 13.1 Tomt repository

Romanskaparen ska:

1. identifiera default branch eller hjälpa användaren initiera repositoryt
2. skapa arbetsbranch
3. skapa hela romanprojektets mallstruktur där
4. initiera projektets interna revision
5. verifiera resultatet
6. committa till arbetsbranchen
7. öppna PR mot default branch

### 13.2 Befintligt modernt projekt

Romanskaparen läser och verifierar projektet från vald branch och commit.

Om default branch innehåller projektet men arbetsbranchen saknas skapas arbetsbranchen från aktuell default head.

### 13.3 Äldre manifestlöst projekt

Legacy-migrering ska kunna genomföras mot en exakt låst Git-commit på motsvarande säkra sätt som nuvarande ZIP-audit.

Befintliga kapitel ska bevaras byte-identiskt under baslinjemigreringen.

### 13.4 Skadat modernt projekt

Om manifest finns men inte verifierar får Romanskaparen inte initiera om projektet. Fallet kräver reparation från en entydig Git-historik eller avbrott.

## 14. ZIP-export från GitHub-läge

Användaren ska kunna begära en projekt-ZIP även när GitHub är kanoniskt lagringsläge.

Romanskaparen ska då:

1. fråga eller avgöra om exporten ska baseras på arbetsbranch eller default branch
2. låsa en exakt commit-SHA
3. verifiera projektet
4. paketera hela romanprojektet
5. återöppna och slutverifiera ZIP-filen
6. leverera ZIP-filen som export eller säkerhetskopia

ZIP-exporten byter inte automatiskt projektets kanoniska lagringsläge. Fortsatt arbete sker mot GitHub tills användaren uttryckligen genomför en lagringsmigrering.

## 15. Växling mellan lagringslägen

Endast ett lagringsläge ska vara kanoniskt åt gången.

En växling mellan ZIP och GitHub ska behandlas som en explicit migreringsoperation med:

- entydigt vald källversion
- full verifiering
- dokumenterat nytt kanoniskt lagringsläge
- oförändrat project-id
- sammanhängande projektrevision
- tydlig revisionskvittens

Romanskaparen får inte växla källa implicit bara för att både en ZIP och ett repository är tillgängliga.

## 16. Behörigheter och felhantering

GitHub-läget kräver att Romanskaparen kan:

- läsa repository och filer
- läsa brancher och commits
- skapa branch
- skapa och uppdatera filer eller commits
- skapa eller uppdatera pull request

Om läsbehörighet finns men skrivbehörighet saknas får Romanskaparen analysera projektet men inte påstå att ändringar är sparade.

Om GitHub-anslutningen saknas eller inte når angivet privat repository ska Romanskaparen stoppa och förklara vilket åtkomstproblem som måste lösas.

## 17. Säkerhets- och kvalitetskrav

GitHub-läget ska minst bevara följande egenskaper från ZIP-läget:

- exakt en kanonisk källa per operation
- låst källversion
- monotona projektrevisioner
- filhashverifiering
- skydd av oförändrade kapitel
- explicit tillåten ändringslista
- slutverifiering av sparad version
- tydlig leveranskvittens
- avbrott i stället för gissning vid oklar källa eller konflikt

Git-historik och PR-diffar är kompletterande skydd, inte ersättning för projektets interna integritetsmodell.

## 18. Föreslagna implementationseffekter

När designen godkänts behöver följande filer sannolikt ändras:

- `gpt-instructions.md`
- `knowledge-upload/05-projektstruktur-och-synk.md`
- ny bindande fil, exempelvis `knowledge-upload/06-github-arbetsflode.md`
- `README.md`
- `SETUP.md`
- `project-template-bundle.md`
- `templates/romanprojekt/project-manifest.json`
- `templates/romanprojekt/README.md`
- `templates/romanprojekt/project-index.md`
- `templates/romanprojekt/projektstatus.md`
- eventuellt `scripts/project_integrity.py`
- test- och valideringsdokumentation

Huvudinstruktionen bör endast innehålla korta bindande huvudregler. Detaljerad verkställighet bör ligga i knowledge-filerna för att hålla Instructions-fältet kompakt.

## 19. Minsta testmatris för implementationen

Följande scenarier ska testas innan GitHub-läget betraktas som färdigt:

1. nytt tomt repository
2. befintligt verifierbart projekt på default branch
3. arbetsbranch saknas
4. arbetsbranch finns, PR saknas
5. öppen PR finns och uppdateras
6. tidigare PR är mergad och ny PR behöver skapas
7. default branch har nya icke överlappande commits
8. default branch har ändrat samma kanoniska fil
9. arbetsbranchen har fått externa commits före operationen
10. arbetsbranchen ändras under pågående operation
11. båda brancherna har ändrats utan filöverlappning
12. båda brancherna har ändrat samma kapitel
13. manifestet verifierar inte
14. användaren saknar skrivbehörighet
15. GitHub-projekt exporteras till verifierad ZIP
16. explicit migrering från ZIP till GitHub
17. explicit migrering från GitHub till ZIP

## 20. Beslut som låses av denna design

- ett romanprojekt per repository
- repositoryts default branch används som basbranch
- `development` används som standardarbetsbranch
- användaren kan välja annat arbetsbranchnamn
- Romanskaparen skapar eller återanvänder en PR mot default branch
- användaren ansvarar normalt för merge
- inga force pushes
- inga automatiska merges till default branch
- externa ändringar på båda brancherna måste upptäckas genom aktuella SHA:n
- arbetsbranchens head låses optimistiskt inför varje skrivoperation
- en ändrad head före publicering tvingar omstart eller konfliktanalys
- projektets interna revisioner och filhashar behålls
- GitHub är ett lagringslager; innehålls- och integritetsflödet ska i övrigt vara gemensamt med ZIP-läget
- ZIP kan skapas som export utan att bli ny kanonisk källa
- endast ett kanoniskt lagringsläge får vara aktivt åt gången

## 21. Nästa steg

Efter godkänd design bör implementationen delas upp i separata revisioner:

1. skapa bindande GitHub-manual och generalisera källbegreppet i fil 05
2. uppdatera `gpt-instructions.md`
3. uppdatera projektmall, manifestmodell och integritetsverktyg
4. uppdatera README, SETUP och conversation starters
5. genomför konsistensgranskning och hela testmatrisen

Denna fil är i steg 1 en designspecifikation och ska inte ensam betraktas som en bindande GPT-instruktion.
