#!/usr/bin/env python3
"""Egyesíti az ingatlan-nyilvántartást és a teremfoglalási táblát az app számára.

Bemenet:  data/rooms.json          (tools/parse-rooms.py)
          <timetable>.json         (tools/parse-timetable.py)
Kimenet:  data/termek.json

A két forrás a hivatalos teremnéven találkozik: a férőhelyek az összes közös
teremnél egyeznek. A nyilvántartás az F03/F04/F07-et egyetlen osztható
teremként viszi, az órarend háromfelé — a felszereltséget mindháromra
átvesszük. Az F09-nek nincs nyilvántartási tétele, ott az órarendi férőhely
marad.

Használat: python3 tools/build-termek.py data/rooms.json tt.json data/termek.json [2026-08-31]
"""
import json, sys, re, datetime, collections

def main(rooms_p, tt_p, out_p, since=None):
    reg = json.load(open(rooms_p, encoding="utf-8"))
    tt = json.load(open(tt_p, encoding="utf-8"))

    # nyilvántartás indexelése: az "F03 - F04 - F07" mindhárom névre felkerül
    info = {}
    for r in reg:
        for part in [p.strip() for p in r["nev"].split(" - ")]:
            info[part.upper()] = r

    slots = tt["slots"]
    if since:
        slots = [s for s in slots if s["date"] >= since]

    per = {}
    by = collections.defaultdict(list)
    for s in slots:
        per[str(s["period"])] = s["time"]
        by[s["room"]].append([s["date"], s["period"], s["faculty"], s["kind"]])

    ALIAS = {"AM": "AUDMAX"}          # az órarend AM-je a nyilvántartás Audmaxa
    rooms = []
    for name in sorted(by, key=lambda n: -tt["capacity"].get(n, 0)):
        reg_r = info.get(ALIAS.get(name, name).upper())
        rooms.append({
            "nev": name,
            "cim": (reg_r or {}).get("nev", name),
            "fero": tt["capacity"].get(name) or (reg_r or {}).get("ferohely"),
            "felsz": (reg_r or {}).get("felszereltseg", []),
            "url": (reg_r or {}).get("url"),
            "slots": sorted(by[name]),
        })

    days = sorted({s[0] for r in rooms for s in r["slots"]})
    out = {
        "generated": datetime.date.today().isoformat(),
        "from": days[0], "to": days[-1],
        "periods": dict(sorted(per.items(), key=lambda kv: int(kv[0]))),
        "rooms": rooms,
    }
    json.dump(out, open(out_p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"{len(rooms)} terem, {sum(len(r['slots']) for r in rooms)} foglalás, "
          f"{days[0]} .. {days[-1]} -> {out_p}")
    for r in rooms:
        print(f"   {r['nev']:<5} {str(r['fero']):>4} fő  {len(r['slots']):>3} foglalás  "
              f"{'nyilvántartásban' if r['url'] else 'NINCS a nyilvántartásban':<24} {r['cim']}")

if __name__ == "__main__":
    main(*sys.argv[1:])
