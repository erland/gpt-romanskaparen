# Implementations- och konsistensrapport

Datum: 2026-08-05  
Branch: `development`  
Målbranch: repositoryts default branch (`main` vid genomförandet)

## Omfattning

Rapporten granskar införandet av GitHub som alternativt kanoniskt lagringsläge för Romanskaparen, samtidigt som ZIP-läget bevaras.

## Genomförda delar

- GitHub-designspecifikation
- gemensam manual för projektstruktur, källås, integritet och export
- bindande GitHub-manual
- lagringsval och GitHub-regler i huvudinstruktionen
- ZIP/GitHub conversation starters
- manifest schema 2 med `storage`-objekt
- lagringsmedvetna projektmallar
- filsystembaserat integritetsverktyg med schema-1-bakåtkompatibilitet
- dokumenterad migrering mellan ZIP och GitHub
- testmatris
- uppdaterad README och SETUP
- deterministisk bundle-generator

## Låsta designbeslut

- ett romanprojekt per repository
- projektroten är repositoryts rot i första versionen
- repositoryts aktuella default branch är basbranch
- `development` är standardarbetsbranch
- användaren kan välja annat arbetsbranchnamn
- en befintlig PR återanvänds
- användaren ansvarar normalt för merge
- ingen force push
- ingen automatisk merge till default branch
- aktuella branch-SHA:n hämtas inför varje operation
- arbetsbranchens head kontrolleras igen före publicering
- exakt ett kanoniskt lagringsläge används åt gången
- Git-SHA lagras inte persistent i manifestet

## Konsistenskontroll

### Instruktioner och knowledge

- `gpt-instructions.md` hänvisar till fil 05 och 06.
- Fil 05 styr gemensam projektintegritet och fil 06 GitHub-specifika detaljer.
- ZIP och GitHub beskrivs som alternativa lagringslager för samma interna projektmodell.
- Förbuden mot force push, automatisk merge och gissad kapitelmerge är konsekventa.

### Manifest och verktyg

- Manifestmallen använder schema 2.
- Storage-fälten överensstämmer med integritetsverktygets validering.
- `canonical_zip_name` finns kvar för äldre schema-1-projekt.
- Integritetsverktyget gör inga nätverksanrop.
- Vanlig commit får inte implicit ändra lagringsläge.
- `project_id` och intern revisionskedja är oberoende av Git-SHA.

### Projektmall och dokumentation

- README, SETUP, project index och projektstatus använder samma begrepp för lagringsläge, repository, basbranch och arbetsbranch.
- ZIP-export från GitHub skiljs från faktisk migrering.
- Migreringsguiden kräver oförändrade kapitel under rent lagringsbyte.

## Genomförd verktygsvalidering

Under implementationen provades:

- syntaxkontroll av `project_integrity.py`
- init av nytt ZIP-projekt
- verify och status i ZIP-läge
- skapande av nästa ZIP-revision
- init av nytt GitHub-projekt
- validering av obligatoriska GitHub-fält
- verify efter intern commit

Resultaten var godkända i de provade scenarierna.

## Kvarstående verifiering

Följande kräver ett separat testrepository och faktisk Custom GPT-konfiguration:

- branch skapad från exakt default-head
- återanvändning av befintlig PR
- ändrad arbetsbranch-head under pågående operation
- samtidiga ändringar på båda brancherna
- read-only-behörighet
- full ZIP → GitHub- och GitHub → ZIP-migrering
- manuell kontroll av alla conversation starters

## Bundle-status

`project-template-bundle.md` innehåller fortfarande den äldre inbäddade integritetsverktygsversionen. Därför är `project-template-storage-v2.md` fortsatt bindande och måste laddas upp tillsammans med bundle-filen.

`scripts/build_project_template_bundle.py` har lagts till för deterministisk regenerering. När generatorn körts i en vanlig Git-miljö ska:

1. den genererade bundle-filen granskas
2. `python scripts/build_project_template_bundle.py --check` ge godkänt resultat
3. `project-template-storage-v2.md` tas bort
4. README och SETUP förenklas till en enda bundle-fil

Detta är den enda kända övergångsbegränsningen i den nuvarande PR-versionen.

## Samlad bedömning

Arkitekturen, instruktionerna, projektmodellen och integritetsverktyget är konsekventa för ZIP och GitHub. Lösningen är redo för connector- och Custom GPT-accepteranstest, med den dokumenterade bundle-övergången som kvarstående paketeringssteg.
