# Projektstruktur, versionslås, synk och exportregler

Detta dokument beskriver den fasta projektstrukturen samt det transaktionsbaserade arbetssätt som Romanskaparen ska använda för att aldrig blanda projektversioner eller återinföra äldre kapitel. Det är den detaljerade och bindande verkställighetsmanualen för källval, legacy-migrering, verifiering, integritetskommandon, tillåtna ändringar, revisioner, paketering, reparation och export. Huvudinstruktionen anger huvudreglerna; detta dokument anger hur de ska genomföras.

## Grundregel
Det ska alltid finnas **en** kanonisk uppsättning projektfiler och **en** entydigt vald indata-revision för varje arbetssteg. Skapa inte parallella statusfiler, alternativa översikter eller tillfälliga sammanfattningsfiler med andra namn när motsvarande fast fil redan finns.

## Begränsning som arbetsflödet måste ta höjd för
En fil som har förekommit tidigare i chatten är inte automatiskt en säker aktuell källa. Romanskaparen får därför aldrig anta att den fil som råkar vara åtkomlig eller har det mest övertygande namnet är den senaste. Säkerheten ska komma från explicit källval, monotona revisionsnummer, manifest och hashkontroll.

## Val av kanonisk indata-zip
Före varje åtgärd som läser eller ändrar ett projekt:
1. Välj exakt en indata-zip.
2. Prioritera den zip som användaren uttryckligen bifogat eller namngivit i sitt aktuella meddelande.
3. Om den namngivna zipen inte är åtkomlig: avbryt. Välj inte en liknande eller äldre fil som ersättning.
4. Om flera zip-filer är bifogade utan att en pekats ut: avbryt filändringen i stället för att gissa.
5. Använd aldrig en gammal extraherad arbetskatalog.
6. Blanda aldrig filer från flera zip-paket, chattext, EPUB/PDF eller tidigare genererade arbetsfiler.
7. Om användaren uttryckligen hänvisar till en högre revision än den valda zipens manifest: avbryt.

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
    kapitel-XX.md  # skapas först när kapitlet faktiskt finns
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

## Projektmanifest och revisioner
`project-manifest.json` är projektets maskinläsbara revisionslås. Det ska minst innehålla:
- ett stabilt `project_id` som aldrig byts för samma romanprojekt
- `project_slug`
- heltalsfältet `revision`
- `parent_revision`
- tidsstämplar
- det kanoniska zip-filnamnet
- hash och filstorlek för varje spårad fil
- separat kapitelöversikt med SHA-256 för varje `kapitel/kapitel-XX.md`
- senaste operation, källrevision och ändrade filer

Manifestet hashar inte sig självt. `revision-log.md` är en läsbar, append-only revisionshistorik. En ny levererad zip ska alltid ha exakt föregående revision + 1. Revisionsnummer får inte återanvändas.

Zip-filer ska heta exempelvis:
- `granslinjen-r0026-kapitel-26.zip`
- `granslinjen-r0027-revision-kapitel-04.zip`
- `granslinjen-r0028-omslag.zip`

Använd inte ord som `ny`, `senaste`, `korrekt`, `komplett`, `uppdaterad` eller suffix som `(1)` som enda versionsidentifierare.

## Deterministiskt integritetsverktyg
Varje projekt ska innehålla `scripts/project_integrity.py`. Standardkommandon:

```bash
python scripts/project_integrity.py verify .
python scripts/project_integrity.py status .
```

För ett äldre projekt där `project-manifest.json` saknas helt ska den aktuella skriptversionen först köras från en tillfällig katalog direkt mot zipen:

```bash
python /tmp/project_integrity.py audit-legacy <indata.zip> \
  --output /tmp/<projekt-slug>-legacy-audit.json
```

Packa därefter upp exakt den auditerade zipen säkert, kopiera in den aktuella skriptversionen och skapa den första revisionslåsta baslinjen:

```bash
python scripts/project_integrity.py init . \
  --slug <projekt-slug> \
  --revision 1 \
  --zip-name <projekt-slug>-r0001-migrerad.zip \
  --source-zip-name <indata.zip> \
  --legacy-migration \
  --legacy-audit /tmp/<projekt-slug>-legacy-audit.json \
  --operation "Migrerade äldre projekt till revisionslåst format"
```

`init` får aldrig köras ovanpå ett befintligt icke-mallmanifest. Om manifestet finns men är trasigt eller inte verifierar är det ett reparationsfall, inte ett legacy-fall.

För att skapa nästa revision efter en ändring:

```bash
python scripts/project_integrity.py commit . \
  --expected-revision <gammal-revision> \
  --operation "<kort beskrivning>" \
  --zip-name <nytt-filnamn.zip> \
  --source-zip-name <indata.zip> \
  --allow '<tillåten/sökväg>'
```

`--allow` anges en gång per fil eller globmönster som får ändras. Verktyget ska stoppa om någon annan fil har ändrats, lagts till eller försvunnit.

## Filtransaktion för varje projektändring
Följ alltid denna ordning:

### Fas A – lås och verifiera källan
1. Skapa en helt ny tom arbetskatalog.
2. Packa upp endast den valda indata-zipen där.
3. Kontrollera att zipen har exakt en projektnivå och inte innehåller flera konkurrerande projektträd.
4. Kör `verify` innan någon fil ändras.
5. Läs `project_id`, revision, kapitelantal, senaste kapitel och kapitelhashar.
6. Kontrollera dubbletter: det får inte finnas flera filer som representerar samma kapitelnummer.
7. Kontrollera att inga kapitel finns gömda under namn som `kapitel-04-ny.md`, `kapitel-04-old.md`, `kapitel-04(1).md` eller i reservkataloger. Sådana filer ska rapporteras och projektet repareras innan fortsatt skrivande.

### Fas B – gör endast den beställda ändringen
1. Skapa en explicit tillåten ändringslista innan du börjar.
2. Vid **nytt kapitel** får en ny `kapitel/kapitel-XX.md` skapas, men inga befintliga kapitelfiler ändras.
3. Vid **revision av kapitel X** får endast `kapitel/kapitel-XX.md` ändras bland kapitelfilerna.
4. Vid **status-, metadata- eller exportarbete** får inga kapitelfiler ändras om användaren inte uttryckligen har begärt textredigering.
5. Vanliga synkfiler får ändras endast när åtgärden kräver det: `kapitelplan.md`, `projektstatus.md`, `arbetslogg.md`, `tidslinje.md`, `kontinuitetsanteckningar.md`, karaktärsfiler, `kapitelnoteringar.md`, `project-index.md`, publicerings- och exportfiler.
6. Kopiera aldrig tillbaka ett kapitel från en annan zip eller från chatten för att "fylla ett hål".

### Fas C – commit och kontroll av oförändrade kapitel
1. Kör `status` och granska väntande ändringar.
2. Kör `commit` med `--expected-revision` och strikt `--allow`-lista.
3. Commit ska öka revisionen exakt med 1 och uppdatera manifest och revisionslogg.
4. Alla kapitelfiler utanför den uttryckligen tillåtna målfilen måste ha samma SHA-256 som i indata-revisionen.
5. Om ett oförändrat kapitel har annan hash: avbryt och leverera ingen zip.

### Fas D – paketera och verifiera leveransen
1. Skapa zipen från hela den nya projektkatalogen, inte från en blandning av gamla och nya filer.
2. Packa upp den färdiga zipen i ytterligare en ny tom kontrollkatalog.
3. Kör `python scripts/project_integrity.py verify .` i kontrollkatalogen.
4. Kontrollera antal kapitel, första/sista kapitel, saknade nummer och att zip-filnamnet stämmer med manifestet.
5. Leverera endast om kontrollen är godkänd.

## Leveranskvittens i chatten
Efter varje uppdaterad projekt-zip ska svaret innehålla:
- vald indata-zip
- källrevision
- ny revision
- project-id
- exakt lista över ändrade filer
- antal kapitel och senaste kapitel
- resultat av slutverifieringen

Detta gör det möjligt för användaren att i nästa meddelande hänvisa till ett exakt filnamn och revisionsnummer.

## Metadata som alltid ska finnas
Följande metadata ska hållas konsekventa i projektets kanoniska filer:
- titel
- undertitel
- författare
- målgrupp
- genre
- status för omslagsbild
- project-id och revision
- senaste godkända kapitel
- nästa rekommenderade steg

Minst `roman-bibel.md`, `synopsis.md`, `projektstatus.md`, `project-index.md` och manifestet ska vara inbördes rimliga.

## Kanoniska filer och ansvar

| Innehåll | Primär fil |
|---|---|
| Maskinläsbar revision och filhashar | `project-manifest.json` |
| Läsbar revisionshistorik | `revision-log.md` |
| Projektets titel, undertitel, författare, genre, målgrupp, kärnidé | `roman-bibel.md` |
| Handlingsöversikt och baksidestext | `synopsis.md` |
| Kapitelstatus och plan | `kapitelplan.md` |
| Projektets aktuella läge och nästa steg | `projektstatus.md` |
| Ändringshistorik för innehållsarbetet | `arbetslogg.md` |
| Händelser i romanens interna tid | `tidslinje.md` |
| Fasta fakta, ledtrådar, öppna trådar | `kontinuitetsanteckningar.md` |
| Karaktärsfakta | `karaktarer/*.md` och sammanfattning i `roman-bibel.md` |
| Filinventering, exportstatus och synkkontroll | `project-index.md` |
| Kapitelnoteringar och uppföljning | `kapitelnoteringar.md` |
| Publiceringsmetadata och sättningsregler | `publishing/*` |
| Exportmetadata | `exports/exportlogg.md` |

## Synkpassering efter varje skapat, reviderat eller godkänt kapitel
När projektfiler används ska en ny verifierad zip skapas i samma svar. Gör alltid detta före leverans:
1. Spara endast berättelsetexten som `kapitel/kapitel-XX.md`. Kapitelnoteringar ska aldrig ligga i kapitelfilen.
2. Spara kapitelnoteringar i `kapitelnoteringar.md` under separat rubrik för kapitlet.
3. Uppdatera raden för kapitlet i `kapitelplan.md`.
4. Lägg till nästa planerade kapitel om planen har vuxit.
5. Uppdatera `projektstatus.md`.
6. Lägg exakt en ny rad i `arbetslogg.md`.
7. Uppdatera `tidslinje.md` med romanens händelser, inte projektarbetets händelser.
8. Uppdatera `kontinuitetsanteckningar.md` och vid behov karaktärsfiler.
9. Uppdatera `project-index.md`.
10. Kör commit med en ändringslista som uttryckligen skyddar övriga kapitelfiler.
11. Paketera, återöppna och verifiera zipen.
12. Leverera zipen och en revisionskvittens.

## Reparera eller migrera uppladdade projekt

### Klassificera innan arbete
- **Verifierbart modernt projekt:** manifest finns och `verify` lyckas. Fortsätt normalt.
- **Äldre manifestlöst projekt:** manifest saknas helt. Kör legacy-migrering.
- **Skadat modernt projekt:** manifest finns men är ogiltigt eller verifieringen misslyckas. Kör inte `init`, ta inte bort manifestet och kalla inte projektet legacy. Reparera endast från en entydig källrevision eller avbryt.

### Legacy-migrering av äldre zip
1. Använd endast den explicit valda zipen.
2. Kör `audit-legacy` mot zipen före uppackning. Auditen ska låsa källzipens SHA-256 och SHA-256 för varje kanonisk kapitelfil.
3. Stoppa om zipen innehåller dubbla sökvägar, osäkra sökvägar, ett befintligt manifest, konkurrerande kapitelkopior eller en möjlig kapitelfil med icke-kanoniskt namn som `kapitel-04-ny.md`.
4. Tomma/mallartade kapitel och luckor ska rapporteras och jämföras med `kapitelplan.md`, `projektstatus.md`, `arbetslogg.md` och `project-index.md`. Om dokumenten gör det oklart om ett kapitel är verkligt skapat: stoppa och begär användarens val.
5. Packa upp den auditerade zipen säkert i en ny tom katalog. Kapiteltexterna i exakt denna zip är baslinjen; påstå inte att de är senaste utanför zipen.
6. Lägg till den aktuella `scripts/project_integrity.py` och saknade moderna administrations-/strukturkomponenter. Befintliga kapitelfiler får inte ens normaliseras beträffande radslut, kodning eller rubrikformat under migreringen.
7. Kör `init --legacy-migration --legacy-audit ... --revision 1`. Verktyget jämför kapitlen med auditens ursprungshashar och stoppar vid minsta avvikelse.
8. Manifestets `migration`-objekt ska registrera källzip, källzipens hash, ursprungliga kapitelhashar, att manifest saknades och att kapitelfilerna bevarades byte-identiskt.
9. Skapa och verifiera `<slug>-r0001-migrerad.zip`. Migreringen får bara lägga till/synka projektadministration och får inte samtidigt skriva nästa kapitel.
10. Utför därefter användarens egentliga åtgärd som en vanlig separat commit, normalt revision 2. Om båda görs i samma svar måste revisionsloggen ändå innehålla två tydliga transaktioner.

### Reparera ett modernt projekt
Ett manifest som finns men inte verifierar får inte skrivas över med `init` eller `--force`. Kontrollera först om den valda zipen själv innehåller tillräcklig information för en säker reparation. Alla reparationer ska dokumentera exakt vilka filer som återställdes eller registrerades och levereras som en separat reparationsrevision. Saknas entydig källa ska arbetet avbrytas.

## Chattsvar vid filbaserat romanskrivande
När projektfiler finns eller skapas ska Romanskaparen normalt arbeta filbaserat:
- Visa inte hela kapiteltexten i chatten.
- Visa ändrade filer, kort sammanfattning, viktiga beslut, revisionskvittens och nästa steg.
- Skapa alltid en ny verifierad projekt-zip efter kapitelarbete eller annan ändring som ska sparas.
- Om korrekt projekt-zip saknas: avbryt filändringen; återskapa inte projektet från chatten.
- Kapitelnoteringar ska alltid separeras från berättelsetexten.

## Publiceringsstandard
Markdown är källformatet. `publishing/` innehåller återanvändbara regler för EPUB/PDF-sättning. Om katalogen saknas i ett äldre projekt ska den skapas när projektet uppdateras eller exporteras.

`publishing/metadata.yaml` ska samla titel, undertitel, författare, språk, rättigheter, omslagsfil och eventuell publisher/ISBN. `publishing/epub.css` styr EPUB-layout. `publishing/pdf-template.tex` styr PDF-layout. `publishing/build-notes.md` beskriver exakt hur exporten skapades och vilka avsteg som gjorts. `publishing/fix-epub-after-pandoc.py` kan användas efter Pandoc för att göra `nav.xhtml` icke-linjär i spine, behålla navigeringsindexet i EPUB-läsaren och neutralisera sidbrytningar på kapitelrubriker.

## Kapitelrubriker för manus och export
Kapitelfiler ska ha en enkel H1-rubrik i formen:

```markdown
# 1. Kapitelrubrik
```

Använd alltså bara numret i kapitelrubrikens nummerdel, inte ordet ”Kapitel”. I EPUB/PDF ska rubriken sättas som två centrerade rader:

```text
1
Kapitelrubrik
```

Rubrikraderna ska vara tydliga men kompakta. I EPUB bör `.chapter-number` vara cirka `font-size: 1.45em` och `.chapter-title` cirka `font-size: 1.30em`. Marginaler bör vara ungefär `h1 margin-top: 0.8em`, `h1 margin-bottom: 0.35em`, `.chapter-number margin-bottom: 0.08em` och `.chapter-title margin-bottom: 0.20em`. I innehållsförteckningen ska samma kapitel visas som `1. Kapitelrubrik`.

## Exportregler: EPUB och PDF
EPUB och PDF är exporter, inte romanens kanoniska källor. Kapiteltexterna i `kapitel/kapitel-XX.md` är alltid originalet.

När användaren ber om EPUB, PDF eller liknande export:
1. Läs faktiska kapitel i `kapitel/` och sortera dem numeriskt.
2. Använd endast godkända/färdiga kapitel om projektstatus anger detta.
3. Om statusfiler, manifest och faktiska kapitelfiler skiljer sig: avbryt exporten och reparera projektet först. Exportera inte från en inkonsekvent revision.
4. Ändra inte kapiteltexter under export om användaren inte uttryckligen ber om redigering.
5. Skapa EPUB/PDF med Pandoc när miljön stödjer det och använd mallarna i `publishing/`. För EPUB ska Pandoc skapa navigeringsindex/TOC, normalt med `--toc --toc-depth=1` eller motsvarande metadata.
6. Skapa EPUB/PDF som separata nedladdningsfiler. De behöver normalt inte packas in i romanprojektets zip om inte användaren ber om det.
7. Uppdatera projektzipen endast med exportmetadata, till exempel `exports/README.md`, `exports/exportlogg.md`, `publishing/build-notes.md`, `projektstatus.md` och `project-index.md`.
8. Skriv exportdatum, format, inkluderade kapitel och filnamn i exportloggen.
9. Om EPUB/PDF inte kan skapas i aktuell miljö, skapa en samlad Markdown-export i stället och beskriv vad som saknas.


## EPUB-standard
- Omslag ska vara första sidan när omslag finns.
- Titelsida ska vara separat och inte ingå i TOC.
- EPUB ska ha navigerbar TOC/index i EPUB-läsaren, men synlig innehållsförteckning i bokflödet ska bara skapas om användaren uttryckligen önskar det. Skapa därför inte en egen Markdown-sida/sektion med rubriken `Innehållsförteckning` för EPUB-standardexport.
- Om Pandoc skapar `nav.xhtml` ska den finnas kvar i EPUB-manifestet med nav-egenskap så EPUB-läsaren får ett index. Om `nav.xhtml` ligger i spine/bokflödet ska den normalt sättas till `linear="no"`; ta bara bort spine-posten om du har kontrollerat att läsarens navigeringsindex fortfarande finns.
- TOC ska normalt bara innehålla översta rubriknivån.
- Kapitelnoteringar, arbetsloggar och romanbibel ska aldrig exporteras som bokinnehåll.
- Kapitelrubriker ska visas centrerat enligt standarden ovan och utan tom startsida före varje kapitel.
- I EPUB-CSS får kapitelrubriken inte ha `page-break-before: always` eller `break-before: page`, eftersom varje kapitel redan ligger i egen XHTML-fil och sådana regler kan göra att TOC-länkar öppnar en tom sida före kapitlet.

## PDF-standard
- PDF ska efterlikna EPUB-layouten så långt möjligt.
- Standardordning: omslag, titelsida, eventuell klickbar innehållsförteckning, kapitel.
- Om användaren ber om PDF med innehållsförteckning ska den vara klickbar.
- Kapitelrubriker ska visas centrerat enligt standarden ovan och utan onödigt stort tomrum.
- Undvik tomma sidor mellan kapitel.
- Tabeller ska anpassas så att de inte går utanför sidbredden.

## Normalisering före export
För att minska variation mellan olika exporttillfällen ska Romanskaparen alltid normalisera exportunderlaget före EPUB/PDF:
- Säkerställ att titel, undertitel och författare finns med.
- Säkerställ att kapitel är i korrekt numerisk ordning.
- Konvertera rubriker till riktiga rubriker.
- Säkerställ att fetstil och kursiv stil använder korrekta och balanserade markörer.
- Säkerställ att listor har korrekt radbrytning och tomrad där det behövs.
- Använd tabeller bara om exportverktyget stöder dem; annars skriv om dem till listor.
- Låt inte råa markdown-markörer som `#`, `##`, `###`, `**`, `__` eller `_` ligga kvar synliga i slutdokumentet utanför kodblock.
- Bevara kodblock som kodblock.
- Kontrollera att innehållsförteckningen visar `1. Kapitelrubrik` medan kapitelstarten visar numret och rubriken på två separata centrerade rader.
- Kontrollera att innehållsförteckning, kapitelrubriker och scenavdelare renderas konsekvent.
- Kontrollera att det inte finns en synlig TOC-sida i bokflödet om användaren inte bett om det, men att EPUB-läsarens navigerings-TOC/index fortfarande finns.
- Kontrollera att TOC-länkar går direkt till kapiteltextens första sida och inte till en tom sida.

## Enkel exportkontroll
Innan slutlig EPUB/PDF levereras ska Romanskaparen kontrollera:
- Hur många kapitel som inkluderats
- Första och sista inkluderade kapitel
- Om något kapitelnummer saknas
- Om titel, undertitel och författare finns
- Om rå markdown ser ut att återstå i exportunderlaget
- Om `nav.xhtml` råkat hamna som synlig sida i spine, och i så fall sätt `linear="no"` utan att ta bort EPUB-läsarens navigeringsindex
- Om EPUB-CSS innehåller `page-break-before: always` eller `break-before: page` på kapitelrubriker
- Om exportloggen ska uppdateras i projektzipen

## Rekommenderat project-index.md
```markdown
# Project Index

## Projekt
- Project-id:
- Revision:
- Källrevision:
- Kanonisk zip-fil:
- Titel:
- Undertitel:
- Författare:
- Senast uppdaterad:
- Nuvarande fas:
- Senast godkända kapitel:
- Nästa kapitel:
- Omslagsbild: Planerad / Skapad / Saknas

## Kapitelinventering
| Kapitel | Fil | Titel | Status | SHA-256 |
|---|---|---|---|---|

## Kanoniska projektfiler
| Fil | Syfte | Status |
|---|---|---|
| project-manifest.json | Revision och filhashar | OK |
| revision-log.md | Revisionshistorik | OK |
| scripts/project_integrity.py | Integritetskontroll | OK |
| README.md | Start och arbetsflöde | OK |
| roman-bibel.md | Centrala fakta | OK |
| synopsis.md | Handlingsöversikt | OK |
| kapitelplan.md | Kapitelplan och status | OK |
| projektstatus.md | Senaste status och nästa steg | OK |
| arbetslogg.md | Projektändringar | OK |
| tidslinje.md | Händelser i romanen | OK |
| kontinuitetsanteckningar.md | Fakta och öppna trådar | OK |
| kapitelnoteringar.md | Kapitelnoteringar utanför kapitelfiler | OK |
| publishing/metadata.yaml | Publiceringsmetadata | OK |
| publishing/epub.css | EPUB-stil | OK |
| publishing/pdf-template.tex | PDF-mall | OK |
| publishing/build-notes.md | Exportinstruktioner | OK |
| exports/exportlogg.md | Exporthistorik | OK |

## Integritetskontroll
- Indata verifierad före ändring: Ja / Nej
- Oförändrade kapitelfiler byte-identiska: Ja / Nej
- Leveranszip återöppnad och verifierad: Ja / Nej
- Verifierad revision:

## Synkkontroll
- Kapitel i `kapitel/`:
- Senaste kapitel i `kapitelplan.md`:
- Senaste kapitel i `projektstatus.md`:
- Senaste kapitel i `arbetslogg.md`:
- Senaste export:
- Resultat: Synkad / Behöver repareras
```
