# Status – Romanskaparen

**Produktversion:** 1.0.0  
**Migration:** GPT Byggaren 1.5.1  
**Tillstånd:** Maintenance

## Migrationssteg

- [x] Steg 1 – Stateful 1.5-projektmodell och plattformsneutrala kontrakt
- [x] Steg 2 – Test/eval-kontrakt för state, revisioner och failure gates
- [x] Steg 3 – OpenCode peer-runtime och fördjupad Claude-bedömning
- [x] Steg 4 – Runtime parity och modern releaseleverans
- [x] Steg 5 – Slutregression, hygiene och reproducerbar release

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
- OpenCode: ready / active
- Claude Projects: reduced / inactive
- OpenAI Plugin: ready / active (`ready_runtime_dependent`)

## Verifiering av steg 1

CI passerade GPT Builder 1.5 stateful-linten tillsammans med project-template-bundle-synk, befintliga Chat/Custom-byggen, distributionsvalidering och artifact upload. Den befintliga romanmetoden, source-ZIP-regeln och project_integrity.py har inte ändrats.

## Verifiering av steg 2

CI passerade GPT Builder-testmanifestet, 12 stateful behavioral failure-cases och en exekverad project_integrity-svit. Den senare verifierar bland annat revision +1, parent/source revision, allow-list-blockering, fel expected revision, att audit-legacy avvisar moderna manifest samt att init inte skriver över ett trasigt modernt manifest. Live-runtime-scenarier hålls separat från de deterministiska CI-testerna.

## Verifiering av steg 3

CI passerade OpenCode-build och runtime-validering tillsammans med Chat/Custom, GPT Builder-testkontraktet, project_integrity state-transition-testerna och de 12 behavioral failure-casen. OpenCode-paketet innehåller canonical instruktion, Knowledge, hela romanprojektmallen och exakt samma project_integrity.py som projektmallen. project-manifest.json är fortsatt auktoritativ state och native filesystem/shell/archive används för deterministiska transaktioner.

Claude Projects förblir reduced/inactive eftersom deterministic ZIP transaction och project_integrity.py-exekveringsparity inte är verifierad. OpenAI Plugin är nu aktiv som skills-first peer-runtime med explicita hostkrav och `project_integrity.py` som required script resource.

## Verifiering av steg 4

Runtime parity omfattar alla fem bedömda runtimes. Aktiva peers är ChatGPT Chat, Custom GPT, OpenCode och OpenAI Plugin; Claude Projects är fortsatt reduced/inactive. Releaseleveransen bygger Project ZIP samt fyra aktiva runtime-ZIP:ar, SHA256SUMS.txt och DELIVERY-MANIFEST.json.

## Verifiering av steg 5

Slutkörningen passerade hela stateful test- och releasekedjan inklusive final project hygiene, workflow parity och reproducerbarhetskontroll. Reproducerbarhetsgrinden byggde Project, Chat, Custom GPT och OpenCode samt SHA256SUMS.txt och DELIVERY-MANIFEST.json två gånger och verifierade identiska SHA-256-hashar.

## Aktuellt läge

GPT Byggaren 1.5.1-pluginjusteringen är implementerad och valideras i aktuell PR. Efter grön CI återgår projektet till **maintenance-läge**.

## Blockerare

Inga.
