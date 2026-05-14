# Projektstruktur och synkronisering

Syftet med denna guide är att Romanskaparen alltid ska skapa samma romanprojektstruktur och hålla statusfilerna i synk med genererade kapitel.

## Grundregel

Ett romanprojekt ska vara ett litet, stabilt arkiv. Skapa inte nya status- eller översiktsfiler med varierande namn. Uppdatera de fasta filerna i stället.

## Fast filstruktur

```text
romanskaparen-projekt/
  README.md
  project-index.md
  roman-bibel.md
  synopsis.md
  kapitelplan.md
  stilguide.md
  tidslinje.md
  projektstatus.md
  kontinuitetsanteckningar.md
  revisionsonskemal.md
  arbetslogg.md
  karaktarer/
    huvudperson.md
    antagonist.md
    bifigurer.md
  kapitel/
    kapitelmall.md
    kapitel-01.md
    kapitel-02.md
```

Tillåtna kapitelmappar och filer:
- Ett godkänt kapitel sparas som `kapitel/kapitel-XX.md`.
- `XX` är alltid två siffror: `01`, `02`, `03`.
- `kapitel/kapitelmall.md` är mall, inte ett skrivet kapitel.

Undvik:
- `projektoversikt-efter-kapitel-24.md`
- `status-v2.md`
- `kapitel-24-sammanfattning.md`
- nya parallella filer som duplicerar status, synopsis eller kontinuitet

Om en särskild översikt behövs, lägg den som en daterad sektion i `projektstatus.md`, `synopsis.md` eller `kontinuitetsanteckningar.md`.

## Single source of truth

Använd dessa filer för respektive typ av information:

| Information | Primär fil |
|---|---|
| Senaste godkända kapitel, nästa steg, fas | `projektstatus.md` |
| Kapitelnummer, titlar, plan och status | `kapitelplan.md` |
| Faktiska kapiteltexter | `kapitel/kapitel-XX.md` |
| Vad som hänt i projektarbetet | `arbetslogg.md` |
| Handlingen i stort | `synopsis.md` |
| Kronologiska händelser i romanen | `tidslinje.md` |
| Fakta som inte får motsägas | `kontinuitetsanteckningar.md` |
| Karaktärsfakta | `karaktarer/*.md` och sammanfattning i `roman-bibel.md` |
| Filinventering och synkstatus | `project-index.md` |

## Synkpassering efter varje godkänt kapitel

När användaren godkänt ett kapitel och vill uppdatera zipen, gör alltid detta innan zipen skapas:

1. Spara kapitlet som `kapitel/kapitel-XX.md`.
2. Uppdatera raden för kapitlet i `kapitelplan.md` till `Godkänt/sparat`.
3. Lägg till nästa planerade kapitel om planen har vuxit.
4. Uppdatera `projektstatus.md`:
   - nuvarande fas
   - senast godkända kapitel
   - nästa rekommenderade steg
   - öppna beslut och risker
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


## Exportregler: EPUB och andra format

EPUB är en export, inte romanens kanoniska källa. Kapiteltexterna i `kapitel/kapitel-XX.md` är alltid originalet. När användaren ber om EPUB, Markdown-samling eller liknande export:

1. Läs faktiska kapitel i `kapitel/` och sortera dem numeriskt.
2. Använd endast godkända/färdiga kapitel om projektstatus anger detta.
3. Om statusfiler och faktiska kapitelfiler skiljer sig, använd kapitelfilerna som källa men rapportera avvikelsen.
4. Ändra inte kapiteltexter under export om användaren inte uttryckligen ber om redigering.
5. Skapa EPUB som separat nedladdningsfil när miljön stödjer det. Den behöver normalt inte packas in i romanprojektets zip.
6. Uppdatera projektzipen endast med exportmetadata, till exempel `exports/README.md`, `exports/exportlogg.md`, `projektstatus.md` och `project-index.md`.
7. Skriv exportdatum, inkluderade kapitel och filnamn i exportloggen.
8. Om EPUB inte kan skapas i aktuell miljö, skapa en samlad Markdown-export i stället och beskriv vad som saknas.

Rekommenderad exportkatalog i romanprojektet:

```text
exports/
  README.md
  exportlogg.md
```

EPUB-innehåll:
- titel
- författare eller pseudonym om angiven
- eventuell undertitel eller baksidestext
- innehållsförteckning
- kapitel i numerisk ordning

## Rekommenderat project-index.md

```markdown
# Project Index

## Projekt
- Titel:
- Senast uppdaterad:
- Nuvarande fas:
- Senast godkända kapitel:
- Nästa kapitel:

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

## Synkkontroll
- Kapitel i `kapitel/`: 
- Senaste kapitel i `kapitelplan.md`: 
- Senaste kapitel i `projektstatus.md`: 
- Senaste kapitel i `arbetslogg.md`: 
- Resultat: Synkad / Behöver repareras
```
