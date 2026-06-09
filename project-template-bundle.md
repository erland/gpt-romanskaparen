# Romanprojektmall

Detta är en samlad mall för romanprojekt. Den behöver normalt inte laddas upp som GPT knowledge om GPT:n redan har instruktioner om projektpaket, men kan användas som referens eller kopieras när ett nytt romanprojekt skapas.

## README.md

```markdown
# Romanprojekt

Detta är projektarkivet för en roman som utvecklas steg för steg.

## Rekommenderat arbetsflöde

1. Planera romankärnan: huvudperson, mål, hinder, insats och förändring.
2. Skapa synopsis, kapitelplan, romanbibel och stilguide.
3. Skriv ett kapitel i taget i chatten.
4. Justera kapitlet tills användaren är nöjd.
5. Uppdatera projektfilerna och projektstatus.
6. Fortsätt med nästa kapitel eller revision.

## Viktiga filer

- `projektstatus.md` visar nuvarande fas, senaste godkända kapitel och nästa rekommenderade steg.
- `roman-bibel.md` innehåller projektets centrala fakta.
- `synopsis.md` sammanfattar hela handlingen.
- `kapitelplan.md` är färdplanen för romanen.
- `stilguide.md` håller språk, ton och perspektiv konsekvent.
- `tidslinje.md` håller ordning på händelser.
- `kontinuitetsanteckningar.md` fångar fakta som inte får motsägas.
- `revisionsonskemal.md` samlar planerade förbättringar.
- `arbetslogg.md` visar vad som har gjorts.
- `kapitel/` innehåller godkända kapitel som ska kunna exporteras.
- `kapitelnoteringar.md` innehåller anteckningar som inte ska exporteras.
- `publishing/` innehåller metadata och sättningsregler för EPUB/PDF.

```


---

## project-index.md

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
| 1 | kapitel/kapitel-01.md |  | Ej skrivet |

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

---

## arbetslogg.md

```markdown
# Arbetslogg

## Logg

| Datum | Ändring | Kommentar |
|---|---|---|
|  | Projekt skapat |  |

## Nästa rekommenderade steg

- Fyll i romanbibel.
- Skapa synopsis.
- Skapa kapitelplan.

```

---

## kapitel/kapitel-01.md

```markdown
# 1. [Titel]

[Kapiteltext placeras här när användaren godkänt versionen i chatten.]

```

---

## kapitel/kapitelmall.md

```markdown
# X. [Kapitelrubrik]

## Kapitelmål

Vad ska kapitlet åstadkomma i berättelsen?

## Startläge

Var befinner sig huvudpersonen praktiskt och känslomässigt när kapitlet börjar?

## Viktiga scener

### Scen 1

- Perspektivperson:
- Scenmål:
- Motstånd:
- Förändring:

### Scen 2

- Perspektivperson:
- Scenmål:
- Motstånd:
- Förändring:

## Konflikt

Vad gör kapitlet svårt, spänt eller betydelsefullt?

## Vändning

Vad förändras i kapitlet?

## Slutpunkt

Vilken fråga, känsla eller situation leder vidare till nästa kapitel?

## Kapiteltext

[Kapiteltext]


```

---

## kapitelplan.md

```markdown
# Kapitelplan

## Översikt

| Kapitel | Titel | Syfte | Viktiga händelser | Status |
|---|---|---|---|---|
| 1 |  | Introducera huvudperson och startläge |  | Ej skrivet |

## Kapitelanteckningar

### Kapitel 1
- Mål:
- Konflikt:
- Slutpunkt:

```

---

## karaktarer/antagonist.md

```markdown
# Antagonist eller motkraft

## Namn eller beskrivning

## Roll

## Mål

## Motivation

## Metoder

## Koppling till huvudpersonen

## Varför motkraften är trovärdig

## Utveckling genom romanen

```

---

## karaktarer/bifigurer.md

```markdown
# Bifigurer

## Bifigur 1

- Namn:
- Funktion i berättelsen:
- Relation till huvudpersonen:
- Viktig utveckling:

## Bifigur 2

- Namn:
- Funktion i berättelsen:
- Relation till huvudpersonen:
- Viktig utveckling:

```

---

## karaktarer/huvudperson.md

```markdown
# Huvudperson

## Namn

## Roll

## Yttre mål

## Inre behov

## Rädsla

## Styrkor

## Svagheter

## Relationer

## Hemlighet eller konflikt

## Utveckling genom romanen

```

---

## kontinuitetsanteckningar.md

```markdown
# Kontinuitetsanteckningar

## Fasta fakta

## Karaktärsfakta

## Relationsutveckling

## Miljöfakta

## Ledtrådar och planteringar

## Öppna frågor

## Saker som måste följas upp

## Saker som inte får motsägas

```

---

## projektstatus.md

```markdown
# Projektstatus

## Nuvarande fas

Planering / Kapitelutkast / Revision / Slutputs

## Senast godkända kapitel eller del

- Senast godkända: [exempel: Kapitel 1]
- Senast ändrad: [exempel: Kapitel 2, ej godkänt]

## Nästa rekommenderade steg

[Beskriv nästa konkreta steg, till exempel: Skriv kapitel 3 enligt kapitelplanen eller revidera dialogen i kapitel 2.]

## Viktiga öppna beslut

- [Beslut 1]
- [Beslut 2]

## Risker att bevaka

- [Exempel: Huvudpersonen behöver agera mer aktivt.]
- [Exempel: För mycket bakgrundsinformation kommer för tidigt.]
- [Exempel: Mysteriets ledtrådar behöver planteras rättvist.]

## Kontinuitet som måste följas upp snart

- [Punkt 1]
- [Punkt 2]

## Användarens aktuella önskemål

- [Ton, stil, ändringar eller prioriteringar]

```

---

## revisionsonskemal.md

```markdown
# Revisionsönskemål

Här samlas saker som ska förbättras senare men inte behöver stoppa framåtskrivandet.

| Plats | Önskad ändring | Prioritet | Status |
|---|---|---|---|

```

---

## roman-bibel.md

```markdown
# Romanbibel

## Arbetstitel

## Genre

## Målgrupp

## Ton och känsla

## Premiss

## Huvudkonflikt

## Teman

## Huvudperson

## Antagonist eller motkraft

## Viktiga bifigurer

## Miljö och värld

## Centrala regler och begränsningar

## Viktiga återkommande motiv

## Slutets riktning

```

---

## stilguide.md

```markdown
# Stilguide

## Språk

## Berättarperspektiv

## Tempus

## Meningslängd och rytm

## Dialogstil

## Beskrivningsnivå

## Ton

## Saker att undvika

## Exempel på önskad känsla

```

---

## synopsis.md

```markdown
# Synopsis

## Kort baksidestext

## Sammanfattning av hela handlingen

## Början

## Mitt

## Slut

## Viktiga vändpunkter

## Viktiga avslöjanden

## Saker som måste planteras tidigt

```

---

## tidslinje.md

```markdown
# Tidslinje

## Före romanens början

## Under romanen

| Tidpunkt | Händelse | Berörda karaktärer | Kapitel |
|---|---|---|---|

## Efter romanens slut

```

---

## exports/README.md

```markdown
# Exporter

Denna katalog innehåller metadata om genererade exporter, till exempel EPUB.
Exporter är inte romanens kanoniska källtext. De kan återskapas från `kapitel/kapitel-XX.md`.
EPUB-filer behöver normalt inte ligga i projektzipen. När användaren begär EPUB kan den ges som en separat nedladdningsfil.
```

## exports/exportlogg.md

```markdown
# Exportlogg

| Datum | Format | Filnamn | Inkluderade kapitel | Kommentar |
|---|---|---|---|---|
```


## Uppdatering
Projektmallen ska också innehålla titel, undertitel, författare och omslagsstatus samt följa exportreglerna för EPUB/PDF enligt `05-projektstruktur-och-synk.md`.

---

## kapitelnoteringar.md

```markdown
# Kapitelnoteringar

Kapitelnoteringar sparas här och ska inte ligga i `kapitel/kapitel-XX.md`.

## Kapitel 1 – Kapitelrubrik
- Kort sammanfattning:
- Nya fakta/ledtrådar:
- Kontinuitetsrisker:
- Öppna frågor:
- Nästa skrivsteg:
```

---

## publishing/metadata.yaml

```yaml
---
title: "[Titel]"
subtitle: "[Undertitel]"
author: "[Författare]"
lang: sv-SE
rights: "© [År] [Författare]"
cover-image: "omslag/cover.jpg"
toc-depth: 1
---
```

---

## publishing/epub.css

```css
/* Romanskaparen EPUB-standard v4 */
body {
  line-height: 1.45;
  margin: 0;
  padding: 0;
  widows: 2;
  orphans: 2;
}

/* Varje kapitel ligger normalt i en egen XHTML-fil. Lägg därför INTE
   page-break-before/break-before på kapitelrubriken i EPUB, eftersom
   TOC-länkar då kan öppna en tom sida före kapitlet i flera läsare. */
section.level1 > h1,
h1.chapter-heading,
h1 {
  text-align: center;
  font-weight: normal;
  line-height: 1.08;
  margin-top: 0.8em;
  margin-bottom: 0.35em;
  page-break-before: auto;
  break-before: auto;
}

.chapter-number {
  display: block;
  text-align: center;
  font-size: 1.45em;
  letter-spacing: 0.06em;
  line-height: 1.05;
  margin: 0 0 0.08em 0;
  font-weight: normal;
}

.chapter-title,
.chapter-name {
  display: block;
  text-align: center;
  font-size: 1.30em;
  line-height: 1.12;
  margin: 0 0 0.20em 0;
  font-weight: normal;
}

.titlepage {
  text-align: center;
  margin-top: 25vh;
}

.titlepage h1,
.titlepage .subtitle,
.titlepage .author,
.book-title,
.book-subtitle,
.book-author {
  text-align: center;
  text-indent: 0;
}

p {
  margin: 0 0 0.8em 0;
  text-indent: 0;
}

hr {
  border: 0;
  text-align: center;
  margin: 1.2em 0;
}

hr::after {
  content: "* * *";
  letter-spacing: 0.4em;
}
```

---

## publishing/build-notes.md

```markdown
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
```


---

## publishing/fix-epub-after-pandoc.py

```python
#!/usr/bin/env python3
"""Efterbearbetar en Pandoc-EPUB enligt Romanskaparens standard v4.

Mål:
1. Behåll den navigerbara EPUB-TOC:en/nav.xhtml som index i läsaren.
2. Visa inte nav.xhtml som en vanlig innehållsförteckningssida i bokflödet.
3. Neutralisera CSS-regler som kan skapa tom sida före kapitelrubriken.

Viktigt: Ta normalt inte bort nav-itemref helt. Sätt hellre linear="no" för
bättre kompatibilitet med EPUB-läsare som förväntar sig nav i spine men inte
ska visa den i den linjära läsordningen.
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


def find_nav_ids(opf_text: str) -> set[str]:
    ids: set[str] = set()
    item_re = re.compile(r"<item\b[^>]*>", re.IGNORECASE)
    id_re = re.compile(r'\bid=["\']([^"\']+)["\']', re.IGNORECASE)
    prop_re = re.compile(r'\bproperties=["\'][^"\']*\bnav\b[^"\']*["\']', re.IGNORECASE)
    href_nav_re = re.compile(r'\bhref=["\'][^"\']*(?:nav|toc)[^"\']*\.xhtml["\']', re.IGNORECASE)
    for m in item_re.finditer(opf_text):
        item = m.group(0)
        if prop_re.search(item) or href_nav_re.search(item):
            id_m = id_re.search(item)
            if id_m:
                ids.add(id_m.group(1))
    if not ids:
        ids.add("nav")
    return ids


def hide_nav_in_spine(opf_text: str) -> str:
    nav_ids = find_nav_ids(opf_text)
    for nav_id in nav_ids:
        # itemref self-closing without linear: add linear="no"
        opf_text = re.sub(
            rf'(<itemref\b(?=[^>]*\bidref=["\']{re.escape(nav_id)}["\'])(?![^>]*\blinear=)[^>]*)/?>',
            lambda m: m.group(1).rstrip().rstrip('/') + ' linear="no"/>',
            opf_text,
            flags=re.IGNORECASE,
        )
        # itemref with linear yes/true: change to no
        opf_text = re.sub(
            rf'(<itemref\b(?=[^>]*\bidref=["\']{re.escape(nav_id)}["\'])[^>]*\blinear=)["\'](?:yes|true|1)["\']',
            r'\1"no"',
            opf_text,
            flags=re.IGNORECASE,
        )
    return opf_text


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: fix-epub-after-pandoc.py input.epub [output.epub]")
        return 2

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) == 3 else src
    if not src.exists():
        print(f"Missing file: {src}")
        return 2

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        with zipfile.ZipFile(src) as zf:
            zf.extractall(tmp)

        for opf in tmp.rglob("*.opf"):
            text = opf.read_text(encoding="utf-8")
            text = hide_nav_in_spine(text)
            opf.write_text(text, encoding="utf-8")

        for css in tmp.rglob("*.css"):
            text = css.read_text(encoding="utf-8")
            text = text.replace("page-break-before: always;", "page-break-before: auto;")
            text = text.replace("break-before: page;", "break-before: auto;")
            css.write_text(text, encoding="utf-8")

        out = dst
        if out == src:
            backup = src.with_suffix(src.suffix + ".bak")
            shutil.copy2(src, backup)
        if out.exists():
            out.unlink()
        with zipfile.ZipFile(out, "w") as zf:
            mimetype = tmp / "mimetype"
            if mimetype.exists():
                zf.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
            for path in sorted(tmp.rglob("*")):
                if path.is_file() and path.name != "mimetype":
                    zf.write(path, path.relative_to(tmp).as_posix(), compress_type=zipfile.ZIP_DEFLATED)

    print(f"Fixed EPUB: {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

---

## Chatt- och zip-beteende

När GPT:n arbetar med denna projektmall ska den normalt uppdatera filer och skapa/erbjuda projekt-zip. Den ska inte visa hela kapiteltexten i chatten om användaren inte uttryckligen ber om det. Chattsvaret ska fokusera på ändrade filer, kort sammanfattning, viktiga kontinuitetspunkter och nästa steg.
