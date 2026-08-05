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
- `project-template-bundle.md` – deterministiskt genererad samlad projektmall för GPT Knowledge.
- `scripts/build_project_template_bundle.py` – regenererar och kontrollerar bundle-filen.
- `docs/` – design, migreringsguide, testmatris och valideringsrapport.

## Rekommenderad uppladdning

Ladda upp följande sju knowledge-filer:

```text
knowledge-upload/01-arbetsflode-och-nyborjarstod.md
knowledge-upload/02-berattelsehantverk.md
knowledge-upload/03-karaktarer-varld-och-kontinuitet.md
knowledge-upload/04-genreguider.md
knowledge-upload/05-projektstruktur-och-synk.md
knowledge-upload/06-github-arbetsflode.md
project-template-bundle.md
```

Kopiera `gpt-instructions.md` till Instructions-fältet. Fil 05 styr gemensam projektintegritet och fil 06 styr GitHub-specifika repository-, branch-, commit- och PR-regler.

## Två kanoniska lagringslägen

### ZIP

- exakt en indata-ZIP väljs per operation
- nästa interna projektrevision skapas med strikt ändringslista
- den nya ZIP-filen återöppnas och verifieras före leverans

### GitHub

- repositoryts aktuella default branch används som bas
- `development` används som standardarbetsbranch
- aktuella commit-SHA:n låses inför varje operation
- en PR mot default branch skapas eller återanvänds
- force push och automatisk merge används inte

Endast ett lagringsläge är kanoniskt åt gången. Byte mellan ZIP och GitHub är en uttrycklig migrering som bevarar `project_id` och revisionskedjan.

## Versionssäker filhantering

Projektmallen använder:

- `project-manifest.json` med schema 2, lagringsmetadata, revision och SHA-256-hashar
- `revision-log.md` som läsbar revisionskedja
- `scripts/project_integrity.py` för verifiering, strikt ändringskontroll och legacy-audit
- samma interna projektmodell i ZIP- och GitHub-läge

Integritetsverktyget är filsystembaserat. GitHub-API, branchlås, commits och pull requests hanteras separat av GPT-arbetsflödet.

## Bundle-underhåll

`project-template-bundle.md` genereras från `templates/romanprojekt/`:

```bash
python scripts/build_project_template_bundle.py
python scripts/build_project_template_bundle.py --check
```

`--check` ska lyckas innan en ändring av projektmallen mergas.

## Publiceringsstandard

Markdown är källformat. Projektmallen innehåller `publishing/` med metadata och sättningsregler för Pandoc-baserad EPUB/PDF-export.

Kapitelfiler använder:

```markdown
# 1. Kapitelrubrik
```

Kapitelstarten visas i EPUB/PDF som två centrerade, kompakta rader: nummer och rubrik. Kapitelnoteringar exporteras inte.

## Rekommenderade capabilities

- Code Interpreter / Data Analysis: På för ZIP, SHA-256, EPUB och PDF.
- GitHub connector: På för GitHub-läge.
- Image generation: Valfritt för omslag och konceptbilder.
- Web browsing: Vid behov för research.
