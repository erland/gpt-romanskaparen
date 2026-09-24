# Konverteringsplan – GPT Byggaren 1.5.0

**Projekt:** Romanskaparen  
**Konverteringstyp:** existing-project-conversion  
**Modellrobusthet:** `stateful`

Den befintliga romanmetoden, filtransaktionsmodellen, projektmallen och `project_integrity.py` ska bevaras. GPT Builder 1.5 ska formalisera dem, inte ersätta dem.

## Steg 1 – Stateful 1.5-projektmodell och plattformsneutrala kontrakt

Inför:
- `gpt-project.yaml`
- `PROJECT.md`
- `STATUS.md`
- `project-status.yaml`
- capability-, artifact-, workspace/state- och tool-kontrakt
- explicit fem-runtime-bedömning
- lint för state authority, source lock, revision +1, allow-list och resume-regler

Auktoritativ state är romanprojektets `project-manifest.json`.

## Steg 2 – Test/eval-kontrakt

Bygg deterministiska och behavioral tester för bland annat:
- exakt en indata-ZIP
- saknad/otillgänglig explicit ZIP
- trasigt manifest får inte behandlas som legacy
- legacy kräver audit före init
- revision +1 och korrekt parent revision
- chapter isolation
- metadata/export får inte ändra kapitel
- otillåten filändring blockerar commit
- failed final verify blockerar leverans
- projekt får inte rekonstrueras från chat/export

## Steg 3 – Peer-runtimes

Bygg OpenCode som aktiv peer-runtime med native filesystem/shell och `project_integrity.py`. Bedöm Claude Projects utifrån faktisk möjlighet till säkra ZIP-transaktioner och deterministisk verifiering.

## Steg 4 – Runtime parity och modern releaseleverans

Inför runtime contracts, fem-runtime parity, Project ZIP, runtimepaket, checksummor, delivery manifest och release readiness.

## Steg 5 – Slutregression, hygiene och reproducerbar release

Verifiera full test/eval-kedja, project hygiene, workflow parity och reproducerbar release.

## Aktuellt steg

**Steg 1 – Stateful 1.5-projektmodell och plattformsneutrala kontrakt.**
