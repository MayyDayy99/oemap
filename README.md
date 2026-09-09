# OA Épület Teremkereső

Interaktív teremkereső és útvonaltervező az OA épülethez. Egyetlen, önálló HTML
fájl — nincs build lépés, nincs függőség, nincs csomagkezelő.

**Élő oldal:** https://mayydayy99.github.io/oemap/

## Felépítés

| Fájl | Szerep |
| --- | --- |
| `index.html` | Maga az alkalmazás (HTML + CSS + JS egy fájlban) |
| `fonts/` | Saját kiszolgálású betűtípusok + licencek |
| `icons/` | Alkalmazásikonok (a Metropolisszal generálva) |
| `manifest.webmanifest` | PWA leíró — telepíthetőség |
| `sw.js` | Service worker — offline működés |
| `.github/workflows/deploy-pages.yml` | Automatikus deploy GitHub Pages-re |
| `.nojekyll` | Kikapcsolja a Jekyll feldolgozást |

**Nincs külső hivatkozás.** A betűtípusok a `fonts/` mappából jönnek, minden más
— a teremadatok, az alaprajz geometriája, az útvonalkeresés — az `index.html`-en
belül van. Így az oldal külső szolgáltató nélkül, offline is működik.

## Kezelés

| | Alaprajz | Épület |
| --- | --- | --- |
| egy ujj / egér húzás | tolás | **forgatás** — vízszintesen a tengely körül, függőlegesen a dőlés (15°–85°) |
| két ujj | tolás + nagyítás | tolás + nagyítás |
| görgő | nagyítás | nagyítás |
| Shift + húzás (egérrel) | tolás | tolás |
| ⤢ gomb | képre igazít | képre igazít **és visszaállítja az alapállást** |

Az alsó lapot a fejléc bármely pontjáról lehet húzni, és a lista tetejéről lefelé
is. Az elengedés sebessége számít: egy határozott pöccintés a mozgás irányában
lép a következő állásra.

## Telepítés a kezdőképernyőre

Az oldal telepíthető webalkalmazás. Androidon a böngésző menüjében „Alkalmazás
telepítése", iOS-en Safari → Megosztás → „Hozzáadás a főképernyőhöz". Telepítés
után a teljes app offline is elindul — a service worker az első betöltéskor
elteszi a HTML-t, a betűket és az ikonokat. Az épületben, gyenge térerővel is
működik.

Frissítés: a dokumentumot hálózat-először kéri le, így egy új deploy a következő
indításnál azonnal megérkezik; offline a gyorsítótárazott példány jön.

## Arculat

Az Óbudai Egyetem Brand Guide 2026 / 1.0 szerint:

| | |
| --- | --- |
| Elsődleges szín | `#00288C` (sötét téma: `#799AEC`, a brand kék világosított változata) |
| Cím / rövid szöveg | **Metropolis** (400/600/700) |
| Folyó szöveg | **Open Sans** (400/600) |
| Teremkódok | IBM Plex Mono — a `0`/`O` megkülönböztetése tájékozódásnál funkcionális |

Az útvonal narancs marad: tájékozódási szín, nem arculati elem, és a kézikönyv
másodlagos színei közül egyik sem ad elég kontrasztot a világos alaprajzon.
A helyiség-kategóriák színei szintén változatlanok — azok a jelmagyarázathoz
tartoznak, nem a márkamegjelenéshez.

A betűtípusok szabadon terjeszthetők (Metropolis: public domain, Open Sans és
IBM Plex Mono: SIL Open Font License); a licencfájlok a `fonts/` mappában vannak.

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
magától lefut. Ha a fájl újragenerált változatát teszed be, ne felejtsd el a
`fonts/` mappára mutató `@font-face` blokkot és az arculati színeket átvinni.
