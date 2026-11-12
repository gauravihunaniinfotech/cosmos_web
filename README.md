# COSMO'S Heating & Air Conditioning — Homepage Redesign

Files: `index.html`, `style.css`, `script.js`, `assets/images/`. Plain HTML/CSS/vanilla JS.

## Run at http://localhost:5500
**VS Code Live Server:** install the *Live Server* extension → right-click `index.html` → **Open with Live Server** (port 5500 preconfigured in `.vscode/settings.json`).
**Or Python:** `python3 serve.py` (Windows: `python serve.py`) → open http://localhost:5500 in Chrome.

## Images
Photos in `assets/images/` were cropped from the original-site screenshot (low resolution, used as offline fallbacks).
When online, `script.js` automatically swaps each one for the full-resolution original hosted on the current site's image CDN (`data-hires` attributes in `index.html`).
For a fully self-hosted site, save the original files from your Wix media library into `assets/images/` and update the `src` attributes. The hero fallback is an illustration until the real skyline photo loads.

## Before launch
- The three testimonial cards are placeholders — paste real Google reviews.
- The contact form is demo-only; set `data-endpoint` on `<form id="lead-form">` to a Formspree/other JSON endpoint to receive leads.
- Real details used: (702) 960-5555, service@cosmosaclv.com, 10161 W Park Run Dr #150 Las Vegas NV 89145, License #0095036, 5.0 / 10 Google reviews, Housecall Pro booking link.

## About page (`about.html`)
Files: `about.html`, `css/about.css`, `js/about.js`. Open http://localhost:5500/about.html.

**Photos:** real project photos only (no illustrations). They live in `assets/about/` (copies/crops of the project photos already on the site, because no other real photos were available). Replace any file in that folder with a higher-resolution photo of the same name — or change the `src` in `about.html` — and the layout adapts. The originals are only ~350px wide, so new, larger photos will look noticeably sharper.

**Timeline:** the three `[Year]` markers (class `is-placeholder`) are placeholders — replace with real dates.

Homepage header/footer "About" links point to `about.html`.

## Services & Comfort Club pages
- `services.html`, `comfort-club.html` — styled by `style.css` + `css/about.css` (shared atoms) + `css/pages.css`; scripts `script.js`, `js/about.js` (reveals/animations), `js/pages.js` (FAQ).
- `python3 tools/build_inner.py` regenerates both pages and syncs header/footer links on all four pages (header/footer/icon sprite are copied from `about.html`). You can also edit the HTML files directly.
- Photos: `assets/services/*.jpg`, `assets/club/*.jpg` (real project photos from the site, cropped per section — swap any file for a larger photo of the same name).
- Comfort Club plan details are placeholders: edit the `<dl>` in the `#plans` section of `comfort-club.html`. Benefit wording is marked `VERIFY` in an HTML comment — confirm against your actual agreement.
- No `og:image` yet (TODO comment in each `<head>`).
