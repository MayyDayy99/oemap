#!/usr/bin/env python3
"""Az ingatlan.uni-obuda.hu/termek listaoldalairól kinyeri a termeket.

A lapok kliensoldali szűrővel működnek, de maga a lista sima szerverrendered
HTML: kártyánként egy <h2> a névvel, egy <h3> a férőhellyel, ikonok title
attribútumában a felszereltség, és egy /terem/<slug> hivatkozás. Épületet a
kártya nem hordoz — ahhoz a helyszínre szűrt lista vagy a részletoldal kell.

Használat:  python3 tools/parse-rooms.py mentett*.htm > data/rooms.json
"""
import sys, re, html, json

CARD = re.compile(
    r'<h2[^>]*>(?P<name>.*?)</h2>\s*'
    r'<h3[^>]*>Férőhelyek:\s*(?P<cap>[\d\s]+)\s*fő</h3>'
    r'(?P<mid>.*?)href="(?P<url>[^"]*/terem/(?P<slug>[^"/]+))"',
    re.S)


def parse(path):
    src = open(path, encoding="utf-8", errors="replace").read()
    for m in CARD.finditer(src):
        yield {
            "nev": html.unescape(re.sub(r"<[^>]+>", "", m.group("name"))).strip(),
            "ferohely": int(m.group("cap").replace(" ", "")),
            "slug": m.group("slug"),
            "url": m.group("url"),
            "felszereltseg": sorted({html.unescape(t)
                                     for t in re.findall(r'title="([^"]+)"', m.group("mid"))}),
        }


def main(paths):
    rooms = {}
    for p in paths:
        for r in parse(p):
            rooms[r["slug"]] = r
    out = sorted(rooms.values(), key=lambda r: r["nev"])
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print(f"\n{len(out)} terem, {len(paths)} lapról", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
