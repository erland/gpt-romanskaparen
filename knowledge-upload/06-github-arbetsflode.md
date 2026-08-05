# GitHub-arbetsflöde för romanprojekt

Detta är den bindande manualen för Romanskaparens GitHub-läge. `knowledge-upload/05-projektstruktur-och-synk.md` styr gemensam projektstruktur, revision, filintegritet, synk, migration och export. Denna fil styr repository, brancher, commits, pull requests, samtidighet och GitHub-specifik felhantering.

Vid konflikt gäller huvudinstruktionen först, därefter fil 05 och sedan denna fil för GitHub-specifika frågor.

## Grundregel

GitHub är ett valfritt lagringslager för samma romanprojekt som annars kan lagras i projekt-ZIP. Exakt ett lagringsläge är kanoniskt åt gången. Blanda aldrig ZIP- och GitHub-filer i samma operation.

GitHub-läge får endast användas när den aktuella GPT-konfigurationen faktiskt har de anslutningar och rättigheter som krävs. Anta aldrig att GitHub-stöd finns bara för att användaren anger ett repository.

## Obligatoriskt förmågetest

Före första GitHub-migreringen eller skrivningen ska Romanskaparen verifiera:

1. repositoryt kan läsas
2. repositorymetadata och aktuell default branch kan hämtas
3. aktuella head-SHA:n för berörda brancher kan hämtas
4. skrivbehörighet finns
5. en arbetsbranch kan skapas eller säkert återanvändas
6. en fil eller commit kan skapas eller uppdateras på arbetsbranchen
7. en pull request kan skapas eller en befintlig PR kan återanvändas
8. den publicerade committen och berörda filer kan läsas tillbaka

Förmågetestet ska genomföras utan att ändra romanprojektets kanoniska innehåll. Använd vid behov en neutral testfil eller ett separat tomt testrepository. Om detta inte kan göras säkert ska testet avbrytas.

Om någon förmåga saknas:

- ändra inte `storage.mode` till `github`
- påbörja inte ZIP → GitHub-migrering
- gör inga projektändringar i repositoryt
- påstå inte att GitHub-stöd finns
- erbjud fortsatt ZIP-läge
- ange exakt vilken läs-, skriv-, branch-, commit-, PR- eller återläsningsförmåga som saknas

Ett lästest är inte tillräckligt för skrivande GitHub-läge. Läsbehörighet utan säker skrivning får endast användas för analys.

## Antaganden för första versionen

- Ett repository innehåller exakt ett romanprojekt.
- Projektroten är repositoryts rot.
- Repositoryts aktuella default branch är basbranch.
- Standardarbetsbranchen är `development`, om användaren inte väljer annat.
- Projektändringar görs endast på arbetsbranchen.
- En PR skapas eller återanvänds mot default branch.
- Användaren ansvarar normalt för merge.
- Ingen force push eller automatisk merge används.

## Aktivera GitHub-läge

Efter godkänt förmågetest anger användaren repository som URL eller `owner/repository`.

Före första projektoperationen ska Romanskaparen kontrollera:

- repository och behörigheter
- default branch och dess aktuella head-SHA
- vald arbetsbranch och dess aktuella head-SHA
- eventuell öppen PR mellan arbetsbranch och default branch
- om repositoryt är tomt eller innehåller ett romanprojekt
- om projektet är verifierbart modernt, äldre manifestlöst eller skadat modernt

Redovisa minst:

```text
Lagringsläge: GitHub
Repository: owner/repository
Projektrot: /
Basbranch: <default branch>
Arbetsbranch: development
Förmågetest: Godkänt
```

## Kanonisk GitHub-källa

Före varje åtgärd ska följande låsas:

```text
repository
project_root
base_branch
base_head_sha
working_branch
source_head_sha
```

Hämta alltid aktuella SHA:n från GitHub. Använd inte branchstatus eller filinnehåll enbart från tidigare chatthistorik.

Alla projektfiler ska läsas från exakt `source_head_sha` på arbetsbranchen. Om arbetsbranchen saknas skapas den från exakt låst default-head.

## Arbetsbranch och pull request

Om arbetsbranchen saknas:

1. läs default branchens aktuella head-SHA
2. skapa arbetsbranchen från exakt denna SHA
3. läs tillbaka arbetsbranchens head
4. kontrollera att SHA:n matchar

En befintlig arbetsbranch får inte återställas eller återskapas utan analys. Den kan innehålla externa ändringar.

Efter första publicerade ändringen ska en PR finnas från arbetsbranch till default branch. Skapa inte en konkurrerande PR för samma branchpar. Nya commits uppdaterar normalt befintlig PR. Uppdatera PR-beskrivningen när den annars blir missvisande.

## En projektoperation motsvarar normalt en commit

En avslutad operation ska normalt ge:

- exakt en ökning av intern projektrevision
- exakt en Git-commit
- en explicit tillåten ändringslista
- uppdaterat manifest och revisionslogg
- verifierade hashvärden för oförändrade kapitel

Git-SHA redovisas i revisionskvittensen men lagras inte som obligatoriskt fält i samma manifestversion.

## GitHub-transaktion

### Fas A – lås källan

1. verifiera repository, förmågor och behörigheter
2. läs default branch och `base_head_sha`
3. läs eller skapa arbetsbranch
4. läs `source_head_sha`
5. identifiera öppen PR
6. lås repository, brancher och SHA:n

### Fas B – verifiera projektet

1. läs kanoniska filer från exakt `source_head_sha`
2. kör verifiering enligt fil 05
3. läs project-id, revision, kapitelantal och kapitelhashar
4. kontrollera dubbletter och icke-kanoniska kopior
5. avbryt om modernt manifest finns men inte verifierar

### Fas C – ändra

1. skapa explicit tillåten ändringslista
2. genomför endast beställd ändring
3. synka berörda kanoniska filer
4. skapa nästa interna revision med förväntad källrevision
5. kontrollera att otillåtna filer är oförändrade

### Fas D – kontrollera samtidighet

Omedelbart före publicering:

1. läs arbetsbranchens head-SHA igen och jämför med `source_head_sha`
2. läs default branchens head-SHA igen och jämför med `base_head_sha`

Om arbetsbranchens head ändrats får den förberedda versionen inte publiceras. Läs om och börja om eller avbryt vid konflikt.

### Fas E – publicera

1. publicera den verifierade projektversionen
2. uppdatera arbetsbranchen endast fast-forward från förväntad head
3. skapa eller återanvänd PR
4. använd aldrig force push

### Fas F – läs tillbaka

1. läs den nya commit-SHA:n
2. läs tillbaka berörda filer från exakt denna commit
3. verifiera projektet igen
4. kontrollera ny intern revision och PR:ns branchpar
5. lämna revisionskvittens

Om slutverifieringen misslyckas får operationen inte beskrivas som godkänd.

## Externa ändringar och konflikter

Arbetsbranchen är inte exklusivt ägd av Romanskaparen. Om dess head ändrats före publicering:

- skriv inte över
- använd inte force push
- läs den nya headen
- verifiera projektet igen
- jämför filer och projektrevision
- börja om endast om källan fortfarande är entydig

Jämför default branch och arbetsbranch från en tillförlitlig gemensam bas. En säker integration kan vara möjlig när ändrade filuppsättningar är disjunkta och resultatet verifierar.

Stoppa automatisk integration om båda sidor ändrat exempelvis:

- samma kapitelfil
- manifestet på oförenliga sätt
- revisionsloggen med konkurrerande revisioner
- samma status-, tidslinje- eller kontinuitetsfakta med olika innehåll

Slå aldrig kreativt ihop två kapitelversioner utan uttryckligt uppdrag. Ingen hard reset, force push, radering av externa commits eller omskrivning av publicerad historik.

## Klassificering av projekt

- **Verifierbart modernt:** manifest finns och `verify` lyckas. Fortsätt från exakt låst commit.
- **Äldre manifestlöst:** manifest saknas helt. Legacy-migrering får ske från exakt låst commit med byte-identiska befintliga kapitel.
- **Skadat modernt:** manifest finns men verifieringen misslyckas. Kör inte `init`, radera inte manifestet och återställ inte godtyckligt.

## Tomt repository

Efter godkänt förmågetest:

1. fastställ default branch
2. skapa arbetsbranch
3. skapa projektmallen i repositoryts rot
4. initiera intern revision
5. verifiera projektfilerna
6. committa till arbetsbranchen
7. läs tillbaka och verifiera
8. skapa PR

Om repositoryt saknar användbar default branch och anslutningen inte kan initiera den säkert ska GitHub-läget avbrytas och ZIP erbjudas.

## Export och lagringsbyte

En ZIP-export från GitHub är en export, inte automatiskt ett lagringsbyte. Lås exakt commit-SHA, verifiera, paketera, återöppna och slutverifiera ZIP-filen.

Växling mellan ZIP och GitHub är en uttrycklig migrering som bevarar project-id, revisionskedja, filhashar och entydig källversion. ZIP → GitHub får endast ske efter godkänt förmågetest.

## Revisionskvittens

Efter en sparad GitHub-operation ska svaret innehålla:

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
Verifiering: Godkänd
Pull request: #N, skapad eller uppdaterad
```

Vid avbrott ska svaret ange vilken förmåga, SHA, fil eller verifiering som blockerade skrivning och varför ingen commit publicerades.

## Obligatoriska avbrott

Avbryt utan skrivning om:

- förmågetestet inte är fullständigt godkänt
- repositoryt är oåtkomligt
- skriv-, branch-, commit-, PR- eller återläsningsförmåga saknas
- repository, branch eller projektrot är oklar
- arbetsbranchens head ändras under operationen
- projektverifieringen misslyckas
- manifestet finns men är skadat
- samma kapitel har konkurrerande ändringar
- revisionskedjan har divergerat
- fast-forward-säker publicering inte kan garanteras

Vid avbrott får inga halvfärdiga projektfiler beskrivas som sparade.
