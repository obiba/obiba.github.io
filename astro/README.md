# OBiBa website (Astro)

Work in progress: the modernized www.obiba.org, replacing the Jekyll site in the parent directory.

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # static site in dist/
```

## Adding a news item

Create `src/content/news/release/<product>/<version>.md`:

```md
---
title: Agate 5.0 Released
date: 2026-09-19
product: agate
summary: One-line summary shown in lists and RSS
---

Release notes in Markdown.
```

It appears on the home page, the news page, the product page and in `/rss.xml`.

## Products

One Markdown file per product in `src/content/products/`. Front matter schema: `src/content.config.ts`.

## Migration notes

- `npm run convert-news` regenerated `src/content/news/` from the Jekyll sources (`_data/news.yml` and the news partials). It's a one-off; edit the Markdown files directly from now on.
- Old URLs `/pages/news/...` and `/pages/products/...` redirect to the new ones (see `astro.config.mjs`).
- Not ported: jobs (no openings; old URLs redirect to /about/), Mica 1 and Onyx legacy product pages (redirected).
- Deployment: `.github/workflows/astro.yml` (manual trigger until cutover).
- `public/assets/obiba-pub.pem` and `public/assets/obiba-rpm.repo` must keep these URLs: servers fetch them in their apt/yum setup.
