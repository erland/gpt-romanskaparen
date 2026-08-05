# Romanskaparen 2.0

Romanskaparen är en plattformsoberoende skrivpartner för att planera, skriva, revidera och exportera romanprojekt med versionssäker filhantering.

## Distributioner

### Custom GPT Edition

Använd när du vill skapa en egen GPT i GPT Builder. ZIP är den garanterade lagringsformen.

- Installation: `distributions/gpt/INSTALL.md`
- Instruktion: `distributions/gpt/instructions.md`
- Knowledge: sex filer i `distributions/gpt/knowledge/` samt `distributions/gpt/project-template-bundle.md`

### ChatGPT Project Edition

Rekommenderas för långvariga romanprojekt. Skapa ett separat ChatGPT Project per roman.

- Installation: `distributions/project/INSTALL.md`
- Projektinstruktion: `distributions/project/PROJECT-INSTRUCTIONS.md`
- Startguide: `distributions/project/START-HERE.md`
- Knowledge: sex filer i `distributions/project/knowledge/` samt `distributions/project/project-template-bundle.md`

GitHub och andra externa lagringsformer är villkorliga. De får endast användas när den aktuella användarens miljö har verifierad läs-, skriv- och återläsningsförmåga. ZIP fungerar som säker fallback.

## Arkitektur

```text
core/                  kanoniska regler, kunskap och projektmall
distributions/gpt/     genererad Custom GPT-distribution
distributions/project/ genererad ChatGPT Project-distribution
scripts/               bygg- och valideringsverktyg
docs/                  arkitektur, installation och migration
```

Ändra normalt endast `core/` och tunna plattformsspecifika wrapperfiler. Genererade knowledge-kopior, bundles och manifest byggs från kärnan.

## Bygg och validera

```bash
python3 scripts/build_distributions.py
python3 scripts/validate_distributions.py
```

eller:

```bash
bash scripts/build.sh
```

GitHub Actions synkar och validerar distributionerna automatiskt.

## Befintliga romanprojekt

Romanskaparen 2.0 är kompatibel med verifierbara 1.x-projekt. Ett befintligt projekt ska behålla `project_id`, revisioner, kapitel, hashvärden och revisionslogg. Se `docs/migration-from-1.x.md`.

## Dokumentation

- `docs/architecture.md`
- `docs/custom-gpt-edition.md`
- `docs/chatgpt-project-edition.md`
- `docs/migration-from-1.x.md`
- `docs/build-and-validation.md`
- `docs/archive/README.md`
