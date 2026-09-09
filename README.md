# OA Épület Teremkereső

Interaktív teremkereső és útvonaltervező az OA épülethez. Egyetlen, önálló HTML
fájl — nincs build lépés, nincs függőség, nincs csomagkezelő.

**Élő oldal:** https://mayydayy99.github.io/oemap/

## Felépítés

| Fájl | Szerep |
| --- | --- |
| `index.html` | Maga az alkalmazás (HTML + CSS + JS egy fájlban) |
| `.github/workflows/deploy-pages.yml` | Automatikus deploy GitHub Pages-re |
| `.nojekyll` | Kikapcsolja a Jekyll feldolgozást |

Az egyetlen külső hivatkozás a Google Fonts (IBM Plex család). Minden más — a
teremadatok, az alaprajz geometriája, az útvonalkeresés — a fájlon belül van.

## Deploy

A `deploy-pages.yml` workflow minden pusholásnál lefut, és a repó tartalmát
kirakja GitHub Pages-re. Kézzel is indítható: **Actions → Deploy to GitHub Pages
→ Run workflow**.

### Egyszeri beállítás — ezt kézzel kell megtenni

1. **Settings → Pages**
2. **Build and deployment → Source:** válaszd a **GitHub Actions** opciót

Ezt egyszer kell megcsinálni, és nem lehet automatizálni: az Actions
`GITHUB_TOKEN` deployolni tud a Pages-re, de magát a Pages site-ot létrehozni
nem — ahhoz repo admin jog kell. Amíg ez nincs kész, a workflow a *Setup Pages*
lépésnél `Get Pages site failed` hibával leáll.

Ha megvan, indítsd újra a legutóbbi futást (**Actions → Deploy to GitHub Pages →
Re-run jobs**), vagy pusholj egyet. Az élő URL az Actions futás összegzésében és
a **Settings → Pages** oldalon is megjelenik.

> Ha a deploy `Branch not allowed to deploy` hibával áll meg, akkor a
> `github-pages` environment ághoz van kötve: **Settings → Environments →
> github-pages → Deployment branches** alatt engedélyezd az ágat, amelyikről
> deployolsz.

## Ágak

A repó alapértelmezett ága jelenleg `claude/blissful-goodall-royl5x`, mert egy
üres repóba ez került fel elsőként. Ha átnevezed `main`-re, a deploy attól még
működik — a workflow a `main`, a `master` és ez az ág mindegyikére fut.

## Helyi futtatás

Elég megnyitni a fájlt a böngészőben:

```
open index.html
```

Vagy egy helyi szerverrel:

```
python3 -m http.server 8000
# majd http://localhost:8000
```

## Frissítés

Az alkalmazás cseréjéhez írd felül az `index.html` fájlt, és pushold — a deploy
magától lefut.
