# OBiBa website

Source of [www.obiba.org](https://www.obiba.org), built with [Astro](https://astro.build). License [GPL v3](https://www.gnu.org/licenses/gpl-3.0.html).

```sh
make prepare     # npm install (Node 22.12+)
make run         # dev server at http://localhost:4321
make build       # static site in dist/
make preview     # serve dist/, e.g. to test redirects
```

Pushing to `master` deploys the site with `.github/workflows/astro.yml`.

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

## Other pages

Markdown files in `src/pages/` (layout `src/layouts/Page.astro`). Images go in `public/img/`.

## Notes

- The site was migrated from Jekyll in October 2026 (see git history before that for the old sources). Old `/pages/...` URLs redirect to the new ones, see `redirects` in `astro.config.mjs`.
- `public/assets/obiba-pub.pem` and `public/assets/obiba-rpm.repo` must keep these URLs: servers fetch them in their apt/yum setup.
- `_graphics/` holds the source artwork (logos, illustrations).
