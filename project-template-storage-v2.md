# Projektmall – lagringsstöd v2

Denna fil är ett bindande tillägg till `project-template-bundle.md` under övergången till lagringsschema 2. Vid konflikt ersätter sektionerna här motsvarande sektioner i den äldre bundle-filen. Övriga mallsektioner i bundle-filen gäller oförändrade.

## Manifestmodell

Nya projekt använder `schema_version: 2` och följande lagringsobjekt:

```json
{
  "storage": {
    "mode": "zip",
    "repository": null,
    "project_root": "/",
    "base_branch": null,
    "working_branch": null
  }
}
```

I GitHub-läge ska `mode` vara `github` och `repository`, `base_branch` samt `working_branch` vara ifyllda. `canonical_zip_name` behålls för bakåtkompatibilitet och ZIP-exporter. Aktuell Git-commit-SHA lagras inte permanent i manifestet.

## Bindande integritetsverktyg

Den kanoniska verktygsfilen för schema 2 är:

```text
templates/romanprojekt/scripts/project_integrity.py
```

När Romanskaparen skapar ett projekt från knowledge-filerna ska den använda exakt verktygsversionen från denna fil eller från ovanstående mallfil på samma repositoryrevision, aldrig den äldre inbäddade verktygsversionen i `project-template-bundle.md`.

Verktygets bindande egenskaper:

- arbetar endast med projektfiler på lokalt filsystem
- gör inga GitHub-API-anrop, branchoperationer eller pull-request-operationer
- verifierar äldre schema 1 som implicit ZIP-läge
- skapar nya manifest och nästa revision som schema 2
- validerar `storage.mode`, repository, projektrot och branchmetadata
- kräver repository, base branch och working branch i GitHub-läge
- stöder `init --storage-mode zip`
- stöder `init --storage-mode github --repository owner/repo --base-branch main --working-branch development`
- visar lagringsmetadata i `status`
- behåller strikt tillåten ändringslista och förväntad projektrevision
- tillåter inte implicit byte av lagringsläge via `commit`
- behåller legacy-audit och byte-identiskt kapitelskydd
- lagrar inte aktuell Git-commit-SHA i manifestet

## Exempel: nytt ZIP-projekt

```bash
python scripts/project_integrity.py init . \
  --slug min-roman \
  --storage-mode zip \
  --zip-name min-roman-r0000.zip
```

## Exempel: nytt GitHub-projekt

```bash
python scripts/project_integrity.py init . \
  --slug min-roman \
  --storage-mode github \
  --repository owner/min-roman \
  --base-branch main \
  --working-branch development
```

## Exempel: nästa revision

ZIP-läge:

```bash
python scripts/project_integrity.py commit . \
  --expected-revision 12 \
  --storage-mode zip \
  --operation "Skapade kapitel 13" \
  --zip-name min-roman-r0013-kapitel-13.zip \
  --allow 'kapitel/kapitel-13.md' \
  --allow 'kapitelplan.md' \
  --allow 'projektstatus.md' \
  --allow 'arbetslogg.md' \
  --allow 'tidslinje.md' \
  --allow 'kontinuitetsanteckningar.md' \
  --allow 'kapitelnoteringar.md' \
  --allow 'project-index.md'
```

GitHub-läge:

```bash
python scripts/project_integrity.py commit . \
  --expected-revision 12 \
  --storage-mode github \
  --operation "Skapade kapitel 13" \
  --allow 'kapitel/kapitel-13.md' \
  --allow 'kapitelplan.md' \
  --allow 'projektstatus.md' \
  --allow 'arbetslogg.md' \
  --allow 'tidslinje.md' \
  --allow 'kontinuitetsanteckningar.md' \
  --allow 'kapitelnoteringar.md' \
  --allow 'project-index.md'
```

GitHub-publicering, branch-SHA-lås och pull request hanteras därefter av Romanskaparen enligt `knowledge-upload/06-github-arbetsflode.md`.

## Bakåtkompatibilitet

Ett giltigt manifest med `schema_version: 1` och utan `storage` ska tolkas som:

```json
{
  "mode": "zip",
  "repository": null,
  "project_root": "/",
  "base_branch": null,
  "working_branch": null
}
```

När nästa godkända projektcommit görs uppgraderas manifestet till schema 2 utan att `project_id`, revisionens föräldrakedja eller kapitelhashar förloras.

## Bundle-synk

Till dess att den monolitiska `project-template-bundle.md` regenereras fullständigt ska Custom GPT-konfigurationen ladda upp både:

- `project-template-bundle.md`
- `project-template-storage-v2.md`

Denna fil har företräde för manifestschema, lagringsmetadata, integritetsverktyg och kommandon. Den fullständiga regenereringen och borttagningen av övergångstillägget ska göras i dokumentations- och slutvalideringssteget.
