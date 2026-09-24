# PROJECT – Romanskaparen

Romanskaparen är en stateful skrivassistent för planering, skrivande, revision, versionshantering och export av romanprojekt.

## Canonical källor

- Huvudinstruktion: `gpt-instructions.md`
- Fil-/transaktionsmanual: `knowledge-upload/05-projektstruktur-och-synk.md`
- Projektmall: `templates/romanprojekt/`
- Genererad projektbundle: `project-template-bundle.md`
- Integritetsverktyg: `templates/romanprojekt/scripts/project_integrity.py`

## GPT Byggaren 1.5-konvertering

Projektet konverteras till GPT Byggaren 1.5.0 utan att ändra romanskrivnings- eller filintegritetsbeteendet.

Robusthetsnivå: **stateful**.

Auktoritativ projektstate:
- `project-manifest.json`
- stabilt `project_id`
- monoton `revision`
- `parent_revision`
- fil- och kapitelhashar
- `last_operation`

Varje filbaserad ändring är en transaktion: välj exakt en explicit indata-ZIP, verifiera, lås revision/hashar, ändra endast explicit tillåtna filer, committa revision +1, paketera hela projektet, återöppna och verifiera leveransen.

Runtime-mål:
- ChatGPT Chat – ready / active
- Custom GPT – ready / active
- OpenCode – ready / planned
- Claude Projects – reduced / inactive tills säker ZIP/script-parity är verifierad
- OpenAI Plugin – reduced / inactive

Migreringsplan: `docs/gpt-builder-1.5-migration-plan.md`.
