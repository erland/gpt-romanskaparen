# Installera Romanskaparen som Custom GPT

## 1. Skapa GPT:n

Öppna GPT Builder i ChatGPT och skapa en ny GPT.

Rekommenderade grunduppgifter:

- Namn: `Romanskaparen`
- Beskrivning: `En guidande skrivpartner för planering, skrivande, revision och export av romansprojekt.`

## 2. Instructions

Kopiera hela innehållet i:

```text
instructions.md
```

in i GPT:ns Instructions-fält.

## 3. Knowledge

Ladda upp exakt dessa sju filer:

```text
knowledge/01-arbetsflode-och-nyborjarstod.md
knowledge/02-berattelsehantverk.md
knowledge/03-karaktarer-varld-och-kontinuitet.md
knowledge/04-genreguider.md
knowledge/05-projektstruktur-och-synk.md
knowledge/06-verktyg-och-lagringskapaciteter.md
project-template-bundle.md
```

Ladda inte upp `core/templates/romanprojekt/` fil för fil. Bundle-filen innehåller hela projektmallen och `scripts/project_integrity.py`.

## 4. Conversation starters

Kopiera önskade rader från `conversation-starters.md`.

## 5. Capabilities

Aktivera:

- Code Interpreter / Data Analysis – obligatoriskt för ZIP, SHA-256, integritetsverktyg och export.
- Image generation – valfritt för omslag och konceptbilder.
- Web browsing – valfritt för research.

Externa appar eller anslutningar är inte obligatoriska. GPT:n ska fungera fullt i ZIP-läge utan dem.

## 6. Första test

Testa i denna ordning:

1. Starta ett litet nytt romanprojekt.
2. Skapa projekt-ZIP revision 0.
3. Skriv ett kort första kapitel och skapa nästa revision.
4. Fortsätt från den nya ZIP-filen.
5. Revidera endast kapitel 1 och kontrollera att andra kapitel inte ändras.
6. Skapa en EPUB-export.

## Begränsningar

Custom GPT Edition ska inte anta att GitHub eller annan extern skrivanslutning finns. Sådana funktioner får endast användas efter ett godkänt kapacitetstest enligt knowledge-fil 06.