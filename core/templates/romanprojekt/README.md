# Romanprojekt

Detta projekt använder revisionslås, manifest och SHA-256-kontroll för att skydda kapitelversionerna.

Detta är projektarkivet för en roman som utvecklas steg för steg.

## Metadata att fastställa tidigt
- Titel
- Undertitel
- Författare
- Genre
- Målgrupp
- Om omslagsbild/framsida ska skapas

## Rekommenderat arbetsflöde
1. Planera romankärnan: huvudperson, mål, hinder, insats och förändring.
2. Fastställ titel, undertitel och författare.
3. Avgör om omslagsbild ska skapas nu eller senare.
4. Skapa synopsis, kapitelplan, romanbibel och stilguide.
5. Skriv ett kapitel i taget i chatten.
6. Justera kapitlet tills användaren är nöjd.
7. Uppdatera projektfilerna och projektstatus.
8. Fortsätt med nästa kapitel, revision eller export.

## Säker filhantering

- `project-manifest.json` anger projekt-id, revision och hash för varje fil.
- `revision-log.md` visar levererade revisioner.
- `scripts/project_integrity.py` verifierar projektet före och efter ändringar.
- Verktygets `audit-legacy`-läge granskar äldre manifestlösa zippar innan migrering.
- Varje nytt arbetssteg ska utgå från exakt en uttryckligen vald projekt-zip.
- En ändring är inte sparad förrän en ny verifierad zip-revision har levererats.

Grundkommandon:

```bash
python scripts/project_integrity.py verify .
python scripts/project_integrity.py status .
```

## Viktiga filer
- `projektstatus.md` visar nuvarande fas, senaste godkända kapitel och nästa rekommenderade steg.
- `roman-bibel.md` innehåller projektets centrala fakta.
- `synopsis.md` sammanfattar hela handlingen.
- `kapitelplan.md` är färdplanen för romanen.
- `stilguide.md` håller språk, ton och perspektiv konsekvent.
- `tidslinje.md` håller ordning på händelser.
- `kontinuitetsanteckningar.md` fångar fakta som inte får motsägas.
- `revisionsonskemal.md` samlar planerade förbättringar.
- `arbetslogg.md` visar vad som har gjorts.
- `kapitel/` innehåller kapitelutkast och godkända kapitel.
- `exports/exportlogg.md` visar skapade EPUB/PDF-exporter.


## Publicering
- `publishing/` innehåller metadata och sättningsregler för EPUB/PDF.
- `kapitelnoteringar.md` innehåller anteckningar som inte ska exporteras som boktext.
