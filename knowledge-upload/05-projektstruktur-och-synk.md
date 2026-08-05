# Projektstruktur, versionslås, synk och exportregler

Detta dokument är den bindande verkställighetsmanualen för Romanskaparens gemensamma projektstruktur, källval, revisioner, filintegritet, synk, migrering, reparation och export. Det gäller oavsett om projektet lagras som ZIP eller i GitHub.

GitHub-specifika regler för repository, brancher, commits, pull requests och samtidighet finns i `06-github-arbetsflode.md`. Vid konflikt gäller huvudinstruktionen först, därefter denna fil och sedan fil 06 för GitHub-specifika frågor.

## Grundregel

Det ska alltid finnas:

- exakt en kanonisk uppsättning projektfiler
- exakt ett aktivt lagringsläge
- exakt en entydigt vald och låst källrevision per arbetssteg

Skapa inte parallella statusfiler, alternativa översikter eller tillfälliga sammanfattningsfiler när motsvarande kanonisk fil redan finns.

## Kanoniskt lagringsläge

Ett projekt har ett av följande kanoniska lagringslägen:

- **ZIP:** en uttryckligen vald projekt-ZIP är källa och nästa verifierade ZIP är leverans.
- **GitHub:** ett uttryckligen valt repository, projektrot, arbetsbranch och commit-SHA är källa; nästa verifierade Git-commit på arbetsbranchen är leverans.

Blanda aldrig filer från ZIP, GitHub, chattext, EPUB/PDF, äldre arbetskataloger eller andra projektversioner i samma operation.

Att skapa en ZIP-export från GitHub eller lägga projektet i ett repository byter inte automatiskt kanoniskt lagringsläge. Ett byte är en uttrycklig migreringsoperation.

## Begränsning som arbetsflödet måste ta höjd för

En fil eller branch som förekommit tidigare i chatten är inte automatiskt en säker aktuell källa. Säkerheten ska komma från:

- explicit källval
- låst källversion
- monotona revisionsnummer
- manifest
- filhashar
- ny verifiering före varje ändring

Romanskaparen får aldrig anta att det mest övertygande filnamnet, den senast nämnda ZIP-filen eller en tidigare läst branch fortfarande är aktuell.

## Val och låsning av kanonisk projektkälla

Före varje åtgärd som läser eller ändrar projektfiler ska exakt en källa väljas och låsas.

### ZIP-källa

1. Välj exakt en indata-ZIP.
2. Prioritera ZIP-filen som användaren uttryckligen bifogat eller namngivit i aktuellt meddelande.
3. Om den namngivna ZIP-filen inte är åtkomlig: avbryt.
4. Om flera ZIP-filer är möjliga och ingen valts: avbryt.
5. Kontrollera att användaren inte hänvisar till en högre revision än ZIP-filens manifest.
6. Lås filnamn, storlek och SHA-256 för käll-ZIP-filen när verktyget stödjer det.

### GitHub-källa

1. Lås repository.
2. Lås projektrot; i första versionen `/`.
3. Hämta repositoryts aktuella default branch.
4. Lås arbetsbranch.
5. Hämta och lås aktuell head-SHA för både default branch och arbetsbranch.
6. Läs projektfiler från exakt arbetsbranchens låsta commit-SHA.
7. Följ därefter `06-github-arbetsflode.md`.

## Fast projektstruktur

```text
romanprojekt/
  README.md
  project-manifest.json
  revision-log.md
  project-index.md
  roman-bibel.md
  synopsis.md
  kapitelplan.md
  stilguide.md
  tidslinje.md
  kontinuitetsanteckningar.md
  revisionsonskemal.md
  arbetslogg.md
  projektstatus.md
  karaktarer/
    huvudperson.md
    antagonist.md
    bifigurer.md
  kapitel/
    kapitelmall.md
    kapitel-XX.md
  kapitelnoteringar.md
  scripts/
    project_integrity.py
  omslag/
    cover.jpg
  publishing/
    metadata.yaml
    epub.css
    pdf-template.tex
    build-notes.md
    fix-epub-after-pandoc.py
  exports/
    README.md
    exportlogg.md
```

Skapa inte en `kapitel-XX.md` förrän kapitlet faktiskt finns.

## Projektmanifest och revisioner

`project-manifest.json` är projektets maskinläsbara revisionslås. Det ska minst innehålla:

- stabilt `project_id`
- `project_slug`
- heltalsfältet `revision`
- `parent_revision`
- tidsstämplar
- senaste operation
- källrevision
- ändrade filer
- hash och filstorlek för varje spårad fil
- separat kapitelöversikt med SHA-256 för varje kanonisk kapitelfil

ZIP-specifika fält får finnas i ZIP-läge. GitHub-specifik lagringsmetadata läggs till när projektmallen senare stödjer detta. Ett äldre manifest utan lagringsmetadata ska fortsätta vara ett giltigt ZIP-projekt om övrig verifiering lyckas.

Manifestet hashar inte sig självt. `revision-log.md` är append-only revisionshistorik.

Varje avslutad projektoperation ska:

- utgå från exakt förväntad revision
- öka revisionen med exakt 1
- sätta korrekt `parent_revision`
- använda ett revisionsnummer som aldrig återanvänds

## Deterministiskt integritetsverktyg

Varje projekt ska innehålla `scripts/project_integrity.py`.

```bash
python scripts/project_integrity.py verify .
python scripts/project_integrity.py status .
```

För nästa projektversion används `commit` med:

- `--expected-revision`
- tydlig operation
- en eller flera strikta `--allow`
- lagringsspecifik källmetadata enligt aktuell verktygsversion

Exempel för befintligt ZIP-flöde:

```bash
python scripts/project_integrity.py commit . \
  --expected-revision <gammal-revision> \
  --operation "<kort beskrivning>" \
  --zip-name <nytt-filnamn.zip> \
  --source-zip-name <indata.zip> \
  --allow '<tillåten/sökväg>'
```

`--allow` anges per fil eller globmönster som får ändras. Verktyget ska stoppa om någon annan fil har ändrats, lagts till eller försvunnit.

Integritetsverktyget verifierar projektets interna filer och revisioner. GitHub-API, branch-SHA, commits och pull requests hanteras av GitHub-arbetsflödet i fil 06.

## Gemensam projekttransaktion

### Fas A – lås och verifiera källan

1. Skapa en helt ny tom arbetskatalog eller motsvarande isolerad arbetsyta.
2. Materialisera endast den låsta källversionen där.
3. Kontrollera att källan innehåller exakt ett projektträd.
4. Kör `verify` före varje ändring.
5. Läs project-id, revision, kapitelantal, senaste kapitel och kapitelhashar.
6. Kontrollera dubbletter och icke-kanoniska kapitelkopior som `kapitel-04-ny.md`, `kapitel-04-old.md` eller `kapitel-04(1).md`.
7. Avbryt om projektet inte kan verifieras.

För ZIP packas exakt vald ZIP upp. För GitHub läses exakt låst commit enligt fil 06.

### Fas B – gör endast den beställda ändringen

1. Skapa en explicit tillåten ändringslista innan arbetet börjar.
2. Vid nytt kapitel får en ny `kapitel/kapitel-XX.md` skapas, men inga befintliga kapitelfiler ändras.
3. Vid revision av kapitel X får endast `kapitel/kapitel-XX.md` ändras bland kapitelfilerna.
4. Vid status-, metadata-, omslags- eller exportarbete får kapitelfiler inte ändras utan uttrycklig beställning.
5. Vanliga synkfiler ändras endast när operationen kräver det.
6. Kopiera aldrig in ett kapitel från annan ZIP, branch, export eller chattext för att fylla ett hål.

Vanliga synkfiler:

- `kapitelplan.md`
- `projektstatus.md`
- `arbetslogg.md`
- `tidslinje.md`
- `kontinuitetsanteckningar.md`
- `karaktarer/*.md`
- `kapitelnoteringar.md`
- `project-index.md`
- publicerings- och exportfiler

### Fas C – intern commit och kapitelskydd

1. Kör `status`.
2. Granska alla väntande ändringar.
3. Kör projektets interna `commit` med förväntad revision och strikt tillåten ändringslista.
4. Kontrollera att revisionen ökade exakt med 1.
5. Kontrollera att manifest och revisionslogg uppdaterades.
6. Alla kapitelfiler utanför uttryckligen tillåten målfil ska ha samma SHA-256 som i källrevisionen.
7. Avbryt om ett skyddat kapitel har ändrats.

### Fas D – spara i valt lagringslager

#### ZIP

1. Paketera hela projektkatalogen.
2. Använd revisionsbaserat filnamn.
3. Packa upp färdig ZIP i ytterligare en tom kontrollkatalog.
4. Kör `verify` där.
5. Leverera endast godkänd ZIP.

#### GitHub

1. Kontrollera branch-SHA:n på nytt enligt fil 06.
2. Publicera endast som fast-forward från förväntad head.
3. Skapa Git-commit på arbetsbranchen.
4. Skapa eller uppdatera PR mot default branch.
5. Läs tillbaka filer från nya commit-SHA:n.
6. Kör slutverifiering mot den sparade GitHub-versionen.

## Synkpassering efter kapitelarbete

Efter varje skapat, reviderat eller godkänt kapitel:

1. Spara endast berättelsetext i `kapitel/kapitel-XX.md`.
2. Spara redaktionella noteringar i `kapitelnoteringar.md`.
3. Uppdatera kapitlets rad i `kapitelplan.md`.
4. Lägg till nästa planerade kapitel om planen vuxit.
5. Uppdatera `projektstatus.md`.
6. Lägg exakt en ny post i `arbetslogg.md`.
7. Uppdatera `tidslinje.md` med romanens interna händelser.
8. Uppdatera `kontinuitetsanteckningar.md` och vid behov karaktärsfiler.
9. Uppdatera `project-index.md`.
10. Kör intern commit med kapitelskydd.
11. Spara och slutverifiera enligt aktivt lagringsläge.
12. Lämna revisionskvittens.

## Leveranskvittens

### ZIP-läge

Svaret ska innehålla:

- vald indata-ZIP
- källrevision
- ny revision
- project-id
- ändrade filer
- kapitelantal och senaste kapitel
- resultat av slutverifiering
- nedladdningsbar ny ZIP

### GitHub-läge

Svaret ska innehålla:

- repository och projektrot
- basbranch och arbetsbranch
- källcommit och ny commit
- källrevision och ny revision
- project-id
- ändrade filer
- kapitelantal och senaste kapitel
- resultat av slutverifiering
- PR-nummer och om PR:n skapades eller uppdaterades

## Metadata som alltid ska vara konsekvent

- titel
- undertitel
- författare
- målgrupp
- genre
- omslagsstatus
- project-id och revision
- senaste godkända kapitel
- nästa rekommenderade steg

Minst `roman-bibel.md`, `synopsis.md`, `projektstatus.md`, `project-index.md` och manifestet ska vara inbördes rimliga.

## Kanoniska filer och ansvar

| Innehåll | Primär fil |
|---|---|
| Maskinläsbar revision och filhashar | `project-manifest.json` |
| Läsbar revisionshistorik | `revision-log.md` |
| Projektfakta och kärnidé | `roman-bibel.md` |
| Handlingsöversikt och baksidestext | `synopsis.md` |
| Kapitelstatus och plan | `kapitelplan.md` |
| Aktuellt läge och nästa steg | `projektstatus.md` |
| Projektändringar | `arbetslogg.md` |
| Romanens interna tid | `tidslinje.md` |
| Fasta fakta och öppna trådar | `kontinuitetsanteckningar.md` |
| Karaktärsfakta | `karaktarer/*.md` |
| Filinventering och synkkontroll | `project-index.md` |
| Kapitelnoteringar | `kapitelnoteringar.md` |
| Publiceringsregler | `publishing/*` |
| Exporthistorik | `exports/exportlogg.md` |

## Klassificera projekt före arbete

- **Verifierbart modernt:** manifest finns och `verify` lyckas.
- **Äldre manifestlöst:** manifest saknas helt; migrera från exakt låst källa.
- **Skadat modernt:** manifest finns men är ogiltigt eller verifieringen misslyckas; reparera från entydig källa eller avbryt.

Kör aldrig `init` ovanpå ett befintligt icke-mallmanifest. Ta inte bort ett trasigt manifest och kalla inte projektet legacy.

## Legacy-migrering i ZIP-läge

1. Lås exakt käll-ZIP och dess SHA-256.
2. Kör `audit-legacy` före uppackning.
3. Stoppa vid osäkra sökvägar, dubbla kapitel, konkurrerande kopior eller befintligt manifest.
4. Packa upp säkert i tom katalog.
5. Bevara befintliga kapitelfiler byte-identiskt.
6. Lägg till aktuell projektstruktur och integritetsverktyg.
7. Skapa separat baslinjerevision med `init --legacy-migration`.
8. Registrera käll-ZIP och ursprungliga kapitelhashar.
9. Paketera och verifiera `r0001-migrerad`.
10. Genomför användarens egentliga ändring som separat nästa revision.

## Legacy-migrering i GitHub-läge

Följ fil 06. Källan ska vara exakt repository, branch och commit-SHA. Befintliga kapitel ska bevaras byte-identiskt i baslinjerevisionen. Migreringen ska vara en separat commit och får inte samtidigt skriva nästa kapitel.

## Reparera modernt projekt

Ett manifest som finns men inte verifierar får inte skrivas över med `init` eller force-läge. Reparera endast från en entydig ZIP-revision eller Git-historik. Dokumentera exakt vilka filer som reparerades. Saknas entydig källa: avbryt.

## Chattsvar vid filbaserat arbete

- Visa normalt inte hela kapiteltexten.
- Visa ändrade filer, kort sammanfattning, viktiga beslut, revisionskvittens och nästa steg.
- En ändring räknas som sparad först efter godkänd slutverifiering i aktivt lagringsläge.
- Kapitelnoteringar ska vara separerade från berättelsetexten.
- Om kanonisk källa saknas eller är oklar: avbryt i stället för att rekonstruera från chatten.

## Publiceringsstandard

Markdown är kanoniskt källformat. EPUB och PDF är exporter.

Kapitelfiler ska börja:

```markdown
# 1. Kapitelrubrik
```

Använd inte ordet `Kapitel` i H1-rubriken.

I EPUB/PDF ska kapitelstart visas som två centrerade, kompakta rader:

```text
1
Kapitelrubrik
```

TOC ska visa:

```text
1. Kapitelrubrik
```

### Exportregler

1. Läs faktiska kapitelfiler i numerisk ordning.
2. Använd endast godkända kapitel enligt projektstatus.
3. Avbryt om manifest, statusfiler och faktiska kapitel inte stämmer.
4. Ändra inte berättelsetext under export utan uttrycklig beställning.
5. Använd `publishing/` och Pandoc när miljön stödjer det.
6. Kapitelnoteringar och arbetsfiler får inte exporteras som bokinnehåll.
7. Logga format, datum, inkluderade kapitel och filnamn i `exports/exportlogg.md`.
8. Uppdatera endast export- och statusmetadata om ingen textrevision beställts.

### EPUB-standard

- Omslag först när det finns.
- Separat titelsida, inte i TOC.
- Navigerbar TOC, normalt utan synlig TOC-sida i bokflödet.
- TOC-depth normalt 1.
- `nav.xhtml` ska behållas som navigeringsindex; använd normalt `linear="no"` om den ligger i spine.
- Kapitelrubriker får inte ha extra `page-break-before` som skapar tom sida.
- Kapitelnoteringar, arbetslogg och romanbibel ska inte ingå.

### PDF-standard

- Standardordning: omslag, titelsida, eventuell klickbar TOC, kapitel.
- Kapitelrubriker ska vara centrerade och kompakta.
- Undvik tomma sidor och tabeller utanför sidbredd.

### Normalisering före export

- kontrollera titel, undertitel och författare
- sortera kapitel numeriskt
- normalisera rubriker, listor, tabeller och markdownmarkörer
- kontrollera att ingen rå markdown återstår
- kontrollera TOC och kapitelstart
- kontrollera att TOC-länkar inte går till tom sida

## Rekommenderad project-index

`project-index.md` bör minst redovisa:

- project-id
- revision och källrevision
- aktivt lagringsläge
- ZIP-fil eller GitHub-repository/branch när modellen stödjer detta
- titel, undertitel och författare
- projektfas
- senaste och nästa kapitel
- omslagsstatus
- kapitelinventering med SHA-256
- kanoniska projektfiler
- integritetskontroll
- synkkontroll

Fälten för lagringsmetadata införs fullt ut när projektmallen och integritetsverktyget uppdateras i ett senare implementeringssteg.
