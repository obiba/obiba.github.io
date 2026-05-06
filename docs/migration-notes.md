# Jekyll to MkDocs Migration Notes

## Migration Date

May 6, 2026

## Overview

Complete migration from Jekyll Bootstrap to MkDocs Material.

## Changes

### Technology Stack

- **From:** Jekyll (Ruby) + Bootstrap theme
- **To:** MkDocs (Python) + Material theme

### URL Structure

All previous URLs redirect to new locations:

- Product pages: `/pages/products/{product}/` → `/products/{product}/`
- Static pages: `/pages/{section}/` → `/{section}/`
- News/releases: `/pages/news/release/{product}/{version}/` → `/blog/{date}/{slug}/`
- Events: `/pages/news/event/{name}/` → `/blog/{date}/{slug}/`

### Content Changes

1. **Product Pages:** Converted from HTML includes to Markdown with Material features
2. **News:** Migrated to blog format with categories and dates
3. **Assets:** Migrated to `docs/assets/` directory
4. **Styling:** New custom CSS based on Material theme

### New Features

- Enhanced search with suggestions
- Blog plugin for news and releases
- Dark mode support
- Better mobile responsiveness
- Faster build times
- Improved navigation

### Breaking Changes

None for end users - all URLs redirect properly.

For contributors:
- Content now in Markdown format
- New build command: `mkdocs serve` (instead of `jekyll serve`)
- Python environment required (instead of Ruby)

## Development Workflow

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Serve locally with hot reload
mkdocs serve

# Build site
mkdocs build

# Validate build
./scripts/validate_build.sh
```

### Adding Content

**New product page:**
1. Create `docs/products/{product}/index.md`
2. Add to `nav` section in `mkdocs.yml`

**New blog post:**
1. Create `docs/blog/posts/YYYY-MM-DD-slug.md`
2. Add frontmatter with date, categories, authors

**New static page:**
1. Create `docs/{section}/index.md`
2. Add to `nav` section in `mkdocs.yml`

### Deployment

Automatic via GitHub Actions:
- Push to `main` branch triggers deployment
- PR builds test the site without deploying

## Rollback Plan

If issues arise, revert to Jekyll:
1. `git revert <migration-commit>`
2. Push to main
3. Jekyll site automatically deploys

Backup Jekyll branch: `jekyll-backup`

## Known Issues

None at this time.

## Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Migration Scripts](../scripts/)

## Contact

For questions or issues, contact the OBiBa development team.
