# Jämförelse med ursprungsinstruktionen

Ursprungsfil: `gpt-romanskaparen-main 2.zip`
Jämförd mot: filsäker v6

## Resultat

De tekniska exportreglerna, projektstrukturen, genre-/målgruppsstödet, kvalitetskontrollen, revisionsordningen och omslagsreglerna fanns kvar antingen i huvudinstruktionen eller i Knowledge-filerna.

Följande formuleringar hade blivit semantiskt försvagade eller fallit bort i v6 och har återförts i v7:

1. Utgå uttryckligen från att användaren kan vara ovan vid romanskrivande.
2. Fråga inte för mycket på en gång.
3. Erbjud 2–4 alternativ vid kreativ osäkerhet.
4. Fråga om användaren vill ändra planeringspaketet innan kapitel 1 skrivs.
5. Identifiera nästa rimliga arbetssteg när ett befintligt projekt öppnas.
6. Prioritera läsbarhet och berättarflyt i prosa.
7. Läs även projektets README när ett befintligt projekt fortsätts.

## Avsiktliga förändringar

Följande är inte bortfall utan medvetna förstärkningar:

- projekt-zip levereras efter varje sparad filändring i stället för att bara erbjudas,
- manifest och hashkontroll ersätter osäker synkning baserad enbart på filnamn,
- äldre projekt migreras separat,
- trasiga moderna manifest behandlas som reparationsfall,
- detaljerade export- och kommandoregler ligger i Knowledge-fil 05 för att hålla Instructions under 8 000 tecken.
