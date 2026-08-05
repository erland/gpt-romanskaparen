# Romanskaparen GPT-paket

Detta paket innehåller material för en Custom GPT som planerar, skriver, reviderar och exporterar romanprojekt steg för steg. Romanprojekt kan lagras antingen som verifierade projekt-ZIP-filer eller direkt i ett GitHub-repository.

## Rekommenderad GPT-konfiguration

**Namn:** Romanskaparen

**Beskrivning:** En guidande skrivpartner för romanprojekt. Hjälper användaren att utveckla idé, synopsis, karaktärer, kapitelplan, kapiteltext, kontinuitet och EPUB/PDF-export, med ZIP eller GitHub som kanoniskt lagringsläge.

## Filer

- `gpt-instructions.md` – huvudinstruktioner att klistra in i GPT Builder.
- `conversation-starters.md` – förslag på conversation starters.
- `knowledge-upload/` – bindande arbets- och hantverksmanualer.
- `templates/romanprojekt/` – den faktiska projektmallen.
- `project-template-bundle.md` – samlad projektmall för GPT Knowledge.
- `project-template-storage-v2.md` – bindande schema-2-tillägg tills bundle-filen har regenererats med den nya integritetsverktygsversionen.
- `docs/` – design, migreringsguide och testmatris.

## Rekommenderad uppladdning

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

Kopiera `gpt-instructions.md` till Instructions-fältet. Fil 05 styr gemensam projektintegritet och fil 06 styr GitHub-specifika repository-, branch-, commit- och PR-regler.

`project-template-storage-v2.md` har företräde framför äldre schema-1- och ZIP-specifika delar i den monolitiska bundle-filen. När `project-template-bundle.md` senare regenererats från `templates/romanprojekt/` kan tillägget tas bort från uppladdningen.

## Två kanoniska lagringslägen

### ZIP

- exakt en indata-ZIP väljs per operation
- nästa interna projektrevision skapas
- hela projektet paketeras
- leverans-ZIP:en återöppnas och verifieras
- filnamn använder monotona revisioner, exempelvis `roman-r0012-kapitel-12.zip`

### GitHub

- exakt repository, projektrot, basbranch, arbetsbranch och commit-SHA låses
- repositoryts default branch används som bas
- `development` används som standardarbetsbranch om användaren inte väljer annat
- varje avslutad projektoperation ger en intern projektrevision och en Git-commit
- en PR mot default branch skapas eller återanvänds
- användaren ansvarar normalt för merge
- ingen force push eller automatisk merge används

Endast ett lagringsläge är kanoniskt åt gången. En ZIP-export från GitHub ändrar inte automatiskt projektets lagringsläge.

## Versionssäker filhantering

Båda lägena använder samma interna skyddsmodell:

- `project-manifest.json` håller project-id, revision, lagringsmetadata och SHA-256-hashar
- `revision-log.md` ger en läsbar revisionskedja
- `scripts/project_integrity.py` stoppar oavsiktliga fil- och kapiteländringar
- strikt tillåten ändringslista används vid varje intern commit
- externa ändringar på GitHub-brancher upptäcks genom aktuella SHA:n
- skadat modernt manifest initieras aldrig om
- äldre manifestlösa ZIP-projekt auditeras och migreras med byte-identiska kapitel

Integritetsverktyget är avsiktligt filsystembaserat. GitHub-API, branchlås, commits och PR-hantering utförs av GPT:ns GitHub-arbetsflöde.

## Viktiga beteenderegler

Romanskaparen ska:

- välja och låsa exakt en kanonisk projektkälla
- normalt inte visa hela kapiteltexten i chatten vid filbaserat arbete
- spara kapiteltext i `kapitel/kapitel-XX.md`
- spara kapitelnoteringar i `kapitelnoteringar.md`
- hålla manifest, revisionslogg, status-, plan- och kontinuitetsfiler synkade
- hashverifiera alla oförändrade kapitel
- lämna en lagringsanpassad revisionskvittens efter varje sparad ändring

## Publiceringsstandard

Markdown är källformat. Projektmallen innehåller `publishing/` med metadata och regler för Pandoc-baserad EPUB/PDF-export.

Kapitelfiler använder:

```markdown
# 1. Kapitelrubrik
```

EPUB/PDF visar kapitelstart som två centrerade rader:

```text
1
Kapitelrubrik
```

Innehållsförteckningen visar `1. Kapitelrubrik`.

## Rekommenderade capabilities

- GitHub connector: krävs för privat repository och skrivning i GitHub-läge.
- Code Interpreter / Data Analysis: krävs för ZIP, SHA-256, integritetsverktyg och export.
- Web browsing: vid behov för research.
- Image generation: valfritt för omslag och konceptbilder.

## Dokumentation

- `docs/github-storage-design.md` – arkitektur och låsta designbeslut.
- `docs/storage-migration-guide.md` – migrering mellan ZIP och GitHub.
- `docs/github-workflow-tests.md` – testmatris och accepteranskriterier.
