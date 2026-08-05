# Testmatris för ZIP- och GitHub-arbetsflöden

Statusvärden:

- **Automatiserat verktygstest** – kan testas med `project_integrity.py` i lokal filstruktur.
- **Connector-test** – kräver GitHub-anslutning och ett testrepository.
- **Manuell accepterans** – kräver granskning av GPT-beteende och kvittens.

## A. Integritetsverktyg

| ID | Scenario | Förväntat resultat | Typ |
|---|---|---|---|
| A01 | Initiera nytt ZIP-projekt | Schema 2, `storage.mode=zip`, revision 0 och godkänd verify | Automatiserat verktygstest |
| A02 | Commit i ZIP-läge | Revision ökar exakt med 1 och ZIP-namn uppdateras | Automatiserat verktygstest |
| A03 | Initiera nytt GitHub-projekt | Schema 2 och komplett repository-/branchmetadata | Automatiserat verktygstest |
| A04 | GitHub-läge utan repository | Init eller verify stoppas | Automatiserat verktygstest |
| A05 | GitHub-läge utan basbranch | Init eller verify stoppas | Automatiserat verktygstest |
| A06 | GitHub-läge utan arbetsbranch | Init eller verify stoppas | Automatiserat verktygstest |
| A07 | Schema-1-projekt | Behandlas som implicit ZIP och kan verifieras | Automatiserat verktygstest |
| A08 | Nästa commit från schema 1 | Uppgraderas till schema 2 utan byte av project-id | Automatiserat verktygstest |
| A09 | Fel förväntad revision | Commit stoppas utan manifeständring | Automatiserat verktygstest |
| A10 | Fil utanför `--allow` | Commit stoppas | Automatiserat verktygstest |
| A11 | Annat kapitel ändras vid kapitelrevision | Commit stoppas av tillåten lista | Automatiserat verktygstest |
| A12 | Implicit byte ZIP → GitHub i vanlig commit | Commit stoppas | Automatiserat verktygstest |
| A13 | Skadat manifest | Verify och init stoppas | Automatiserat verktygstest |
| A14 | Legacy-ZIP med entydiga kapitel | Audit kan migrera och kapitelhashar låses | Automatiserat verktygstest |
| A15 | Legacy-ZIP med konkurrerande kapitel | Audit blockerar migrering | Automatiserat verktygstest |

## B. GitHub-branch och PR

| ID | Scenario | Förväntat resultat | Typ |
|---|---|---|---|
| B01 | Arbetsbranch saknas | `development` skapas från exakt aktuell default-head | Connector-test |
| B02 | Arbetsbranch finns | Den återanvänds och återställs inte | Connector-test |
| B03 | Ingen PR finns | PR skapas från arbetsbranch till default branch | Connector-test |
| B04 | Öppen PR finns | Nya commits uppdaterar samma PR | Connector-test |
| B05 | Tidigare PR är mergad | Ny PR skapas när nya commits skiljer brancherna | Connector-test |
| B06 | Arbetsbranchens head ändras före skrivning | Planerad publicering stoppas och källan läses om | Connector-test |
| B07 | Default branch ändras utan filöverlappning | Säker synk kan göras efter ny verifiering | Connector-test |
| B08 | Default och arbetsbranch ändrar samma kapitel | Automatisk merge stoppas | Connector-test |
| B09 | Båda ändrar manifest/revisionslogg | Automatisk merge stoppas | Connector-test |
| B10 | Endast läsbehörighet | Analys tillåts men ingen sparad ändring påstås | Connector-test |
| B11 | Force push skulle krävas | Operationen stoppas | Connector-test |
| B12 | PR pekar på fel base | Operationen stoppas eller PR:n korrigeras uttryckligt | Connector-test |

## C. GPT-användarflöde

| ID | Scenario | Förväntat resultat | Typ |
|---|---|---|---|
| C01 | Nytt projekt färdigplanerat | GPT frågar ZIP eller GitHub innan projektfiler skapas | Manuell accepterans |
| C02 | Användaren väljer ZIP | Befintligt ZIP-flöde används utan GitHub-frågor | Manuell accepterans |
| C03 | Användaren väljer GitHub | Repository och upptäckt branchkonfiguration redovisas | Manuell accepterans |
| C04 | Repository saknas | GPT begär eller använder uttryckligen angivet repository | Manuell accepterans |
| C05 | GitHub-anslutning saknas | GPT förklarar åtkomstproblemet och påstår inte att något sparats | Manuell accepterans |
| C06 | Nytt kapitel i GitHub-läge | Intern revision, commit och PR uppdateras; äldre kapitel oförändrade | Manuell accepterans |
| C07 | Revidera ett kapitel | Endast valt kapitel och tillåtna synkfiler ändras | Manuell accepterans |
| C08 | Exportera ZIP från GitHub | ZIP levereras som export; `storage.mode` förblir GitHub | Manuell accepterans |
| C09 | Migrera ZIP → GitHub | Project-id bevaras, revision ökar och kapitel är oförändrade | Manuell accepterans |
| C10 | Migrera GitHub → ZIP | Project-id bevaras och leverans-ZIP blir kanonisk | Manuell accepterans |
| C11 | Konflikt på samma kapitel | GPT redovisar konflikt och inväntar uttryckligt beslut | Manuell accepterans |
| C12 | Revisionskvittens | Innehåller lagringsläge och rätt ZIP- eller GitHub-fält | Manuell accepterans |

## D. Dokument- och mallkonsistens

Följande kontroller ska göras inför release:

1. `gpt-instructions.md` är under den avsedda GPT Builder-gränsen.
2. Fil 05 och 06 motsäger inte varandra.
3. Manifestmallen använder schema 2 och samma storage-fält som integritetsverktyget.
4. README, SETUP, project index och projektstatus använder samma benämningar.
5. `canonical_zip_name` finns kvar för schema-1-bakåtkompatibilitet.
6. Aktuell Git commit-SHA lagras inte i manifestet.
7. Integritetsverktyget gör inga nätverks- eller GitHub-anrop.
8. Bundle och mallkatalog ska jämföras efter regenerering.
9. Övergångstillägget får tas bort först när bundle-filen innehåller schema 2 och den nya verktygsversionen.
10. Testresultat och kvarstående begränsningar ska redovisas i PR:n.

## Genomförda kontroller i implementationen

Följande verktygsscenarier har provats under prompt 5:

- nytt ZIP-projekt
- ZIP verify och status
- nästa ZIP-revision
- nytt GitHub-projekt
- GitHub storage-validering
- verify efter commit

Fulla connector- och manuella GPT-testfall bör köras i ett separat testrepository innan ändringen betraktas som produktionsverifierad.
