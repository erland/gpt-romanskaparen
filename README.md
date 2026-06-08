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

Ladda upp dessa fem filer från `knowledge-upload/`:

```text
01-arbetsflode-och-nyborjarstod.md
02-berattelsehantverk.md
03-karaktarer-varld-och-kontinuitet.md
04-genreguider.md
05-projektstruktur-och-synk.md
```

Det håller GPT:n långt under gränsen på 20 knowledge-filer. Kopiera `gpt-instructions.md` till Instructions-fältet.

## Viktiga beteenderegler

Romanskaparen ska:

- erbjuda att skapa projekt-zip när ett nytt projekt startas eller större ändringar gjorts
- vid filbaserat arbete normalt inte visa hela kapiteltexten i chatten
- i stället visa ändrade filer, kort sammanfattning, kontinuitetsnoteringar och nästa steg
- spara kapiteltext i `kapitel/kapitel-XX.md`
- spara kapitelnoteringar i `kapitelnoteringar.md`, inte i kapitelfilerna
- hålla `kapitelplan.md`, `projektstatus.md`, `arbetslogg.md`, `tidslinje.md`, `kontinuitetsanteckningar.md` och `project-index.md` synkade

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
