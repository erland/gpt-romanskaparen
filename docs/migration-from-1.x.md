# Migrering från Romanskaparen 1.x till 2.0

Status: första utkast från Prompt 1

## 1. Vad som migreras

Migreringen gäller repositoryts produkt- och distributionsstruktur. Den ska inte framtvinga en ändring av användarnas befintliga romanprojekt.

Romanskaparen 1.x är organiserad som ett Custom GPT-paket. Romanskaparen 2.0 organiseras som:

- gemensam produktkärna
- Custom GPT-distribution
- ChatGPT Project-distribution
- enkel konversationsdistribution

## 2. Vad som inte ändras för befintliga romanprojekt

Ett verifierbart befintligt romanprojekt ska behålla:

- `project_id`
- intern revision
- `parent_revision`
- kapitel och filnamn
- kapitelhashar och filhashar
- revisionslogg
- projektstatus och kontinuitetsfiler
- publiceringsmetadata

En befintlig 1.x-ZIP ska inte behöva konverteras bara för att Romanskaparen körs från 2.0.

## 3. Repositorymigrering

### Fas 1 – parallell kärna

Prompt 2 skapar `core/` medan nuvarande rotfiler lämnas kvar. Detta gör förändringen granskningsbar och gör rollback enkel.

Under fasen gäller:

- nya kärnfiler är framtida kanonisk källa
- gamla filer får inte vidareutvecklas separat
- större beteendeändringar undviks
- projektmallen flyttas i första hand innehållsmässigt oförändrad

### Fas 2 – bygg distributioner

Prompt 3 och 4 skapar GPT- respektive Project-distribution från kärnan.

När distributionerna finns ska följande verifieras:

- GPT-instruktionen är under 8 000 tecken
- knowledge-filerna är högst 20
- Project Edition kan installeras utan GPT Builder
- ZIP-flödet fungerar i båda
- externa verktyg beskrivs villkorligt

### Fas 3 – automatiserad generering

Prompt 5 inför scripts som genererar bundles och distributionskopior.

Efter detta ska manuella ändringar i genererade distributionsfiler betraktas som fel.

### Fas 4 – städa 1.x-roten

Prompt 6 ersätter eller arkiverar gamla rotfiler.

Möjliga utfall:

- `gpt-instructions.md` tas bort eller ersätts av hänvisning till `distributions/gpt/instructions.md`
- `knowledge-upload/` tas bort när båda distributionerna genereras från `core/knowledge/`
- `templates/` tas bort när `core/templates/` är kanonisk
- `project-template-bundle.md` tas bort från roten när distributionsbundles genereras
- historiska dokument flyttas till `docs/archive/`

## 4. Migrera en befintlig Custom GPT

När GPT Edition är färdig:

1. öppna GPT Builder
2. ersätt Instructions med `distributions/gpt/instructions.md`
3. ta bort gamla knowledge-filer
4. ladda upp filerna i `distributions/gpt/knowledge/`
5. ladda upp `distributions/gpt/project-template-bundle.md`
6. ersätt conversation starters
7. kontrollera capabilities enligt `distributions/gpt/INSTALL.md`
8. testa med en kopia av ett befintligt ZIP-projekt

Befintliga romanprojekt behöver inte ändras.

## 5. Migrera till ChatGPT Project Edition

För varje roman:

1. skapa ett separat ChatGPT Project med romanens namn
2. klistra in `distributions/project/PROJECT-INSTRUCTIONS.md` som projektinstruktion
3. bifoga `distributions/project/knowledge/`
4. bifoga projektbundlen
5. följ `START-HERE.md`
6. välj exakt en kanonisk romanprojektkälla
7. fortsätt från den senaste verifierade ZIP-revisionen eller annan verifierat tillgänglig källa

Projektets chattminne är inte en ersättning för romanprojektets filer.

## 6. Flytta ett ZIP-projekt till ett ChatGPT Project

Att lägga ett befintligt ZIP-projekt i ett ChatGPT Project är inte i sig en formatmigrering.

Säker procedur:

1. skapa ChatGPT-projektet
2. installera Project Edition
3. bifoga exakt senaste verifierade projekt-ZIP
4. be Romanskaparen läsa och verifiera ZIP-filen
5. fortsätt från samma `project_id` och revision
6. leverera nästa vanliga verifierade ZIP-revision

Ingen baslinjerevision behövs om manifestet redan verifierar.

## 7. Legacyprojekt

Ett projekt utan manifest behandlas fortsatt enligt legacy-reglerna:

- auditera källan
- kontrollera dubbletter
- bevara befintliga kapitel byte-identiskt
- skapa separat baslinjerevision

Ett projekt där manifest finns men inte verifierar är fortfarande skadat modernt och får inte initieras om.

## 8. Rollback

Så länge Prompt 2–4 pågår kan `main` och 1.x-strukturen användas som referens.

När 2.0 mergas ska Git-historiken vara rollbackmekanismen. Gamla aktiva filer ska inte ligga kvar permanent som parallella regelkällor.

## 9. Kompatibilitetslöfte

Romanskaparen 2.0 ska inte kräva att en användare:

- byter filnamn i sitt romanprojekt
- skapar om manifestet
- startar om revisionen
- flyttar kapitel
- byter från ZIP
- använder GitHub

Förändringen gäller hur Romanskaparen distribueras och installeras, inte hur en fungerande roman måste lagras.

## 10. Öppna punkter till senare promptar

- slutliga versionsnummer för distributionerna
- om rotfiler ska bli hänvisningsfiler eller tas bort helt
- exakt format för `distribution-manifest.json`
- hur Project Edition-filer bäst paketeras för enkel installation
- om en färdig distributions-ZIP ska genereras

Dessa beslut påverkar inte den låsta kärnarkitekturen.
