# Installation

Romanskaparen 2.0 finns i två huvuddistributioner.

## Custom GPT

Följ:

```text
distributions/gpt/INSTALL.md
```

Denna variant kräver Code Interpreter/Data Analysis för fullständigt ZIP-arbete. GitHub är inte en garanterad Custom GPT-kapacitet.

## ChatGPT Project

Följ:

```text
distributions/project/INSTALL.md
```

Skapa ett separat ChatGPT Project per roman. Project Edition kan använda användarens egna anslutna verktyg när de faktiskt finns, men ZIP ska alltid kunna användas som fallback.

## Utveckling av repositoryt

Ändra kanoniska regler och mallar under `core/`. Regenerera och validera sedan:

```bash
bash scripts/build.sh
```

Se `docs/build-and-validation.md` för detaljer.
