# Romanskaparen – Custom GPT Edition

Detta är den färdiga Custom GPT-distributionen av Romanskaparen 2.0.

Den bygger på den gemensamma kärnan under `core/` och är avsedd för GPT Builder. ZIP-läget är den garanterade filbaserade arbetsformen. Externa anslutningar får endast användas när de faktiskt finns och har verifierad läs- och skrivförmåga.

## Innehåll

- `instructions.md` – klistras in i GPT Builders Instructions-fält.
- `conversation-starters.md` – förslag på startfrågor.
- `knowledge/` – sex knowledge-filer genererade från `core/knowledge/`.
- `project-template-bundle.md` – komplett romanprojektmall och integritetsverktyg.
- `distribution-manifest.json` – maskinläsbar beskrivning av distributionen och dess källor.
- `INSTALL.md` – installationsanvisning.

## Garanterad funktion

När Code Interpreter/Data Analysis är aktiverat ska GPT:n kunna:

- skapa nya revisionslåsta romanprojekt som ZIP
- fortsätta från exakt vald projekt-ZIP
- skriva och revidera kapitel med kapitelskydd
- migrera äldre manifestlösa projekt
- stoppa skadade moderna projekt
- skapa verifierade EPUB- och PDF-exporter

GitHub eller andra externa lagringsformer är villkorliga och får inte lovas utan ett godkänt förmågetest.

## Kanoniska källor

Filerna i denna katalog är distributionsartefakter. De kanoniska källorna finns under:

```text
core/instructions/
core/knowledge/
core/templates/romanprojekt/
core/prompts/
```

Distributionen ska i ett senare steg byggas och valideras automatiskt från kärnan.