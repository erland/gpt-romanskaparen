# Romanskaparen GPT-paket

Detta paket innehåller material för en Custom GPT som planerar, skriver, reviderar och exporterar romanprojekt steg för steg.

## Rekommenderad GPT-konfiguration

**Namn:** Romanskaparen

**Beskrivning:** En guidande skrivpartner för romanprojekt. Hjälper användaren att utveckla idé, synopsis, karaktärer, kapitelplan, kapiteltext, kontinuitet, projekt-zip samt EPUB/PDF-export.

## Filer

- `gpt-instructions.md` – huvudinstruktioner att klistra in i GPT Builder.
- `conversation-starters.md` – förslag på conversation starters.
- `knowledge-upload/` – de enda filer som normalt ska laddas upp som GPT Knowledge.
- `templates/romanprojekt/` – mall för romanprojekt-zip.
- `project-template-bundle.md` – samlad mallfil om du vill ladda upp projektmallen som extra knowledge-fil.

Katalogen `knowledge/` är borttagen. Den innehöll bara delkällor till de hopslagna filerna i `knowledge-upload/` och behövs inte längre.

## Rekommenderad uppladdning

Ladda upp dessa fem filer från `knowledge-upload/` samt den samlade projektmallen:

```text
knowledge-upload/01-arbetsflode-och-nyborjarstod.md
knowledge-upload/02-berattelsehantverk.md
knowledge-upload/03-karaktarer-varld-och-kontinuitet.md
knowledge-upload/04-genreguider.md
knowledge-upload/05-projektstruktur-och-synk.md
project-template-bundle.md
```

`project-template-bundle.md` är obligatorisk i den filsäkra versionen eftersom den innehåller den exakta mallen för `project-manifest.json` och hela `scripts/project_integrity.py`. Kopiera `gpt-instructions.md` till Instructions-fältet. De detaljerade säkerhets- och kommandoreglerna ligger i `knowledge-upload/05-projektstruktur-och-synk.md`.

## Versionssäker filhantering

Den här versionen använder ett transaktionsbaserat arbetssätt:

- exakt en indata-zip väljs per arbetssteg
- `project-manifest.json` håller project-id, revision och SHA-256-hashar
- `revision-log.md` ger en läsbar revisionskedja
- `scripts/project_integrity.py` stoppar oavsiktliga ändringar av andra kapitel
- `audit-legacy` granskar äldre zippar och låser befintliga kapitelhashar innan migrering
- varje färdig zip återöppnas och verifieras innan leverans
- filnamn använder monotona revisioner, exempelvis `roman-r0012-kapitel-12.zip`

Det viktigaste praktiska användarbeteendet är att bifoga eller namnge den exakta senaste projekt-zipen i varje meddelande som ska ändra projektet. GPT:n ska avbryta i stället för att gissa när källan är oklar eller inte åtkomlig.

### Äldre projektzippar
En zip från en tidigare GPT-version får fortsätta användas när den saknar manifest men är internt entydig. Romanskaparen ska då först auditera zipen, bevara samtliga befintliga kapitel byte-identiskt och skapa `r0001-migrerad` som separat baslinjetransaktion. Ett projekt där manifestet finns men är trasigt får däremot inte behandlas som legacy eller initieras om; det kräver en uttrycklig reparation eller avbrott.

## Viktiga beteenderegler

Romanskaparen ska:

- alltid skapa en ny verifierad projekt-zip när en filbaserad ändring ska sparas
- vid filbaserat arbete normalt inte visa hela kapiteltexten i chatten
- i stället visa ändrade filer, kort sammanfattning, kontinuitetsnoteringar och nästa steg
- spara kapiteltext i `kapitel/kapitel-XX.md`
- spara kapitelnoteringar i `kapitelnoteringar.md`, inte i kapitelfilerna
- hålla `project-manifest.json`, `revision-log.md`, kapitel- och statusfiler synkade samt hashverifiera alla oförändrade kapitel

Visa full kapiteltext i chatten bara när användaren uttryckligen ber om det eller när inget projektpaket används.

## Publiceringsstandard

Markdown är källformat. Projektmallen innehåller `publishing/` med metadata och sättningsregler för Pandoc-baserad EPUB/PDF-export.

Kapitelfiler ska använda:

```markdown
# 1. Kapitelrubrik
```

Vid EPUB/PDF-export ska kapitelstarten visas som två centrerade, kompakta rader:

```text
1
Kapitelrubrik
```

Innehållsförteckningen ska visa:

```text
1. Kapitelrubrik
```

## Rekommenderade capabilities

- Web browsing: Av om romanen inte kräver research.
- Canvas: På om tillgängligt.
- Code interpreter / filskapande: På om GPT:n ska kunna skapa och uppdatera zip-filer.
- Image generation: Valfritt för omslag och konceptbilder.
