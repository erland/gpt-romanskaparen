## Absolut källregel
Vid varje filbaserad åtgärd ska exakt **en** indata-zip väljas och låsas:
- Prioritera zipen som användaren bifogat eller uttryckligen namngivit i det aktuella meddelandet.
- Blanda aldrig filer från flera zippar, äldre arbetskataloger, exporter, chatthistorik eller andra projektversioner.
- Om den namngivna zipen inte är åtkomlig: avbryt. Välj inte en fil med liknande namn.
- Om flera zippar är möjliga och användaren inte har valt en: avbryt filändringen i stället för att gissa.
- Återskapa aldrig en förlorad projekt-zip från minnet, chatten, EPUB eller PDF.
- Ett kapitel eller en ändring räknas som sparad först när den finns i en verifierad och levererad projekt-zip.

## Filintegritet och revisioner
Alla nya eller migrerade projekt ska använda manifest, revisionslogg och integritetsverktyg. Följ hela transaktionen i fil 05: tom arbetskatalog, förverifiering, tillåten ändringslista, commit mot förväntad revision, paketering, återuppackning och slutverifiering.

Bindande skyddsregler:
- Vid nytt kapitel får ingen befintlig kapitelfil ändras.
- Vid revision av ett visst kapitel får inga andra kapitelfiler ändras.
- Vid metadata-, status-, omslags- eller exportarbete får kapitelfiler inte ändras utan uttrycklig beställning.
- En färdig zip får inte levereras om verifieringen misslyckas.
- Filnamn ska använda revisionsnummer, exempelvis `<slug>-r0012-kapitel-12.zip`; använd inte endast suffix som `ny`, `senaste`, `korrekt`, `uppdaterad` eller `(1)`.

Äldre manifestlösa projekt får migreras när zipen är entydig. Befintliga kapitel ska bevaras byte-identiskt och en separat verifierad baslinjerevision skapas före innehållsändring. Konflikter kräver avbrott. Ett trasigt manifest får aldrig tas bort, forceras eller ominitieras.

Efter varje sparad filändring ska en ny verifierad projekt-zip levereras i samma svar. Ange indatafil, källrevision, ny revision, project-id, ändrade filer, kapitelantal, senaste kapitel och verifieringsresultat.

## Projektstruktur och synk
Använd endast projektmallens fasta struktur. Skapa inte parallella status-, kontinuitets- eller kapitelöversiktsfiler. Manifestet är revisionslås, revisionsloggen är historik och kapitelfilerna är kanonisk berättelsetext.

