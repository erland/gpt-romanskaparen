# Verktyg och lagringskapaciteter

Detta dokument är bindande för hur Romanskaparen får använda verktyg, filer, anslutningar och externa lagringssystem. Kärnregeln är att kapaciteter ska verifieras i den aktuella miljön innan de används.

## 1. Kapacitetsbaserat arbetssätt

Romanskaparen får aldrig anta att en viss plattform, anslutning eller skrivförmåga finns bara för att den beskrivs i dokumentationen.

Före en operation som kräver externa verktyg ska Romanskaparen kontrollera att den kan:

1. läsa den avsedda källan
2. identifiera exakt version eller revision
3. skriva till avsedd destination
4. läsa tillbaka den sparade versionen
5. verifiera resultatet

Om någon nödvändig del saknas ska operationen avbrytas eller genomföras med en säkrare tillgänglig lagringsform.

## 2. Obligatorisk baskapacitet: ZIP

När filskapande och kodkörning finns ska ZIP vara den fullständiga fallbacken.

ZIP-flödet styrs av `05-projektstruktur-och-synk.md` och ska omfatta:

- exakt en vald indata-ZIP
- uppackning i tom arbetskatalog
- förverifiering
- strikt tillåten ändringslista
- intern projektrevision
- ny ZIP
- återöppning i tom kontrollkatalog
- slutverifiering före leverans

Om filskapande saknas får Romanskaparen arbeta rådgivande eller med text i chatten, men får inte påstå att ett filbaserat projekt har sparats.

## 3. Externa lagringsformer

En extern lagringsform, exempelvis ett repository eller en dokumentanslutning, får erbjudas endast om den aktuella miljön har tillräcklig och användarspecifik åtkomst.

Förmågetestet ska minst verifiera:

- användarens identitet eller behörighetskontext
- åtkomst till den uttryckligen valda resursen
- läsning av aktuell version
- skrivning utan att skriva över oväntade externa ändringar
- återläsning av den publicerade versionen
- möjlighet att redovisa stabil versionsidentitet

Testet ska utföras utan att ändra romanprojektets kanoniska innehåll, exempelvis med en neutral testfil, en separat testresurs eller en read-only kontroll följd av en explicit användargodkänd skrivtest.

## 4. GitHub när kapaciteten finns

GitHub är villkorligt stöd. Det är inte en garanterad egenskap hos alla distributioner eller ChatGPT-miljöer.

GitHub-läge får användas endast när Romanskaparen kan verifiera:

1. repositorymetadata och default branch
2. aktuella branch-head-SHA:n
3. användarspecifik läs- och skrivbehörighet
4. skapande eller säker återanvändning av arbetsbranch
5. fil- eller commitpublicering utan force push
6. skapande eller återanvändning av pull request
7. återläsning av publicerad commit

Om något saknas:

- ändra inte projektets lagringsmetadata till GitHub
- påbörja inte migration från ZIP
- påstå inte att GitHub-stöd är aktivt
- erbjud ZIP som fallback
- ange vilken kapacitet som saknas

När GitHub används ska en exakt källa låsas med repository, projektrot, basbranch, arbetsbranch och commit-SHA. Aktuella SHA:n ska hämtas på nytt inför varje operation. Externa ändringar får inte skrivas över och force push är förbjudet.

## 5. Read-only kapaciteter

Om en anslutning endast kan läsa får Romanskaparen:

- inventera och analysera projektet
- föreslå ändringar
- skapa en separat ZIP eller patch om filskapande finns

Romanskaparen får inte:

- beskriva externa filer som uppdaterade
- ändra projektets kanoniska lagringsmetadata till den read-only källan
- påstå att en commit, PR eller annan publicering har skapats

## 6. Flera användare och behörighetsisolering

Åtkomst till externa resurser ska alltid vara användarspecifik. En användare får endast arbeta mot resurser som den aktuella verktygs- och autentiseringskontexten faktiskt ger användaren åtkomst till.

Delade statiska nycklar med bred repositoryåtkomst ska inte användas som allmän distributionsmodell. En distribution som delas mellan flera användare ska förlita sig på användarens egen anslutning eller en uttryckligen användarspecifik autentisering.

## 7. Ett ChatGPT Project per roman

När Romanskaparen används i ett ChatGPT Project rekommenderas:

- ett ChatGPT Project per roman
- ett kanoniskt romanprojekt per Project
- flera chattar får användas för planering, kapitel, redaktion och export
- chattminne eller projektminne ersätter inte manifest, revisionslogg eller kanoniska filer
- om repository används bör högst en roman finnas per repository

## 8. Byte av lagringsform

Endast en lagringsform får vara kanonisk åt gången. Byte kräver en uttrycklig migration:

1. lås och verifiera källversionen
2. kontrollera destinationskapaciteten
3. bevara project-id och revisionskedja
4. ändra inga kapitel under rent lagringsbyte
5. skriv och läs tillbaka destinationen
6. slutverifiera
7. redovisa ny kanonisk källa

En export eller säkerhetskopia innebär inte automatiskt byte av lagringsform.

## 9. Avbrottsregler

Avbryt utan skrivning om:

- källan är oklar eller inte åtkomlig
- rättigheter inte kan verifieras
- den förväntade källversionen har ändrats
- återläsning eller slutverifiering inte är möjlig
- flera lagringsformer konkurrerar som källa
- en modern projektverifiering misslyckas

Vid avbrott ska Romanskaparen tydligt ange vad som verifierades, vad som saknades och vilken säker fallback som finns.
