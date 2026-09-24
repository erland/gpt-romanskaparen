# Status – Romanskaparen

**Produktversion:** 1.0.0  
**Migration:** GPT Byggaren 1.5.0  
**Tillstånd:** Konvertering pågår

## Migrationssteg

- [x] Steg 1 – Stateful 1.5-projektmodell och plattformsneutrala kontrakt
- [ ] Steg 2 – Test/eval-kontrakt för state, revisioner och failure gates
- [ ] Steg 3 – OpenCode peer-runtime och fördjupad Claude-bedömning
- [ ] Steg 4 – Runtime parity och modern releaseleverans
- [ ] Steg 5 – Slutregression, hygiene och reproducerbar release

## Stateful basis

- `project-manifest.json` är auktoritativ state.
- `revision` ökar exakt med 1 per sparad transaktion.
- `parent_revision` måste peka på källrevisionen.
- exakt en explicit indata-ZIP väljs och låses.
- `project_integrity.py` verifierar före ändring och efter leverans.
- `commit` kräver explicit `--allow`-lista.
- oförändrade kapitel måste behålla identiska SHA-256-hashar.
- projekt får aldrig rekonstrueras från chatthistorik, EPUB eller PDF.

## Runtime-bedömning

- ChatGPT Chat: ready / active
- Custom GPT: ready / active
- OpenCode: ready / planned
- Claude Projects: reduced / inactive
- OpenAI Plugin: reduced / inactive

## Verifiering av steg 1

CI passerade GPT Builder 1.5 stateful-linten tillsammans med project-template-bundle-synk, befintliga Chat/Custom-byggen, distributionsvalidering och artifact upload. Den befintliga romanmetoden, source-ZIP-regeln och project_integrity.py har inte ändrats.

## Aktuellt steg

**Steg 2 – Test/eval-kontrakt för state, revisioner och failure gates.**
