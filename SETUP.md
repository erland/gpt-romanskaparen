# Setup för Custom GPT

## Obligatorisk uppladdning

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

Kopiera innehållet i `gpt-instructions.md` till GPT:ns Instructions-fält. Conversation starters finns i `conversation-starters.md`.

Fil 05 är den gemensamma bindande manualen för källval, revision, integritet, synk, migrering och export. Fil 06 styr repository, brancher, commits, pull requests, samtidighet, förmågetest och GitHub-specifik felhantering.

## Projektmallen

Ladda inte upp katalogen `templates/romanprojekt/` fil för fil. Ladda endast upp den samlade `project-template-bundle.md`.

Bundle-filen är deterministiskt genererad från den aktuella projektmallen och innehåller:

- manifestschema 2
- ZIP/GitHub-lagringsmetadata
- projektstruktur och mallfiler
- den aktuella versionen av `scripts/project_integrity.py`

Kontrollera bundle-synk med:

```bash
python scripts/build_project_template_bundle.py --check
```

## Capabilities och anslutningar

Aktivera:

- **Code Interpreter / Data Analysis** för ZIP, SHA-256, integritetsverktyg, EPUB och PDF.
- **GitHub-app eller anslutning med läs- och skrivrättigheter** om GitHub-läge ska användas.
- **Image generation** vid behov för omslag.
- **Web browsing** vid behov för research.

ZIP-läget är alltid grundläget. GitHub-läget är villkorligt och får endast erbjudas när den aktuella GPT-konfigurationen faktiskt kan utföra hela GitHub-arbetsflödet.

## Obligatoriskt GitHub-förmågetest

Innan ett projekt migreras till GitHub eller ett GitHub-projekt skrivs ska GPT:n verifiera att den kan:

1. läsa repositorymetadata och aktuell default branch
2. läsa branchernas aktuella head-SHA
3. bekräfta skrivbehörighet
4. skapa eller säkert återanvända en arbetsbranch
5. skapa eller uppdatera en fil/commit på arbetsbranchen
6. skapa eller återanvända en pull request
7. läsa tillbaka den publicerade committen och berörda filer

Testet ska göras utan att ändra romanprojektets kanoniska innehåll, exempelvis med en neutral testfil eller i ett separat tomt testrepository.

Om någon förmåga saknas ska GPT:n:

- inte ändra `storage.mode` till `github`
- inte påbörja ZIP → GitHub-migrering
- inte påstå att GitHub-stöd finns
- fortsätta eller erbjuda ZIP-läge
- ange exakt vilken förmåga som saknas

En anslutning som endast kan läsa GitHub räcker för analys men inte för GitHub-läge med sparade projektändringar.

## Lagringsval

När projektfilerna ska skapas frågar GPT:n efter kanoniskt lagringsläge:

1. Projekt-ZIP
2. GitHub-repository, endast efter godkänt förmågetest

Endast ett läge får vara kanoniskt åt gången.

### ZIP-läge

- användaren bifogar eller namnger exakt en indata-ZIP
- GPT:n packar upp i en tom arbetskatalog
- `verify` körs före ändring
- intern revision skapas med strikt `--allow`
- ny ZIP skapas, återöppnas och verifieras

### GitHub-läge

Efter godkänt förmågetest:

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

GitHub-förmågetest, branchlås, commit och PR utförs separat av GPT:n enligt fil 06.

## Äldre och skadade projekt

En äldre manifestlös ZIP auditeras först med `audit-legacy`. Befintliga kapitel ska bevaras byte-identiskt när den första revisionslåsta baslinjen skapas.

Finns manifest men verifieringen misslyckas är projektet skadat modernt. GPT:n får inte radera manifestet, köra om `init` eller behandla projektet som legacy.

## Revisionskvittens

Efter en sparad ändring ska GPT:n redovisa lagringsläge, project-id, källrevision, ny revision, ändrade filer och verifieringsresultat.

I ZIP-läge anges indata- och leveransfil. I GitHub-läge anges repository, basbranch, arbetsbranch, källcommit, ny commit och skapad eller uppdaterad PR.

## Export

EPUB/PDF och ZIP-export från GitHub är exporter. De blir inte ny kanonisk projektkälla utan en uttrycklig migrering.

Reglerna i fil 05 och projektets `publishing/` styr exporten.
