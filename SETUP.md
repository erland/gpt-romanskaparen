# Setup för Custom GPT

## Rekommenderad uppladdning

Ladda endast upp filerna i:

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

Då blir det totalt 6 knowledge-filer.

## Katalogen knowledge är borttagen

Tidigare fanns en `knowledge/`-katalog med separata källfiler. Den används inte längre i GPT-uploaden och är borttagen ur paketet för att undvika förvirring och spara filplatser.

## Rekommenderad GPT-konfiguration

- Instructions: använd `gpt-instructions.md`
- Knowledge: använd endast `knowledge-upload/*.md`
- Conversation starters: använd `conversation-starters.md`
- Capabilities: aktivera filhantering/code interpreter om GPT:n ska skapa zip-paket, EPUB eller PDF

## Viktigaste beteenden

- GPT:n ska erbjuda projekt-zip när ett nytt romanprojekt startas eller när större ändringar sparas.
- GPT:n ska vid filbaserat arbete normalt inte visa hela kapitel i chatten.
- GPT:n ska visa vilka filer som ändrats, kort sammanfattning och nästa steg.
- Kapitelnoteringar ska sparas i `kapitelnoteringar.md`, inte i kapitelfilerna.
- Kapitelfiler ska använda rubrikformen `# 1. Kapitelrubrik`.
- EPUB/PDF ska visa kapitelstart som två centrerade rader: nummer + rubrik.
- Innehållsförteckningen ska visa `1. Kapitelrubrik`.

## Export till EPUB och PDF

Reglerna i `knowledge-upload/05-projektstruktur-och-synk.md` styr export. Projektmallen innehåller `publishing/metadata.yaml`, `publishing/epub.css`, `publishing/pdf-template.tex` och `publishing/build-notes.md`.
