# Migrering från Romanskaparen 1.x till 2.0

Romanskaparen 2.0 ändrar hur produkten distribueras, inte formatet för ett fungerande romanprojekt.

## Befintliga romanprojekt

Ett verifierbart 1.x-projekt ska behålla `project_id`, revision, `parent_revision`, kapitel, filnamn, hashvärden, revisionslogg och publiceringsmetadata. Starta inte om revisionen och skapa inte om manifestet.

Ett manifestlöst legacyprojekt migreras enligt knowledge-fil 05. Ett projekt där manifest finns men inte verifierar är ett skadat modernt projekt och får inte ominitieras.

## Migrera en befintlig Custom GPT

1. Säkerhetskopiera nuvarande GPT-konfiguration.
2. Ersätt Instructions med `distributions/gpt/instructions.md`.
3. Ta bort gamla knowledge-filer.
4. Ladda upp de sex filerna i `distributions/gpt/knowledge/`.
5. Ladda upp `distributions/gpt/project-template-bundle.md`.
6. Uppdatera conversation starters.
7. Kontrollera capabilities enligt `distributions/gpt/INSTALL.md`.
8. Testa med en kopia av ett verifierat romanprojekt.

## Flytta arbetet till ChatGPT Project Edition

För varje roman:

1. skapa ett separat ChatGPT Project
2. installera `distributions/project/`
3. bifoga exakt senaste verifierade projekt-ZIP
4. be Romanskaparen verifiera källan
5. fortsätt med samma `project_id` och revision

Att lägga en ZIP i ett ChatGPT Project är inte ett lagringsbyte. Projektet fortsätter i ZIP-läge tills en uttrycklig och verifierad migration genomförs.

## Repositoryts 1.x-filer

De gamla aktiva rotfilerna tas bort i 2.0 för att undvika parallella regelkällor. De finns kvar i Git-historiken vid 1.x-bascommit `2bfe0c882d7d4a510aededb23f71a2302af20b5a` och beskrivs i `docs/archive/README.md`.

## Rollback

Git-historiken är rollbackmekanismen. Återställ en 1.x-tagg eller commit vid behov; kopiera inte gamla regelkällor in i den aktiva 2.0-strukturen.
