# Migration v1.1.0

Canonical ursprungsinstruktion bevarad oförändrad. Fyra modulariserade färdighetsmoduler tillagda. Ursprunglig romanprojektmall, manifestkontrakt och revisionslås bevarade.

## Engine-beslut

En separat stor distributionsmotor behövs inte för Romanskaparens runtime. `project_integrity.py` är däremot en **obligatorisk exekverbar resurs** för filbaserat arbete. Distributionen får bära en kopia av skriptet, men kan bara fullfölja revisionssäkra transaktioner om värden erbjuder Python, arbetsyta och ZIP-hantering. Claude Project och Plugin måste därför kontrollera detta per körning; annars ska arbetsflödet avbrytas, inte simuleras. Det äldre valfria `publishing`-skriptet och projektmallarna bevaras.

## Avgränsning

Deterministiska lokala tester verifierar paket och kodkontrakt; faktisk körning i ChatGPT Plugin eller Claude kan inte intygas av ett lokalt bygge.

## Kontroller vid release

`python scripts/lint_gpt_project.py --project-root .`, `python scripts/test_project_integrity_contract.py`, `python scripts/validate_stateful_behavior_contract.py`, `python scripts/validate_workflow_parity.py`, `python scripts/build_distributions.py --project-root . --version <version> --targets project,chat,plugin,claude_project,claude_skills,opencode`, `python scripts/validate_distributions.py --project-root .` och `python scripts/validate_release_readiness.py --version <version>`.

Äldre skript för Custom GPT och den äldre distributören kvarstår enbart som historiska resurser och ska inte användas för nya releaser.
