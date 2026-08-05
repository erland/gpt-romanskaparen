# Romanskaparen 2.0 – accepteranstestplan

Status: slutlig testplan för Prompt 7

## 1. Syfte

Planen verifierar att Romanskaparen 2.0 kan distribueras både som Custom GPT och som underlag för ett ChatGPT Project utan att kärnregler, projektmall eller revisionsskydd divergerar.

## 2. Automatiska kontroller

Följande ska passera vid varje ändring:

```bash
python3 scripts/build_distributions.py --check
python3 scripts/validate_distributions.py
```

Kontrollerna ska verifiera:

- att båda distributionernas knowledge-filer är byte-identiska med `core/knowledge/`
- att båda bundle-filerna är identiska och genererade från `core/templates/romanprojekt/`
- att distributionsmanifesten är aktuella och markerade som genererade
- att GPT-instruktionen håller gränsen på 8 000 tecken
- att Custom GPT Edition använder högst 20 knowledge-filer och för närvarande exakt 7
- att manuellt ändrade eller stale distributionsartefakter upptäcks

## 3. Custom GPT Edition

### Installation

1. Klistra in `distributions/gpt/instructions.md` i Instructions.
2. Ladda upp de sex filerna i `distributions/gpt/knowledge/`.
3. Ladda upp `distributions/gpt/project-template-bundle.md`.
4. Aktivera Code Interpreter/Data Analysis.
5. Lägg till starters från `conversation-starters.md`.

### Accepteransfall

- starta ett nytt litet romanprojekt och skapa revision 0 som ZIP
- fortsätt från exakt den skapade ZIP-filen och skapa revision 1
- skriv ett nytt kapitel utan att ändra tidigare kapitelfiler
- revidera ett utpekat kapitel utan att ändra andra kapitel
- verifiera att manifest, revisionslogg och SHA-256 uppdateras korrekt
- prova en äldre manifestlös ZIP och skapa en separat migreringsbaslinje
- prova ett projekt med trasigt manifest och verifiera att arbetet stoppas
- skapa EPUB och PDF utan att ändra den kanoniska projektkällan
- verifiera att GitHub inte erbjuds som aktivt stöd utan godkänt kapacitetstest

## 4. ChatGPT Project Edition

### Installation

1. Skapa ett separat ChatGPT Project för en roman.
2. Klistra in `distributions/project/PROJECT-INSTRUCTIONS.md` som projektinstruktion.
3. Ladda upp de sex knowledge-filerna och projektbundlen.
4. Följ `START-HERE.md`.

### Accepteransfall

- starta en ny roman i ett tomt Project
- fortsätt ett befintligt ZIP-projekt i en ny chatt i samma Project
- använd separata chattar för planering, kapitel och redaktion utan att blanda kanoniska källor
- verifiera att Project Memory inte behandlas som ersättning för manifest eller revisionslogg
- testa extern anslutning endast efter användarspecifikt kapacitetstest
- verifiera ZIP-fallback när extern skrivåtkomst saknas eller endast är read-only
- verifiera att material från en annan roman inte återanvänds i projektet

## 5. Bakåtkompatibilitet

- öppna en verifierbar 1.x-ZIP utan formatkonvertering
- bevara `project_id`, revision, kapitelhashar och revisionskedja
- skapa nästa vanliga revision med 2.0
- verifiera att användaren inte tvingas byta från ZIP eller använda GitHub

## 6. Negativa tester

Arbetet ska stoppas utan skrivning när:

- flera konkurrerande projektkällor bifogas
- förväntad källrevision eller hash inte stämmer
- ett modernt manifest finns men inte verifierar
- återläsning av skapad leverans misslyckas
- extern lagringsförmåga inte kan verifieras
- en operation skulle ändra kapitelfiler utanför den uttryckliga beställningen

## 7. Godkännandekriterier

Romanskaparen 2.0 är redo för merge när:

- automatiska bygg- och valideringskontroller passerar
- båda distributionerna kan installeras enligt respektive guide
- ZIP-flödet passerar accepteransfallen
- externa verktyg behandlas villkorligt och användarspecifikt
- dokumentationen pekar på `core/` som enda kanoniska produktkälla
- inga aktiva 1.x-regelkällor finns kvar parallellt i repositoryts rot
