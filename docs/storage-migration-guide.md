# Migreringsguide mellan ZIP och GitHub

## Grundregel

Endast ett lagringsläge är kanoniskt åt gången. Att exportera, ladda upp eller kopiera projektfiler byter inte automatiskt lagringsläge.

En migrering ska alltid:

1. låsa en entydig källversion
2. verifiera projektet före ändring
3. bevara `project_id`
4. öka projektrevisionen exakt med 1
5. uppdatera `storage`-metadata
6. bevara kapitelfiler om inte användaren uttryckligen beställt innehållsändring
7. slutverifiera den nya kanoniska källan
8. lämna en fullständig revisionskvittens

## ZIP till GitHub

### Förutsättningar

- exakt en verifierbar projekt-ZIP är vald
- användaren anger ett GitHub-repository
- repositoryts default branch kan läsas
- skrivbehörighet finns
- en arbetsbranch, normalt `development`, kan skapas eller återanvändas säkert

### Transaktion

1. Lås ZIP-filens namn och hash.
2. Packa upp i en ny tom katalog.
3. Kör `verify`.
4. Kontrollera repository, default branch och aktuella branch-SHA:n.
5. Skapa arbetsbranchen från aktuell default head om den saknas.
6. Kontrollera att repositoryt inte redan innehåller ett konkurrerande romanprojekt.
7. Kör en intern projektcommit som ändrar `storage.mode` från `zip` till `github` och fyller i repository, projektrot, basbranch och arbetsbranch.
8. Ändra inga kapitel under lagringsmigreringen.
9. Publicera projektträdet på arbetsbranchen utan force push.
10. Läs tillbaka filerna från den nya committen och kör `verify`.
11. Skapa eller återanvänd PR mot default branch.

Efter migreringen är GitHub kanonisk källa. Den gamla ZIP-filen är historisk källartefakt, inte fortsatt arbetskälla.

## GitHub till ZIP

### Förutsättningar

- repository, arbetsbranch och exakt commit-SHA är låsta
- GitHub-versionen verifierar
- användaren har uttryckligen begärt att ZIP ska bli nytt kanoniskt lagringsläge, inte bara en export

### Transaktion

1. Läs projektet från exakt låst Git-commit.
2. Kör `verify`.
3. Kör en intern projektcommit som ändrar `storage.mode` till `zip` och nollställer GitHub-specifika fält.
4. Ange nytt `canonical_zip_name` med nästa revisionsnummer.
5. Ändra inga kapitel under migreringen.
6. Paketera hela projektet.
7. Packa upp leverans-ZIP:en i en ny tom katalog.
8. Kör `verify` på den återuppackade versionen.
9. Leverera ZIP-filen och revisionskvittensen.

Efter migreringen är den levererade ZIP-filen kanonisk. GitHub-repositoryt är historik eller spegel tills användaren uttryckligen migrerar tillbaka.

## GitHub till ZIP-export utan lagringsbyte

En ZIP-export är inte en migrering.

1. Välj arbetsbranch eller default branch.
2. Lås exakt commit-SHA.
3. Verifiera projektet.
4. Paketera och återverifiera ZIP-filen.
5. Behåll `storage.mode = github`.
6. Märk ZIP-filen och revisionskvittensen som export eller säkerhetskopia.

## Konflikter under migrering

Stoppa automatiskt om:

- manifestet inte verifierar
- båda GitHub-brancherna har ändrat samma kanoniska filer
- arbetsbranchens head ändras efter källås
- repositoryt redan innehåller ett annat projekt-id
- samma projektrevision har skapats i två konkurrerande källor
- kapitelfiler skulle behöva slås ihop utan uttryckligt användarbeslut

Använd aldrig force push, radering av manifest eller ominitiering för att kringgå konflikten.

## Revisionskvittens

Kvittensen ska ange:

- migreringsriktning
- project-id
- källrevision och ny revision
- källans exakta identitet
- nytt kanoniskt lagringsläge
- ändrade metadatafiler
- bekräftelse att kapitelfiler var oförändrade
- verifieringsresultat
- ZIP-fil eller Git-commit/PR beroende på mål
