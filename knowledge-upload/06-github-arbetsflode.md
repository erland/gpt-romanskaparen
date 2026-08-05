# GitHub-arbetsflöde för romanprojekt

Detta dokument är den bindande verkställighetsmanualen för Romanskaparens GitHub-läge. `knowledge-upload/05-projektstruktur-och-synk.md` styr projektets gemensamma struktur, revisioner, filintegritet, synk och export. Denna fil styr repository, brancher, commits, pull requests, samtidighet och GitHub-specifik felhantering.

Vid konflikt gäller huvudinstruktionen först, därefter fil 05 och denna fil tillsammans. För GitHub-specifika frågor har denna fil företräde framför allmänna formuleringar i fil 05.

## Grundregel

GitHub är ett alternativt lagringslager för samma kanoniska romanprojekt som annars kan lagras som projekt-ZIP. GitHub ersätter inte projektets interna revisioner, manifest, filhashar, revisionslogg eller skyddsregler.

Exakt ett lagringsläge är kanoniskt åt gången:

- `zip`
- `github`

Romanskaparen får aldrig blanda filer från en ZIP och ett GitHub-repository i samma projektoperation.

## Antaganden för första versionen

- Ett repository innehåller exakt ett romanprojekt.
- Romanprojektets rot är repositoryts rot.
- Repositoryts aktuella default branch är basbranch.
- Standardarbetsbranchen är `development`.
- Användaren kan uttryckligen välja ett annat arbetsbranchnamn.
- Romanskaparen gör projektändringar på arbetsbranchen.
- Romanskaparen skapar eller återanvänder en pull request mot default branch.
- Användaren ansvarar normalt för merge.
- Romanskaparen använder aldrig force push som standard och merger aldrig automatiskt till default branch.

## Aktivera GitHub-läge

När projektfilerna ska skapas eller ett befintligt projekt ska anslutas ska användaren ange repository som URL eller `owner/repository`.

Före första skrivningen ska Romanskaparen kontrollera:

1. att repositoryt finns och kan läsas
2. att skrivbehörighet finns
3. repositoryts aktuella default branch
4. aktuell head-SHA för default branch
5. om vald arbetsbranch finns
6. aktuell head-SHA för arbetsbranchen om den finns
7. om en öppen pull request finns från arbetsbranchen till default branch
8. om repositoryt är tomt eller innehåller ett romanprojekt
9. om projektet är verifierbart modernt, äldre manifestlöst eller skadat modernt

Redovisa konfigurationen:

```text
Lagringsläge: GitHub
Repository: owner/repository
Projektrot: /
Basbranch: <default branch>
Arbetsbranch: development
```

Om endast läsbehörighet finns får projektet analyseras, men ingen ändring får beskrivas som sparad.

## Kanonisk GitHub-källa

Före varje åtgärd ska exakt följande källidentitet låsas:

```text
repository
project_root
base_branch
base_head_sha
working_branch
source_head_sha
```

Aktuella branch-SHA:n ska hämtas från GitHub inför varje operation. Använd aldrig SHA, branchstatus eller filinnehåll enbart från tidigare chatthistorik.

Alla projektfiler som används i operationen ska läsas från exakt `source_head_sha` på arbetsbranchen. Om arbetsbranchen ännu inte finns används default branchens låsta head som källa för att skapa den.

## Skapa arbetsbranch

Om arbetsbranchen saknas:

1. läs default branchens aktuella head-SHA
2. skapa arbetsbranchen från exakt denna SHA
3. läs tillbaka branchens head
4. kontrollera att den matchar förväntad SHA
5. fortsätt först därefter

Om arbetsbranchen redan finns får den inte flyttas, återställas eller återskapas utan analys. Den kan innehålla externa ändringar.

## Pull request

Efter den första publicerade ändringen ska en pull request finnas från arbetsbranchen till default branch.

### Ingen öppen PR finns

Skapa en PR med:

- tydlig titel för den samlade förändringen
- projektoperationens syfte
- källrevision och ny revision
- ändrade filer
- verifieringsresultat
- eventuella risker eller granskningspunkter

### Öppen PR finns

Skapa inte en konkurrerande PR för samma head- och base-branch. Nya commits på arbetsbranchen uppdaterar PR:n automatiskt. Uppdatera PR-beskrivningen när den annars blir missvisande eller ofullständig.

### Tidigare PR är stängd eller mergad

Om arbetsbranchen därefter skiljer sig från default branch och ingen öppen PR finns, skapa en ny PR.

## En projektoperation motsvarar en commit

En avslutad projektoperation ska normalt ge:

- exakt en ökning av projektets interna revision
- exakt en Git-commit
- en strikt lista över tillåtna projektfiler
- uppdaterat manifest och revisionslogg
- verifierade hashvärden för oförändrade kapitel

Git-commitens SHA ska redovisas i leveranskvittensen. Commitens egen SHA ska inte vara ett obligatoriskt fält i samma manifestversion, eftersom SHA:n inte finns förrän committen skapats.

## GitHub-transaktion

### Fas A – läs repositoryt och lås källan

1. verifiera repository och behörigheter
2. läs default branch och `base_head_sha`
3. läs eller skapa arbetsbranch
4. läs `source_head_sha`
5. identifiera eventuell öppen PR
6. lås repository, brancher och SHA:n för operationen

### Fas B – verifiera projektet

1. läs kanoniska filer från exakt `source_head_sha`
2. kör projektets verifiering enligt fil 05
3. läs project-id, revision, kapitelantal och kapitelhashar
4. kontrollera dubbletter och icke-kanoniska kapitelkopior
5. avbryt om modernt manifest finns men inte verifierar

### Fas C – planera och ändra

1. skapa explicit tillåten ändringslista
2. genomför endast beställd ändring
3. synka berörda kanoniska filer
4. kör projektets interna commit med förväntad revision
5. kontrollera att alla otillåtna filer är oförändrade

### Fas D – kontrollera samtidighet

Omedelbart före GitHub-publicering:

1. läs arbetsbranchens aktuella head-SHA igen
2. jämför den med `source_head_sha`
3. läs default branchens aktuella head-SHA igen
4. jämför den med `base_head_sha`

Om arbetsbranchens head har ändrats får den förberedda ändringen inte publiceras ovanpå den gamla basen. Läs om, verifiera och börja om eller avbryt vid konflikt.

Om endast default branch har ändrats ska reglerna nedan användas innan operationen publiceras eller nästa operation påbörjas.

### Fas E – publicera

1. skapa Git-objekt eller filuppdateringar som motsvarar den verifierade projektversionen
2. uppdatera arbetsbranchen endast som fast-forward från den förväntade headen
3. skapa PR om ingen öppen PR finns
4. annars uppdatera befintlig PR vid behov

Ingen force push.

### Fas F – läs tillbaka

1. läs den nya commit-SHA:n från arbetsbranchen
2. läs tillbaka berörda filer från exakt denna commit
3. verifiera projektet igen
4. kontrollera ny intern revision
5. kontrollera att PR:n har rätt head och base
6. lämna revisionskvittens

Om slutverifieringen misslyckas ska felet redovisas tydligt. Romanskaparen får inte påstå att operationen är godkänd.

## Externa ändringar på arbetsbranchen

Arbetsbranchen är inte exklusivt ägd av Romanskaparen.

Om `source_head_sha` har ändrats före publicering:

- skriv inte över ändringen
- använd inte force push
- publicera inte den lokalt förberedda versionen
- läs den nya headen
- verifiera projektet på nytt
- jämför ändrade filer och projektrevision
- börja om från den nya verifierade källan om det är säkert
- avbryt om manifest, revision eller kanoniska filer är i konflikt

En extern commit som återanvänder revisionsnummer, bryter manifestet eller ändrar skyddade kapitel utan sammanhängande projektcommit ska behandlas som konflikt eller skadat modernt projekt.

## Externa ändringar på default branch

Default branch kan ändras efter att arbetsbranchen skapades eller efter att en PR öppnades.

Romanskaparen ska jämföra brancherna från en tillförlitlig gemensam bas.

### Ingen relevant överlappning

Om default branch endast ändrat filer som inte påverkar den planerade projektoperationen eller projektets revisionskedja kan ändringarna integreras i arbetsbranchen, följt av full verifiering.

### Möjlig säker överlappning

Om ändringarna berör projektmetadata men är entydigt förenliga får de integreras endast om:

- resultatet kan verifieras
- ingen intern revision återanvänds
- manifest och revisionslogg förblir sammanhängande
- inga kapitelversioner väljs eller kombineras genom gissning

### Konflikt

Stoppa automatisk integration om båda brancherna har ändrat exempelvis:

- samma `kapitel/kapitel-XX.md`
- `project-manifest.json` på oförenliga sätt
- `revision-log.md` med konkurrerande revisioner
- samma status-, tidslinje- eller kontinuitetsfakta med olika innehåll

Romanskaparen får inte kreativt slå ihop två kapitelversioner utan uttryckligt uppdrag.

## Båda brancherna har ändrats

Jämför separat:

- gemensam bas till default branch
- gemensam bas till arbetsbranch

Om ändrade filuppsättningar är disjunkta kan en säker integration vara möjlig, men resultatet måste verifieras som en ny sammanhängande projektversion.

Om samma kanoniska filer har ändrats på båda sidor ska operationen normalt avbrytas och användaren få välja konfliktlösning.

## Tillåtna sätt att synka default till arbetsbranch

Romanskaparen får använda en vanlig merge eller annan fast-forward-säker integration om verktygsmiljön stödjer detta och resultatet kan verifieras.

Följande är förbjudet som standard:

- force push
- hard reset av arbetsbranchen
- borttagning av externa commits
- omskrivning av publicerad historik
- automatisk vinnare mellan två kapitelversioner

Om anslutningen inte kan utföra en säker branchmerge ska Romanskaparen inte simulera den genom att kopiera ett urval filer och kalla det merge, om inte hela resultatet och revisionskedjan kan verifieras entydigt.

## Klassificering av befintliga GitHub-projekt

### Verifierbart modernt

Manifest finns och `verify` lyckas. Fortsätt från exakt låst commit.

### Äldre manifestlöst

Manifest saknas helt. Legacy-migrering får genomföras från exakt låst commit. Befintliga kapitel ska bevaras byte-identiskt i baslinjerevisionen.

### Skadat modernt

Manifest finns men är ogiltigt eller verifieringen misslyckas. Kör inte `init`, radera inte manifestet och återställ inte godtyckligt från default branch. Reparera endast från entydig Git-historik eller avbryt.

## Tomt repository

För ett tomt repository:

1. fastställ default branch
2. skapa arbetsbranch
3. skapa projektmallen i repositoryts rot
4. initiera intern revision
5. verifiera alla projektfiler
6. committa till arbetsbranchen
7. läs tillbaka och verifiera
8. skapa PR mot default branch

Om repositoryt saknar en användbar default branch och anslutningen inte kan initiera den säkert ska användaren få ett tydligt fel i stället för att Romanskaparen gissar.

## GitHub till ZIP-export

När GitHub är kanonisk källa kan användaren begära en projekt-ZIP.

1. fastställ om exporten ska baseras på arbetsbranch eller default branch
2. lås exakt commit-SHA
3. verifiera projektet
4. paketera hela projektroten
5. återöppna ZIP-filen i en tom kontrollkatalog
6. kör slutverifiering
7. leverera ZIP-filen som export eller säkerhetskopia

ZIP-exporten blir inte automatiskt ny kanonisk källa.

## Växla lagringsläge

Växling mellan ZIP och GitHub är en explicit migreringsoperation.

Den ska bevara:

- project-id
- sammanhängande revisionsnummer
- filhashar och kapitelhashar
- revisionslogg
- entydig källversion

Romanskaparen får inte byta lagringsläge implicit för att användaren råkar bifoga en ZIP samtidigt som ett repository är anslutet.

## Revisionskvittens

Efter varje sparad GitHub-operation ska svaret innehålla:

```text
Lagringsläge: GitHub
Repository: owner/repository
Projektrot: /
Basbranch: main
Arbetsbranch: development
Källcommit: <sha>
Ny commit: <sha>
Källrevision: r0012
Ny revision: r0013
Project-id: <id>
Ändrade filer:
- ...
Kapitelantal: ...
Senaste kapitel: ...
Verifiering: Godkänd
Pull request: #N, skapad eller uppdaterad
```

Vid avbrott ska svaret ange:

- vilken SHA som låstes
- vilken SHA som senare upptäcktes
- berörda filer om de kan identifieras
- varför ingen commit publicerades
- vad användaren behöver ta ställning till

## Fel och avbrott

Avbryt utan skrivning om:

- repositoryt är oåtkomligt
- skrivbehörighet saknas
- repository, branch eller projektrot är oklar
- arbetsbranchens head ändras under operationen
- projektverifieringen misslyckas
- manifestet finns men är skadat
- samma kapitel har konkurrerande ändringar
- revisionskedjan har divergerat
- anslutningen inte kan garantera fast-forward-säker publicering

Vid avbrott får inga halvfärdiga projektfiler beskrivas som sparade.
