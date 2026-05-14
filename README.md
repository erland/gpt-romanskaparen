# Romanskaparen GPT-paket

Detta paket innehåller material för att skapa en Custom GPT som guidar användaren genom att planera, skriva och vidareutveckla en roman steg för steg.

## Rekommenderad GPT-konfiguration

**Namn:** Romanskaparen

**Beskrivning:**
En guidande skrivpartner för romanprojekt. Hjälper nya och erfarna författare att utveckla idé, synopsis, karaktärer, kapitelplan och skriva romanen kapitel för kapitel med kontinuitet och tydlig struktur.

## Filer

- `gpt-instructions.md` – huvudinstruktioner att klistra in i GPT Builder.
- `conversation-starters.md` – förslag på conversation starters.
- `knowledge/` – stödmaterial som kan laddas upp som Knowledge.
- `templates/romanprojekt/` – mall för hur ett romanprojekt kan paketeras som zip och byggas på successivt.

## Rekommenderade capabilities

- Web browsing: Av, om romanen inte kräver research.
- Canvas: På, om tillgängligt.
- Code interpreter / filskapande: På, om GPT:n ska kunna skapa och uppdatera zip-filer.
- Image generation: Valfritt, användbart för omslag, miljöbilder eller karaktärskoncept.

## Rekommenderat arbetssätt

Romanskaparen bör arbeta i två huvudlägen:

1. **Starta nytt romanprojekt**
   - Samlar in grundidé och mål.
   - Skapar synopsis, romanbibel, kapitelplan, stilguide, tidslinje och karaktärsblad.
   - Erbjuder att paketera projektet som zip.

2. **Fortsätt på befintligt romanprojekt**
   - Användaren laddar upp projekt-zipen.
   - GPT:n läser projektfilerna.
   - GPT:n identifierar nästa rimliga steg eller kapitel.
   - GPT:n skriver nytt material i chatten först.
   - När användaren är nöjd uppdateras projektpaketet.

## Viktig princip

Chatten är arbetsytan där användaren granskar och justerar texten.
Zip-filen är projektarkivet som bevarar plan, kapitel, kontinuitet och historik.


## Genrekunskap

Den här versionen innehåller praktiska knowledge-filer för genrer. De är avsedda att laddas upp som GPT Knowledge tillsammans med övriga filer i `knowledge/`.

Tillagda genreguider:

- `knowledge/genrer/genreoversikt.md`
- `knowledge/genrer/fantasy.md`
- `knowledge/genrer/deckare-mysterium.md`
- `knowledge/genrer/thriller.md`
- `knowledge/genrer/romance.md`
- `knowledge/genrer/skraeck.md`
- `knowledge/genrer/science-fiction.md`
- `knowledge/genrer/historisk-roman.md`
- `knowledge/genrer/barn-och-ungdom.md`
- `knowledge/genrer/litterar-realistisk.md`

Guiderna ska hjälpa Romanskaparen att ställa bättre frågor, skapa bättre kapitelplaner och hålla rätt tempo och läsarförväntningar för olika genrer.

## Nybörjar- och hantverksstöd

Den här versionen innehåller även praktiska stöd för ovana författare och för kapitelvis förbättring:

- `knowledge/forsta-gangen-guide.md` – hjälper GPT:n starta enkelt och bygga en minsta fungerande romanidé.
- `knowledge/konflikt-och-insatser.md` – stöd för mål, hinder, insatser och eskalering.
- `knowledge/scenmall.md` – stöd för att planera och förbättra scener.
- `knowledge/dialogguide.md` – stöd för mer levande dialog med röst och undertext.
- `knowledge/revisionsprocess.md` – stegvis revisionsprocess från struktur till slutputs.
- `templates/romanprojekt/projektstatus.md` – gör det lättare att fortsätta projektet i en ny chatt.
- `templates/romanprojekt/kapitel/kapitelmall.md` – planerings- och uppföljningsmall för varje kapitel.

Rekommendationen är att Romanskaparen först säkrar romanens kärna: huvudperson, mål, hinder, insats och förändring. Därefter kan romanbibeln, kapitelplanen och första kapitlet byggas ut.

## Notering om GPT-instruktionens längd

`gpt-instructions.md` är avsiktligt komprimerad för att hålla sig under GPT Builder-gränsen på 8000 tecken. Mer detaljerad vägledning ligger i `knowledge/` och bör laddas upp som knowledge-filer.


## Uppdatering: stabil projektstruktur

Denna version innehåller `knowledge-upload/05-projektstruktur-och-synk.md` och `templates/romanprojekt/project-index.md` för att GPT:n ska skapa samma filer varje gång och hålla kapitel, status, arbetslogg, tidslinje och kontinuitet synkade.


## EPUB-export

Paketet stödjer att Romanskaparen skapar en EPUB-fil på begäran. EPUB ska normalt levereras som en separat nedladdningsfil, medan romanprojektets zip fortsätter vara källarkivet med kapitel, status och exportlogg.
