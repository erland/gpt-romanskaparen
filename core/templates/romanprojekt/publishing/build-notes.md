# Build-notes

## Standard
- Källformat: Markdown i `kapitel/`.
- Exportverktyg: Pandoc i första hand.
- EPUB: navigerbar TOC ska finnas i EPUB-läsarens index. `nav.xhtml` ska inte visas som vanlig sida i bokflödet om användaren inte uttryckligen ber om synlig innehållsförteckning; använd helst `linear="no"` för nav-spineposten.
- PDF: klickbar TOC om användaren ber om synlig innehållsförteckning.
- Kapitelstart: nummer och rubrik på två centrerade rader med kompakt spacing.
- TOC-post: `1. Kapitelrubrik`.
- Kapitelnoteringar exporteras inte.

## EPUB-kontroll efter Pandoc
Efter att EPUB skapats ska paketet kontrolleras eller efterbearbetas:
1. `nav.xhtml` ska finnas kvar som navigeringsdokument så EPUB-läsaren visar innehållsförteckning/index. Om `EPUB/content.opf` har nav i `<spine>` ska itemref normalt vara `linear="no"` så sidan inte visas i läsflödet.
2. Kapitelrubriker i EPUB-CSS får inte använda `page-break-before: always` eller `break-before: page`; varje kapitel är redan en egen XHTML-fil. Annars kan TOC-länkar öppna en tom sida före kapitlet.
3. Kapitelrubriken ska vara större än brödtext men kompakt: ungefär `.chapter-number font-size:1.45em`, `.chapter-title font-size:1.30em`, `h1 margin-top:0.8em`, `h1 margin-bottom:0.35em`, `.chapter-number margin-bottom:0.08em`.

## Senaste export
- Datum:
- Format:
- Kommando/metod:
- Kommentar:
