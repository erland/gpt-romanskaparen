# Projektstruktur, synk och exportregler

Detta dokument beskriver den fasta projektstrukturen som Romanskaparen ska använda samt hur statusfiler ska hållas synkade med kapitel och exporter.

## Grundregel
Det ska alltid finnas **en** kanonisk uppsättning projektfiler. Skapa inte parallella statusfiler, alternativa översikter eller tillfälliga sammanfattningsfiler med andra namn när motsvarande fast fil redan finns.

## Fast projektstruktur

```text
romanprojekt/
  README.md
  project-index.md
  roman-bibel.md
  synopsis.md
  kapitelplan.md
  stilguide.md
  tidslinje.md
  kontinuitetsanteckningar.md
  revisionsonskemal.md
  arbetslogg.md
  projektstatus.md
  karaktarer/
    huvudperson.md
    antagonist.md
    bifigurer.md
  kapitel/
    kapitel-01.md
    kapitelmall.md
  exports/
    README.md
    exportlogg.md
```

## Metadata som alltid ska finnas
Följande metadata ska hållas konsekventa i projektets kanoniska filer:
- titel
- undertitel
- författare
- målgrupp
- genre
- status för omslagsbild
- senaste godkända kapitel
- nästa rekommenderade steg

Minst `roman-bibel.md`, `synopsis.md`, `projektstatus.md` och `project-index.md` ska spegla titel/författare när de är fastställda.

## Kanoniska filer och ansvar

| Innehåll | Primär fil |
|---|---|
| Projektets titel, undertitel, författare, genre, målgrupp, kärnidé | `roman-bibel.md` |
| Handlingsöversikt och baksidestext | `synopsis.md` |
| Kapitelstatus och plan | `kapitelplan.md` |
| Projektets aktuella läge och nästa steg | `projektstatus.md` |
| Ändringshistorik | `arbetslogg.md` |
| Händelser i romanens interna tid | `tidslinje.md` |
| Fasta fakta, ledtrådar, öppna trådar | `kontinuitetsanteckningar.md` |
| Karaktärsfakta | `karaktarer/*.md` och sammanfattning i `roman-bibel.md` |
| Filinventering, exportstatus och synkkontroll | `project-index.md` |
| Exportmetadata | `exports/exportlogg.md` |

## Synkpassering efter varje godkänt kapitel
När användaren godkänt ett kapitel och vill uppdatera zipen, gör alltid detta innan zipen skapas:
1. Spara kapitlet som `kapitel/kapitel-XX.md`.
2. Uppdatera raden för kapitlet i `kapitelplan.md` till `Godkänt/sparat`.
3. Lägg till nästa planerade kapitel om planen har vuxit.
4. Uppdatera `projektstatus.md` med nuvarande fas, senaste godkända kapitel, nästa steg, öppna beslut och risker.
5. Lägg exakt en ny rad i `arbetslogg.md` för kapitlet. Blanda inte tabell och fria loggstycken.
6. Uppdatera `tidslinje.md` med romanens nya händelser, inte projektarbetets händelser.
7. Uppdatera `kontinuitetsanteckningar.md` med nya fasta fakta, relationer, ledtrådar och öppna frågor.
8. Uppdatera karaktärsfiler om relationer, motivationer eller fakta ändrats.
9. Uppdatera `project-index.md` så antal kapitel, senaste kapitel och filstatus stämmer.
10. Kontrollera att inga nya parallella statusfiler skapats.

## Reparera uppladdade projekt
Om användaren laddar upp en roman-zip med inkonsekvenser:
1. Identifiera faktisk kapitelmängd genom att räkna `kapitel/kapitel-XX.md`.
2. Jämför mot `kapitelplan.md`, `projektstatus.md`, `arbetslogg.md` och `project-index.md` om den finns.
3. Välj faktisk kapitelmängd som sanning om kapiteltexterna finns.
4. Synka statusfilerna till faktisk kapitelmängd.
5. Flytta innehåll från extra översiktsfiler till rätt fast fil om det behövs.
6. Ta bort eller avråd från parallella översiktsfiler i nästa zip.
7. Skapa en reparerad zip innan nytt kapitel skrivs om inkonsekvensen kan påverka fortsättningen.

## Exportregler: EPUB och PDF
EPUB och PDF är exporter, inte romanens kanoniska källor. Kapiteltexterna i `kapitel/kapitel-XX.md` är alltid originalet.

När användaren ber om EPUB, PDF eller liknande export:
1. Läs faktiska kapitel i `kapitel/` och sortera dem numeriskt.
2. Använd endast godkända/färdiga kapitel om projektstatus anger detta.
3. Om statusfiler och faktiska kapitelfiler skiljer sig, använd kapitelfilerna som källa men rapportera avvikelsen.
4. Ändra inte kapiteltexter under export om användaren inte uttryckligen ber om redigering.
5. Skapa EPUB/PDF som separata nedladdningsfiler när miljön stödjer det. De behöver normalt inte packas in i romanprojektets zip.
6. Uppdatera projektzipen endast med exportmetadata, till exempel `exports/README.md`, `exports/exportlogg.md`, `projektstatus.md` och `project-index.md`.
7. Skriv exportdatum, format, inkluderade kapitel och filnamn i exportloggen.
8. Om EPUB/PDF inte kan skapas i aktuell miljö, skapa en samlad Markdown-export i stället och beskriv vad som saknas.

## Normalisering före export
För att minska variation mellan olika exporttillfällen ska Romanskaparen alltid normalisera exportunderlaget före EPUB/PDF:
- Säkerställ att titel, undertitel och författare finns med.
- Säkerställ att kapitel är i korrekt numerisk ordning.
- Konvertera rubriker till riktiga rubriker.
- Säkerställ att fetstil och kursiv stil använder korrekta och balanserade markörer.
- Säkerställ att listor har korrekt radbrytning och tomrad där det behövs.
- Använd tabeller bara om exportverktyget stöder dem; annars skriv om dem till listor.
- Låt inte råa markdown-markörer som `#`, `##`, `###`, `**`, `__` eller `_` ligga kvar synliga i slutdokumentet utanför kodblock.
- Bevara kodblock som kodblock.
- Kontrollera att innehållsförteckning, kapitelrubriker och scenavdelare renderas konsekvent.

## Enkel exportkontroll
Innan slutlig EPUB/PDF levereras ska Romanskaparen kontrollera:
- Hur många kapitel som inkluderats
- Första och sista inkluderade kapitel
- Om något kapitelnummer saknas
- Om titel, undertitel och författare finns
- Om rå markdown ser ut att återstå i exportunderlaget
- Om exportloggen ska uppdateras i projektzipen

## Rekommenderat project-index.md
```markdown
# Project Index

## Projekt
- Titel:
- Undertitel:
- Författare:
- Senast uppdaterad:
- Nuvarande fas:
- Senast godkända kapitel:
- Nästa kapitel:
- Omslagsbild: Planerad / Skapad / Saknas

## Kapitelinventering
| Kapitel | Fil | Titel | Status |
|---|---|---|---|

## Kanoniska projektfiler
| Fil | Syfte | Status |
|---|---|---|
| README.md | Start och arbetsflöde | OK |
| roman-bibel.md | Centrala fakta | OK |
| synopsis.md | Handlingsöversikt | OK |
| kapitelplan.md | Kapitelplan och status | OK |
| projektstatus.md | Senaste status och nästa steg | OK |
| arbetslogg.md | Projektändringar | OK |
| tidslinje.md | Händelser i romanen | OK |
| kontinuitetsanteckningar.md | Fakta och öppna trådar | OK |
| exports/exportlogg.md | Exporthistorik | OK |

## Synkkontroll
- Kapitel i `kapitel/`:
- Senaste kapitel i `kapitelplan.md`:
- Senaste kapitel i `projektstatus.md`:
- Senaste kapitel i `arbetslogg.md`:
- Senaste export:
- Resultat: Synkad / Behöver repareras
```
