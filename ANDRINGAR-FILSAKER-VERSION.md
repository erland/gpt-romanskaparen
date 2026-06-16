# Ändringar i den filsäkra versionen

## Problem som åtgärdas

Den tidigare versionen beskrev zipen som kanonisk källa men saknade regler för:

- vilken av flera zip-filer som skulle väljas
- hur en äldre zip skulle identifieras
- hur oavsiktliga ändringar av tidigare kapitel skulle upptäckas
- hur en färdig zip skulle verifieras efter paketering
- hur tomma mallkapitel skulle skiljas från verkliga kapitel

## Nya skydd

1. **Explicit källåsning** – exakt en namngiven eller bifogad indata-zip per arbetssteg.
2. **Monotona revisioner** – filnamn som `roman-r0012-kapitel-12.zip`.
3. **Stabilt project-id** – samma romanprojekt behåller samma UUID genom alla revisioner.
4. **SHA-256-manifest** – alla spårade filer och varje kapitel får en verifierbar hash.
5. **Tillåten ändringslista** – integritetsverktyget stoppar oväntade filändringar.
6. **Skydd av äldre kapitel** – vid nytt kapitel måste alla befintliga kapitelfiler vara byte-identiska.
7. **Ren arbetskatalog** – varje operation börjar från en ny uppackning av endast den valda zipen.
8. **Efterkontroll** – leveranszipen packas upp på nytt och verifieras innan den lämnas ut.
9. **Ingen rekonstruktion från chatten** – saknas korrekt zip avbryts arbetet i stället för att GPT:n gissar.
10. **Inget tomt `kapitel-01.md` i mallen** – numeriska kapitelfiler skapas först när texten faktiskt finns.

## Nya projektfiler

- `project-manifest.json`
- `revision-log.md`
- `scripts/project_integrity.py`

## Migrering av äldre romanprojekt

Vid nästa användning av ett äldre projekt ska Romanskaparen:

1. använda endast den zip som uttryckligen bifogats eller namngivits
2. kontrollera dubbletter och alternativa kapitelkopior
3. lägga till manifest, revisionslogg och integritetsverktyg
4. skapa och leverera en separat verifierad baslinjerevision
5. först därefter fortsätta med nästa kapitel eller revision

## Komplettering v5 – säker migrering från äldre GPT-versioner

Denna version lägger till ett formellt kompatibilitetslager för projektzippar skapade innan manifeststandarden:

- nytt `audit-legacy`-kommando granskar zipen före uppackning
- källzipens SHA-256 och varje befintligt kapitels SHA-256 låses i en extern auditfil
- dubbla/osäkra arkivsökvägar och konkurrerande kapitelnamn blockerar migreringen
- första revisionslåsta legacy-baslinjen måste vara `r0001-migrerad`
- `init --legacy-migration` kräver auditfil och bevisar att kapitlen är byte-identiska
- manifestet får ett `migration`-objekt med källzip, ursprungshashar och bevarandestatus
- migrering och efterföljande kapitelarbete registreras som två separata transaktioner
- ett befintligt trasigt manifest får aldrig skrivas över eller behandlas som ett äldre manifestlöst projekt
- tidigare `--force`-väg har tagits bort från integritetsverktyget


## v6 – kompakt huvudinstruktion
- Kortade `gpt-instructions.md` till under 8 000 tecken.
- Behöll bindande huvudregler om entydig zip-källa, klassificering, kapitelhashskydd, revisionskedja och obligatorisk slutverifiering.
- Samlade detaljerade migrerings-, verifierings- och kommandoregler i `knowledge-upload/05-projektstruktur-och-synk.md`.
- Behöll samma sex Knowledge-uppladdningar: fem filer i `knowledge-upload/` samt `project-template-bundle.md`.

## v7 – återställning efter jämförelse med ursprungsversionen

Efter radvis jämförelse med den ursprungliga `gpt-instructions.md` återfördes uttryckliga regler om nybörjarperspektiv, begränsat antal frågor, 2–4 kreativa alternativ, godkännande före kapitel 1, identifiering av nästa rimliga steg, läsning av README samt läsbarhet och berättarflyt. Filsäkerhetsreglerna är oförändrade.
