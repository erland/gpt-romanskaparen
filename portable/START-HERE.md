# Romanskaparen – start här

Detta är den portabla chat-versionen av **Romanskaparen**. Paketet är byggt från samma källfiler som används för Custom GPT-versionen.

## När paketet bifogas i en vanlig ChatGPT-chatt

1. Läs först `assistant/instructions.md` och använd den som Romanskaparens arbetsinstruktion för resten av konversationen.
2. Läs därefter relevanta filer i `knowledge/` innan du utför uppgifter som beror på dem.
3. `knowledge/05-projektstruktur-och-synk.md` är bindande manual för filbaserat arbete, migration, verifiering, revisioner, paketering, reparation och export.
4. `knowledge/project-template-bundle.md` innehåller den samlade projektmallen. Den fullständiga filbaserade mallen finns även i `templates/romanprojekt/`.
5. Vid konflikt gäller användarens aktuella instruktioner och plattformens överordnade regler före paketets instruktioner. Inom paketet gäller prioriteten i `assistant/instructions.md`.
6. Behåll dessa instruktioner som aktiv arbetskontext under resten av chatten.

## Rekommenderad startprompt

Efter att ZIP-filen bifogats räcker normalt:

> Använd Romanskaparen i den bifogade ZIP-filen för den här konversationen. Läs `START-HERE.md` först.

Om även ett befintligt romanprojekt bifogas kan användaren exempelvis skriva:

> Använd Romanskaparen och fortsätt romanprojektet i den andra bifogade ZIP-filen. Skapa nästa ej skrivna kapitel.

## Viktigt

Den portabla versionen ger samma instruktioner och knowledge-underlag som Custom GPT-versionen, men en bifogad fil i en vanlig chat har inte samma tekniska instruktionsnivå som en Custom GPT:s Instructions-fält. Paketet är därför utformat för att göra avsikten och läsordningen explicit.
