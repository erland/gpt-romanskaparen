# Setup för Custom GPT

## Rekommenderad uppladdning

För att hålla dig under gränsen på 20 knowledge-filer, ladda bara upp filerna i:

```text
knowledge-upload/
```

Det är 5 filer:

```text
01-arbetsflode-och-nyborjarstod.md
02-berattelsehantverk.md
03-karaktarer-varld-och-kontinuitet.md
04-genreguider.md
05-projektstruktur-och-synk.md
```

Kopiera innehållet i `gpt-instructions.md` till GPT:ns Instructions-fält.

Conversation starters finns i `conversation-starters.md`.

## Ladda normalt inte upp templates som knowledge

Filerna under `templates/romanprojekt/` är främst mallar för de romanprojekt som GPT:n ska skapa åt användaren. De behöver inte laddas upp som separata knowledge-filer.

Om du vill ge GPT:n en exakt projektmall som knowledge, ladda upp den samlade filen:

```text
project-template-bundle.md
```

Då blir det totalt 6 knowledge-filer, fortfarande långt under gränsen på 20.

## Rekommenderad GPT-konfiguration

- Instructions: använd `gpt-instructions.md`
- Knowledge: använd endast `knowledge-upload/*.md`
- Conversation starters: använd `conversation-starters.md`
- Capabilities: filhantering/code interpreter kan vara användbart om GPT:n ska skapa zip-paket för romanprojekt

## Varför denna struktur?

Custom GPT:er har en praktisk gräns för antal knowledge-filer. Därför är kunskapen samlad i få tematiska filer:

1. Arbetsflöde och nybörjarstöd
2. Berättelsehantverk
3. Karaktärer, värld och kontinuitet
4. Genreguider
5. Projektstruktur, synk och exportregler

Det ger samma stöd men med betydligt färre filer.


## EPUB-export

Romanskaparen kan instrueras att skapa EPUB som separat nedladdningsfil när användaren begär export. Projektzipen behöver då normalt bara uppdateras med exportlogg/status, inte innehålla själva EPUB-filen.


## Rekommenderad användning av titel/författare/omslag

När GPT:n startar ett nytt romanprojekt bör den alltid fråga efter titel, undertitel, författare och om omslagsbild ska skapas. Om författare inte anges ska användarens namn användas som standard när det är tillgängligt.

## Export till EPUB och PDF

Den här versionen är optimerad för mer konsekvent export. Trots det kan viss variation fortfarande uppstå beroende på vilken exportmiljö som används. Reglerna i `05-projektstruktur-och-synk.md` minskar risken genom att kräva normalisering av markdown före export.
