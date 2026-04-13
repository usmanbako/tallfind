# Tallfind — One-Page App Summary

## What it is
- Tallfind is a static web directory for finding tall-friendly clothing stores.
- It curates hand-reviewed entries for men and women, with verified sizing metadata.

## Who it's for
- Primary persona: tall shoppers (men ~6'2"+ and women ~5'9"+) who struggle to find reliable tall sizing across brands.

## What it does
- Loads separate men's and women's store datasets from local JSON files.
- Provides tabbed browsing (Home, Men's, Women's) with URL-synced filter state.
- Supports keyword search across store metadata (name, sizing, notes, categories).
- Filters by tall-only brands, tops, bottoms, favorites, and men's minimum inseam.
- Offers sort modes (tall-first, A–Z, and inseam for men's listings).
- Saves user favorites and analytics consent in localStorage.
- Collects store submissions and feedback via Formspree modal forms.

## How it works (repo evidence)
- Front end: `index.html` + `assets/styles.css` + `assets/app.js` rendered in-browser.
- Data layer: static JSON files (`data/men.json`, `data/women.json`, `data/featured.json`).
- Runtime flow: browser fetches JSON -> JS stores state -> applies search/filter/sort -> renders cards and homepage sections dynamically.
- Integrations: Google Analytics (gtag with consent banner), Formspree form endpoints.
- Backend service/API/database: **Not found in repo.**

## How to run (minimal)
1. From repo root, start any static web server (example): `python3 -m http.server 8000`
2. Open `http://localhost:8000` in a browser.
3. Use the directory tabs and filters; submissions/feedback post to Formspree endpoints.

## Notes
- Formal local setup docs beyond a one-line README are **Not found in repo.**
