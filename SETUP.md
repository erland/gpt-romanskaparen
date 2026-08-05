# Setup för Custom GPT

## Obligatorisk uppladdning

Ladda upp följande knowledge-filer:

```text
knowledge-upload/01-arbetsflode-och-nyborjarstod.md
knowledge-upload/02-berattelsehantverk.md
knowledge-upload/03-karaktarer-varld-och-kontinuitet.md
knowledge-upload/04-genreguider.md
knowledge-upload/05-projektstruktur-och-synk.md
knowledge-upload/06-github-arbetsflode.md
project-template-bundle.md
project-template-storage-v2.md
```

Kopiera innehållet i `gpt-instructions.md` till GPT:ns Instructions-fält. Conversation starters finns i `conversation-starters.md`.

Fil 05 är den gemensamma bindande manualen för källval, revision, integritet, synk, migrering och export. Fil 06 är bindande för repository, brancher, commits, pull requests, samtidighet och GitHub-specifik felhantering.

## Projektmallen

Ladda inte upp katalogen `templates/romanprojekt/` fil för fil. Ladda upp den samlade `project-template-bundle.md` och det tillfälliga bindande tillägget `project-template-storage-v2.md`.

Tillägget har företräde för:

- manifestschema 2
- `storage`-metadata
- ZIP/GitHub-kommandon
- den uppdaterade integritetsverktygsversionens beteende

När bundle-filen har regenererats från den aktuella mallkatalogen kan tillägget tas bort.

## Capabilities och anslutningar

Aktivera:

- **Code Interpreter / Data Analysis** för ZIP, SHA-256, integritetsverktyg, EPUB och PDF.
- **GitHub connector** för att läsa och skriva privata eller publika repositoryn i GitHub-läge.
- **Image generation** vid behov för omslag.
- **Web browsing** vid behov för research.

GitHub-läget fungerar endast när GPT:n når repositoryt via användarens anslutna GitHub-konto och har nödvändiga rättigheter.

## Lagringsval

När projektfilerna ska skapas frågar GPT:n efter kanoniskt lagringsläge:

1. Projekt-ZIP
2. GitHub-repository

Endast ett läge får vara kanoniskt åt gången.

### ZIP-läge

- användaren bifogar eller namnger exakt en indata-ZIP
- GPT:n packar upp i en tom arbetskatalog
- `verify` körs före ändring
- intern revision skapas med strikt `--allow`
- ny ZIP skapas, återöppnas och verifieras

### GitHub-läge

- användaren anger repository
- GPT:n läser repositoryts aktuella default branch
- `development` används som standardarbetsbranch
- aktuell head-SHA för båda brancherna hämtas inför varje operation
- ändringar görs endast på arbetsbranchen
- en PR mot default branch skapas eller återanvänds
- användaren ansvarar normalt för merge
- force push och automatisk merge används inte

## Integritetsverktyget

`scripts/project_integrity.py` är filsystembaserat och gör inga GitHub-anrop. Det ska:

- acceptera äldre schema-1-manifest som implicit ZIP-läge
- skriva schema 2 för nya projekt och efter nästa commit
- verifiera ZIP- och GitHub-metadata
- skydda kapitel med SHA-256
- kräva förväntad revision och explicit tillåten ändringslista
- stoppa implicit byte av lagringsläge

GitHub-branchlås, commit och PR utförs separat av GPT:n enligt fil 06.

## Äldre och skadade projekt

En äldre manifestlös ZIP auditeras först med `audit-legacy`. Befintliga kapitel ska bevaras byte-identiskt när den första revisionslåsta baslinjen skapas.

Finns manifest men verifieringen misslyckas är projektet skadat modernt. GPT:n får inte radera manifestet, köra om `init` eller behandla projektet som legacy.

## Revisionskvittens

Efter en sparad ändring ska GPT:n redovisa lagringsläge, project-id, källrevision, ny revision, ändrade filer och verifieringsresultat.

I ZIP-läge anges indata- och leveransfil. I GitHub-läge anges repository, basbranch, arbetsbranch, källcommit, ny commit och skapad eller uppdaterad PR.

## Export

EPUB/PDF och ZIP-export från GitHub är exporter. De blir inte ny kanonisk projektkälla utan en uttrycklig migrering.

Reglerna i fil 05 och projektets `publishing/` styr exporten.
