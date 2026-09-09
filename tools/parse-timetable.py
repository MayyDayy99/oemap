#!/usr/bin/env python3
"""Az OA épület teremfoglalási táblájából (terem.xlsx) kompakt JSON-t készít.

A munkafüzet hetenként egy lap. Minden lapon két, egymás alatti táblázat van:
fent egy másik épület termei, lent az OA F-blokkja (AM, F01..F09). Csak az
utóbbit olvassuk. A cella szövege a kart adja (NIK/KVK/RKK), a kitöltőszíne a
foglalás típusát — a jelmagyarázat a lap alján van.

Használat:  python3 tools/parse-timetable.py terem.xlsx data/timetable.json
"""
import json, sys, datetime, collections
import openpyxl

# A lap alján lévő jelmagyarázat színkódjai.
KIND = {
    "idx49": "foglalas",      # Teremfoglalás
    "idx21": "vizsga",        # Vizsga/ZH
    "idx13": "levelezos",     # Levelezős előadás
    "idx43": "tavos",         # Távos előadás
    "idx17": "eloadas",       # Nappali előadás KVK
    "idx45": "eloadas",       # Nappali előadás NIK
}
DAYS = {"HÉTFŐ":1,"KEDD":2,"SZERDA":3,"CSÜTÖRTÖK":4,"PÉNTEK":5,"SZOMBAT":6,"VASÁRNAP":7}
FBLOCK = {"AM","F01","F02","F03","F04","F05","F06","F07","F08","F09"}


def fill(cell):
    f = cell.fill
    if f is None or f.patternType is None:
        return None
    c = f.fgColor
    if c.type == "indexed":
        return f"idx{c.indexed}"
    if c.type == "rgb" and isinstance(c.rgb, str):
        return c.rgb
    if c.type == "theme":
        return f"theme{c.theme}"
    return None


def parse_sheet(ws):
    """A lap F-blokkjának foglalásai: [{date, day, period, time, room, faculty, kind}]"""
    out, caps = [], {}
    for r in range(1, ws.max_row + 1):
        head = [ws.cell(r, c).value for c in range(4, 20)]
        names = [str(v).strip() for v in head if v not in (None, "")]
        if not (names and FBLOCK.issuperset(names)):
            continue                      # nem az F-blokk fejléce

        date = ws.cell(r, 3).value
        date = date.date() if isinstance(date, datetime.datetime) else date
        cols = {c: str(ws.cell(r, c).value).strip()
                for c in range(4, 20) if ws.cell(r, c).value not in (None, "")}
        # a fejléc fölötti sor a férőhely
        for c, name in cols.items():
            v = ws.cell(r - 1, c).value
            if isinstance(v, (int, float)):
                caps[name] = int(v)

        day = None
        for rr in range(r + 1, min(r + 18, ws.max_row + 1)):
            d = ws.cell(rr, 1).value
            if d and str(d).strip().upper() in DAYS:
                day = str(d).strip().upper()
            period, time = ws.cell(rr, 2).value, ws.cell(rr, 3).value
            if not isinstance(period, (int, float)):
                continue
            for c, room in cols.items():
                cell = ws.cell(rr, c)
                if cell.value in (None, ""):
                    continue
                out.append({
                    "date": str(date), "day": DAYS.get(day, 0),
                    "period": int(period), "time": str(time).strip(),
                    "room": room, "faculty": str(cell.value).strip(),
                    "kind": KIND.get(fill(cell), "egyeb"),
                })
    return out, caps


def main(src, dst):
    wb = openpyxl.load_workbook(src, data_only=True)
    rows, caps = [], {}
    for ws in wb.worksheets:
        r, c = parse_sheet(ws)
        rows += r
        caps.update(c)
    rooms = sorted({r["room"] for r in rows})
    weeks = sorted({r["date"] for r in rows})
    data = {
        "generated": datetime.date.today().isoformat(),
        "source": src.split("/")[-1],
        "capacity": caps,
        "rooms": rooms,
        "days": len(weeks),
        "slots": rows,
    }
    with open(dst, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(rows)} foglalás, {len(rooms)} terem, {len(weeks)} nap -> {dst}")
    print("termek:", ", ".join(f"{r} ({caps.get(r,'?')} fő)" for r in rooms))
    kinds = collections.Counter(r["kind"] for r in rows)
    print("típusok:", dict(kinds))
    print("karok:", dict(collections.Counter(r["faculty"] for r in rows).most_common(8)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
