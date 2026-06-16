# Setup för Custom GPT

## Obligatorisk uppladdning

Ladda upp följande sex knowledge-filer:

```text
knowledge-upload/01-arbetsflode-och-nyborjarstod.md
knowledge-upload/02-berattelsehantverk.md
knowledge-upload/03-karaktarer-varld-och-kontinuitet.md
knowledge-upload/04-genreguider.md
knowledge-upload/05-projektstruktur-och-synk.md
project-template-bundle.md
```

Kopiera innehållet i `gpt-instructions.md` till GPT:ns Instructions-fält. Filen är medvetet kompakt; detaljerade migrerings-, verifierings- och kommandoregler finns i `knowledge-upload/05-projektstruktur-och-synk.md`.

Conversation starters finns i `conversation-starters.md`.

## Projektmallen ska laddas upp som en samlad knowledge-fil

Ladda inte upp katalogen `templates/romanprojekt/` fil för fil. Ladda i stället upp `project-template-bundle.md`. Den innehåller den exakta projektstrukturen, manifestmallen och hela integritetsverktyget.

## Katalogen knowledge är borttagen

Tidigare fanns en `knowledge/`-katalog med separata källfiler. Den används inte längre i GPT-uploaden och är borttagen ur paketet för att undvika förvirring och spara filplatser.

## Rekommenderad GPT-konfiguration

- Instructions: använd `gpt-instructions.md`
- Knowledge: använd `knowledge-upload/*.md` samt `project-template-bundle.md`
- Conversation starters: använd `conversation-starters.md`
- Capabilities: aktivera filhantering/code interpreter om GPT:n ska skapa zip-paket, EPUB eller PDF

## Viktigaste inställningen för säker filhantering

Code Interpreter / Data Analysis måste vara aktiverat. Det krävs för att packa upp zip-filer, köra `scripts/project_integrity.py`, beräkna SHA-256 och återverifiera den skapade zipen.

Efter att kunskapsfilerna uppdaterats bör äldre manifestlösa romanprojekt migreras vid nästa uppladdning. GPT:n kör först `audit-legacy` direkt mot zipen, låser källzipens och kapitlens SHA-256, lägger sedan till `project-manifest.json`, `revision-log.md` och den aktuella `scripts/project_integrity.py`, och skapar `r0001-migrerad` som en separat baslinje. Befintliga kapitel måste vara byte-identiska med källzipen.

Om `project-manifest.json` redan finns men är skadat eller inte verifierar ska GPT:n inte köra `init`, radera manifestet eller använda något force-läge. Det är ett reparationsfall som måste lösas från en entydig källrevision eller avbrytas.

## Viktigaste beteenden

- GPT:n ska skapa en ny verifierad projekt-zip varje gång en filbaserad ändring sparas.
- GPT:n ska vid filbaserat arbete normalt inte visa hela kapitel i chatten.
- GPT:n ska visa indatafil, källrevision, ny revision, project-id, ändrade filer och verifieringsresultat.
- Kapitelnoteringar ska sparas i `kapitelnoteringar.md`, inte i kapitelfilerna.
- Kapitelfiler ska använda rubrikformen `# 1. Kapitelrubrik`.
- EPUB/PDF ska visa kapitelstart som två centrerade rader: nummer + rubrik.
- Innehållsförteckningen ska visa `1. Kapitelrubrik`.

## Export till EPUB och PDF

Reglerna i `knowledge-upload/05-projektstruktur-och-synk.md` styr export. Projektmallen innehåller `publishing/metadata.yaml`, `publishing/epub.css`, `publishing/pdf-template.tex` och `publishing/build-notes.md`.
