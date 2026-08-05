# Romanprojekt

Detta projekt använder revisionslås, manifest och SHA-256-kontroll för att skydda kapitelversionerna.

Detta är projektarkivet för en roman som utvecklas steg för steg. Projektet har exakt ett kanoniskt lagringsläge åt gången: ZIP eller GitHub.

## Metadata att fastställa tidigt
- Titel
- Undertitel
- Författare
- Genre
- Målgrupp
- Om omslagsbild/framsida ska skapas
- Kanoniskt lagringsläge: ZIP eller GitHub

## Rekommenderat arbetsflöde
1. Planera romankärnan: huvudperson, mål, hinder, insats och förändring.
2. Fastställ titel, undertitel och författare.
3. Avgör om omslagsbild ska skapas nu eller senare.
4. Skapa synopsis, kapitelplan, romanbibel och stilguide.
5. Skriv ett kapitel i taget i chatten.
6. Justera kapitlet tills användaren är nöjd.
7. Uppdatera projektfilerna och projektstatus.
8. Spara och slutverifiera enligt valt lagringsläge.
9. Fortsätt med nästa kapitel, revision eller export.

## Säker filhantering

- `project-manifest.json` anger projekt-id, revision, lagringsläge och hash för varje fil.
- `revision-log.md` visar projektets interna revisioner.
- `scripts/project_integrity.py` verifierar projektet före och efter ändringar.
- Verktygets `audit-legacy`-läge granskar äldre manifestlösa ZIP-filer innan migrering.
- Varje arbetssteg ska utgå från exakt en uttryckligen vald och låst projektkälla.
- ZIP- och GitHub-källor får aldrig blandas i samma operation.
- En ändring är inte sparad förrän den finns i en slutverifierad ZIP eller Git-commit enligt det kanoniska lagringsläget.

### ZIP-läge

- En uttryckligen vald projekt-ZIP är kanonisk källa.
- Varje sparad ändring levereras som nästa verifierade ZIP-revision.
- `canonical_zip_name` anger den aktuella kanoniska ZIP-filen.

### GitHub-läge

- Repository, projektrot, default branch, arbetsbranch och commit-SHA låser källan.
- Repositoryts default branch är basbranch.
- Standardarbetsbranch är `development`, om användaren inte väljer annat.
- Ändringar committas på arbetsbranchen och en PR skapas eller återanvänds mot default branch.
- Användaren ansvarar normalt för merge. Ingen automatisk merge eller force push används.
- Git-SHA lagras inte som obligatoriskt manifestfält; den redovisas i revisionskvittensen och Git-historiken.

Grundkommandon:

```bash
python scripts/project_integrity.py verify .
python scripts/project_integrity.py status .
```

## Viktiga filer
- `projektstatus.md` visar nuvarande fas, lagringsläge, senaste godkända kapitel och nästa rekommenderade steg.
- `project-index.md` visar projektkälla, revision, synk och integritetsstatus.
- `roman-bibel.md` innehåller projektets centrala fakta.
- `synopsis.md` sammanfattar hela handlingen.
- `kapitelplan.md` är färdplanen för romanen.
- `stilguide.md` håller språk, ton och perspektiv konsekvent.
- `tidslinje.md` håller ordning på händelser.
- `kontinuitetsanteckningar.md` fångar fakta som inte får motsägas.
- `revisionsonskemal.md` samlar planerade förbättringar.
- `arbetslogg.md` visar vad som har gjorts.
- `kapitel/` innehåller kapitelutkast och godkända kapitel.
- `exports/exportlogg.md` visar skapade EPUB/PDF- och ZIP-exporter.

## Byte av lagringsläge

Byte mellan ZIP och GitHub är en uttrycklig migreringsoperation. `project_id` ska bevaras, projektrevisionen ska vara sammanhängande och endast ett läge får vara kanoniskt efter migreringen. En ZIP som exporteras från GitHub byter inte automatiskt lagringsläge.

## Publicering
- `publishing/` innehåller metadata och sättningsregler för EPUB/PDF.
- `kapitelnoteringar.md` innehåller anteckningar som inte ska exporteras som boktext.
