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

### Egyszeri beállítás

A workflow csak akkor tud publikálni, ha a Pages forrása a GitHub Actions:

1. **Settings → Pages**
2. **Build and deployment → Source:** válaszd a **GitHub Actions** opciót

Ezután az első push (vagy kézi indítás) már élesíti az oldalt. Az URL az Actions
futás összegzésében és a **Settings → Pages** oldalon is megjelenik.

> Ha a deploy `Branch not allowed to deploy` hibával áll meg, akkor a
> `github-pages` environment ághoz van kötve: **Settings → Environments →
> github-pages → Deployment branches** alatt engedélyezd az ágat, amelyikről
> deployolsz.

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
