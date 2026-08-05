# Custom GPT Edition

Custom GPT Edition är Romanskaparens färdiga distribution för GPT Builder.

## När den passar

- användaren vill ha en färdig specialiserad GPT
- ZIP är tillräcklig som kanonisk projektkälla
- romanprojekt ska kunna skapas, revideras och exporteras utan externa anslutningar

## Installation

Följ `distributions/gpt/INSTALL.md`.

Ladda upp sex knowledge-filer från `distributions/gpt/knowledge/` samt `distributions/gpt/project-template-bundle.md`. Kopiera `distributions/gpt/instructions.md` till Instructions-fältet.

## Kapaciteter

Code Interpreter/Data Analysis är obligatoriskt för fullständigt ZIP-arbete, integritetskontroll och export. Bildgenerering och webbsökning är valfria.

GitHub eller annan extern lagring får inte antas finnas. Sådan lagring får endast aktiveras efter ett godkänt användarspecifikt förmågetest. Om testet misslyckas fortsätter GPT:n i ZIP-läge.

## Underhåll

Filerna under `distributions/gpt/knowledge/`, projektbundlen och manifestet är genererade. Ändra kärnan under `core/` och kör byggskripten.
