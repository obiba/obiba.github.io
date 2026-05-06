# MkDocs Migration Design Specification

**Date:** 2026-05-06  
**Project:** OBiBa Website (obiba.github.io)  
**Type:** Complete Migration from Jekyll to MkDocs Material

## Executive Summary

This document specifies the complete migration of the OBiBa website from Jekyll Bootstrap to MkDocs Material. The migration will preserve all existing URLs, maintain the multi-product marketing/documentation hybrid structure, modernize the visual design, and simplify the maintenance toolchain by moving from Ruby/Jekyll to Python/MkDocs.

## Goals & Requirements

### Primary Goals

1. **Better Documentation Features**: Enhanced search, navigation, content organization
2. **Simpler Maintenance**: Python toolchain instead of Ruby, easier content authoring
3. **Modern Theme**: Visual refresh with MkDocs Material's design system
4. **Python Integration**: Better integration with OBiBa's Python-based tooling

### Critical Requirements

- **URL Preservation**: All existing URLs must continue to work (via redirects)
- **Complete Migration**: Big-bang approach, migrate entire site at once
- **GitHub Pages Deployment**: Continue hosting on GitHub Pages
- **Multi-Product Structure**: Maintain current organization (Opal, Mica, Agate, Rock, Amber, Onyx, DataSHIELD)
- **Blog-Style News**: Preserve date-based news and release announcements

### Success Criteria

- All existing URLs redirect correctly to new locations
- Site builds and deploys via GitHub Actions
- Local development workflow is functional
- Search functionality works across all content
- Mobile responsiveness improved
- Build times equal or better than current Jekyll setup

## Architecture Overview

### Technology Stack

**Core:**
- **MkDocs** (v1.5+) - Static site generator
- **Material for MkDocs** (v9.5+) - Theme and extensions
- **Python 3.11+** - Runtime environment

**Key Plugins:**
- `mkdocs-material` - Theme with extended features
- `mkdocs-material blog plugin` - Blog functionality for news/releases
- `mkdocs-redirects` - URL preservation
- `mkdocs-minify-plugin` - Build optimization
- `pymdown-extensions` - Enhanced Markdown features

**Deployment:**
- GitHub Actions - CI/CD pipeline
- GitHub Pages - Hosting

### Project Structure

```
obiba.github.io/
├── mkdocs.yml                 # Main configuration
├── requirements.txt           # Python dependencies
├── docs/                      # All content (Markdown)
│   ├── index.md              # Home page
│   ├── assets/               # Images, CSS, JS, fonts
│   │   ├── stylesheets/
│   │   │   └── extra.css
│   │   ├── javascripts/
│   │   │   └── extra.js
│   │   ├── images/
│   │   └── fonts/
│   ├── products/             # Product pages
│   │   ├── index.md
│   │   ├── opal/
│   │   │   ├── index.md
│   │   │   ├── features.md
│   │   │   └── ...
│   │   ├── mica/
│   │   │   └── index.md
│   │   ├── agate/
│   │   │   └── index.md
│   │   ├── rock/
│   │   │   └── index.md
│   │   ├── amber/
│   │   │   └── index.md
│   │   ├── onyx/
│   │   │   └── index.md
│   │   └── datashield/
│   │       └── index.md
│   ├── documentation/        # General documentation
│   │   └── index.md
│   ├── about/
│   │   └── index.md
│   ├── support/
│   │   └── index.md
│   ├── stories/
│   │   └── index.md
│   ├── publications/
│   │   └── index.md
│   └── blog/                 # News and releases
│       ├── index.md
│       ├── posts/
│       │   ├── 2024-05-06-opal-5.7.md
│       │   ├── 2024-03-15-mica-6.3.md
│       │   └── ...
│       └── .authors.yml
├── overrides/                # Theme customizations
│   ├── partials/
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── ...
│   └── assets/
│       └── stylesheets/
└── .github/
    └── workflows/
        └── deploy.yml        # GitHub Actions deployment
```

### Information Architecture

**Navigation Structure:**
```
Home
├── Products
│   ├── Products Overview
│   ├── Opal
│   ├── Mica
│   ├── Agate
│   ├── Rock
│   ├── Amber
│   ├── Onyx
│   └── DataSHIELD
├── Documentation
├── News (Blog)
├── Support
├── About
├── Publications
└── Stories
```

## Configuration Details

### MkDocs Configuration (mkdocs.yml)

```yaml
site_name: OBiBa
site_url: https://obiba.github.io
site_description: Open Source Software for BioBanks
site_author: OBiBa
repo_url: https://github.com/obiba
copyright: Copyright &copy; OBiBa

theme:
  name: material
  custom_dir: overrides
  logo: assets/images/logo.png
  favicon: assets/images/favicon.ico
  
  features:
    # Navigation
    - navigation.instant          # Fast SPA-like navigation
    - navigation.tracking         # URL updates with scroll position
    - navigation.tabs             # Top-level navigation tabs
    - navigation.tabs.sticky      # Sticky navigation tabs
    - navigation.sections         # Section grouping in sidebar
    - navigation.expand           # Auto-expand navigation
    - navigation.indexes          # Section index pages
    - navigation.top              # Back to top button
    
    # Table of Contents
    - toc.follow                  # TOC follows scroll
    - toc.integrate               # TOC integrated in nav (optional)
    
    # Search
    - search.suggest              # Search suggestions
    - search.highlight            # Highlight search terms
    - search.share                # Share search results
    
    # Content
    - content.tabs.link           # Linked content tabs
    - content.code.copy           # Copy code button
    - content.code.annotate       # Code annotations
    
  palette:
    # Light mode
    - scheme: default
      primary: custom              # Will use custom CSS for OBiBa colors
      accent: custom
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    
    # Dark mode
    - scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  
  font:
    text: Roboto
    code: Roboto Mono

plugins:
  - search:
      lang: en
      separator: '[\s\-,:!=\[\]()"/]+|(?!\b)(?=[A-Z][a-z])|\.(?!\d)|&[lg]t;'
  
  - blog:
      blog_dir: blog
      blog_toc: true
      post_date_format: medium
      post_url_date_format: yyyy/MM/dd
      post_url_format: "{date}/{slug}"
      post_slugify: !!python/object/apply:pymdownx.slugs.slugify
        kwds:
          case: lower
      post_slugify_separator: "-"
      categories_allowed:
        - releases
        - events
        - announcements
      authors_file: "{blog}/.authors.yml"
  
  - tags:
      tags_file: tags.md
  
  - redirects:
      redirect_maps:
        # Product pages
        'pages/products/opal/index.html': 'products/opal/index.md'
        'pages/products/mica/index.html': 'products/mica/index.md'
        'pages/products/agate/index.html': 'products/agate/index.md'
        'pages/products/rock/index.html': 'products/rock/index.md'
        'pages/products/amber/index.html': 'products/amber/index.md'
        'pages/products/onyx/index.html': 'products/onyx/index.md'
        'pages/products/datashield/index.html': 'products/datashield/index.md'
        # Static pages
        'pages/documentation/index.html': 'documentation/index.md'
        'pages/support/index.html': 'support/index.md'
        'pages/about/index.html': 'about/index.md'
        'pages/stories/index.html': 'stories/index.md'
        'pages/publications/index.html': 'publications/index.md'
        # News/release redirects will be auto-generated during migration
  
  - minify:
      minify_html: true
      minify_js: true
      minify_css: true

markdown_extensions:
  # Python Markdown extensions
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - tables
  - toc:
      permalink: true
      toc_depth: 3
  
  # PyMdown Extensions
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem:
      smart_enable: all
  - pymdownx.caret
  - pymdownx.details
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tilde

extra:
  analytics:
    provider: custom
    property: umami
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/obiba
      name: OBiBa on GitHub
  generator: false

extra_css:
  - assets/stylesheets/extra.css

extra_javascript:
  - assets/javascripts/extra.js

nav:
  - Home: index.md
  - Products:
    - products/index.md
    - Opal: products/opal/index.md
    - Mica: products/mica/index.md
    - Agate: products/agate/index.md
    - Rock: products/rock/index.md
    - Amber: products/amber/index.md
    - Onyx: products/onyx/index.md
    - DataSHIELD: products/datashield/index.md
  - Documentation: documentation/index.md
  - News: blog/index.md
  - Support: support/index.md
  - About: about/index.md
  - Publications: publications/index.md
  - Stories: stories/index.md
```

### Python Dependencies (requirements.txt)

```
mkdocs>=1.5.0
mkdocs-material>=9.5.0
mkdocs-material-extensions>=1.3
mkdocs-redirects>=1.2.0
mkdocs-minify-plugin>=0.8.0
pymdown-extensions>=10.7
pillow>=10.0.0
cairosvg>=2.7.0
```

## Content Migration Strategy

### HTML to Markdown Conversion

**Current State:** Jekyll uses HTML templates with Liquid includes
**Target State:** Markdown with MkDocs Material extensions

**Conversion Approach:**

1. **Product Pages**
   - Convert Jekyll section includes to Material tabs or admonitions
   - Transform feature lists to Markdown lists with Material card grids
   - Convert icon references to Material icons or custom CSS

2. **News/Blog Posts**
   - Extract content from Jekyll HTML structure
   - Add blog frontmatter (date, categories, authors)
   - Convert to clean Markdown

3. **Static Pages**
   - Convert HTML content to Markdown
   - Preserve semantic structure (headings, lists, links)
   - Use Material features for enhanced presentation

**Example Transformation:**

Jekyll HTML:
```html
---
layout: product
wiki: http://opaldoc.obiba.org
download: http://download.obiba.org/opal/stable/
github: http://github.com/obiba/opal
demo: https://opal-demo.obiba.org
title: Store with Opal
---
{% include JB/setup %}
{% include themes/bootstrap/section.html 
   icon="fa-info-circle" 
   sectionTitle="What is Opal?" 
   sectionBody="themes/bootstrap/opal/what.html" %}
```

MkDocs Markdown:
```markdown
---
title: Store with Opal
---

# Opal

<div class="product-links" markdown>
[:material-book: Documentation](http://opaldoc.obiba.org){ .md-button }
[:material-download: Download](http://download.obiba.org/opal/stable/){ .md-button }
[:material-github: GitHub](http://github.com/obiba/opal){ .md-button }
[:material-monitor: Demo](https://opal-demo.obiba.org){ .md-button }
</div>

## What is Opal?

[Content from what.html converted to Markdown]

## Features

!!! tip "Key Features"
    - Feature 1
    - Feature 2
```

### Migration Automation

A Python migration script (`migrate_jekyll_to_mkdocs.py`) will:

1. **Scan Jekyll structure** - Identify all pages, posts, includes, data files
2. **Parse frontmatter** - Extract Jekyll YAML configuration
3. **Convert HTML to Markdown** - Use html2text/markdownify libraries
4. **Transform includes** - Inline Jekyll includes as Markdown
5. **Generate blog posts** - Convert news items to blog post format
6. **Map URLs** - Create redirect configuration
7. **Copy assets** - Move images, CSS, JS to new structure
8. **Generate reports** - List manual review items

Script will handle:
- Frontmatter transformation
- Link rewriting (internal links to new paths)
- Asset path updates
- Jekyll Liquid syntax removal
- HTML to Markdown conversion
- Blog post metadata generation

### Manual Review Required

Items requiring manual review after automated migration:
- Complex HTML layouts that don't translate well to Markdown
- Custom JavaScript interactions
- Special styling or animations
- Data-driven content (from `_data/` files)
- Embedded external content

## URL Preservation & Redirects

### Redirect Mapping Strategy

**Critical:** All existing URLs must continue to work.

**Approach:**
1. Inventory all current URLs from sitemap and file structure
2. Map to corresponding new MkDocs URLs
3. Configure redirects in `mkdocs.yml` via redirects plugin
4. Generate meta refresh HTML for edge cases
5. Validate all redirects before deployment

**URL Pattern Mapping:**

| Jekyll Pattern | MkDocs Pattern | Example |
|---------------|----------------|---------|
| `/pages/products/{product}` | `/products/{product}/` | `/pages/products/opal` → `/products/opal/` |
| `/pages/news/release/{product}/{version}` | `/blog/{date}/{product}-{version}/` | `/pages/news/release/opal/5.7/` → `/blog/2024/05/06/opal-5.7/` |
| `/pages/news/event/{name}` | `/blog/{date}/{name}/` | `/pages/news/event/bbmri-lpc/` → `/blog/{date}/bbmri-lpc/` |
| `/pages/{section}` | `/{section}/` | `/pages/support` → `/support/` |

**Redirect Generation:**

Python script to generate redirect configuration:
```python
# Script will:
# 1. Walk Jekyll _site/ directory (or file structure)
# 2. Build URL map (old → new)
# 3. Output redirect_maps YAML
# 4. Create validation test suite
```

**Validation:**
- Automated testing of all redirect mappings
- HTTP status code checking (301/302 redirects)
- Link checker to verify no broken links
- Manual spot-checking of critical pages

## Deployment Pipeline

### GitHub Actions Workflow

**File:** `.github/workflows/deploy.yml`

```yaml
name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for blog dates
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
          
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
        
      - name: Build MkDocs site
        run: mkdocs build --strict
        
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./site
          
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

**Key Features:**
- **Build on PR**: Test builds on pull requests (doesn't deploy)
- **Deploy on merge**: Auto-deploy when merged to main
- **Dependency caching**: Faster builds via pip cache
- **Strict mode**: Fail build on warnings (catches broken links, etc.)
- **Full git history**: Required for accurate blog post dates

### Local Development

**Setup:**
```bash
# Clone repository
git clone https://github.com/obiba/obiba.github.io.git
cd obiba.github.io

# Install Python dependencies
pip install -r requirements.txt

# Serve locally with hot reload
mkdocs serve

# Site available at http://localhost:8000
# Auto-reloads on file changes
```

**Development Commands:**
```bash
# Build site (outputs to site/)
mkdocs build

# Build with strict mode (warnings as errors)
mkdocs build --strict

# Serve on different port
mkdocs serve --dev-addr localhost:8001

# Clean build
rm -rf site && mkdocs build
```

**Performance:**
- Hot reload typically < 1 second
- Full build expected ~10-30 seconds (depending on content size)
- Significantly faster than Jekyll (no Ruby overhead)

## Theme Customization

### Visual Design

**Design Goals:**
- Modern, clean aesthetic
- Improved readability and typography
- Better mobile experience
- Consistent with OBiBa branding
- Professional documentation feel

### Custom Styling

**File:** `docs/assets/stylesheets/extra.css`

Custom CSS for:
1. **Brand Colors** - OBiBa primary/accent colors
2. **Product Cards** - Grid layout for product showcase
3. **External Link Badges** - GitHub, download, demo, wiki icons
4. **Custom Components** - Any elements not covered by Material
5. **Typography Refinements** - Font sizes, spacing, hierarchy
6. **Footer Customization** - Partners, sponsors, contact

**Example Custom CSS:**
```css
:root {
  --md-primary-fg-color: #[OBiBa-primary];
  --md-accent-fg-color: #[OBiBa-accent];
}

/* Product card grid */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.product-card {
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 0.5rem;
  padding: 1.5rem;
  transition: box-shadow 0.3s;
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* External link buttons */
.product-links {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 1rem 0;
}
```

### Theme Overrides

**Directory:** `overrides/`

Custom HTML templates for:
- **Header** - Custom logo, navigation enhancements
- **Footer** - Partners, sponsors, custom links
- **Home page** - Custom landing page layout
- **Product pages** - Special product page template

**Example Override:**
`overrides/partials/footer.html` - Custom footer with sponsors/partners

### Icons and Assets

- **Material Icons** - Use Material's icon library where possible
- **Custom Icons** - Place in `docs/assets/images/icons/`
- **Logos** - Product logos in `docs/assets/images/logos/`
- **Fonts** - Custom fonts in `docs/assets/fonts/` if needed

## Data Migration

### Jekyll Data Files

Current `_data/` directory contains:
- `jobs.yml` - Job postings
- `news.yml` - News items
- `partners.yml` - Partner organizations
- `sponsors.yml` - Sponsors

**Migration Strategy:**

**Option 1: Convert to Markdown Pages**
- Each data category becomes a page
- Use Markdown tables or cards for listings
- Easier to edit, version control friendly

**Option 2: Keep as YAML + Custom Template**
- Keep YAML files
- Create custom Jinja2 templates in overrides/
- Read YAML and render dynamically

**Recommendation:** Option 1 (Markdown pages) for simplicity and maintainability

**Implementation:**
- `jobs.yml` → `docs/jobs/index.md` with job listings
- `partners.yml` → `docs/about/partners.md` with partner cards
- `sponsors.yml` → Integrated into footer or about page
- `news.yml` → Migrate to blog posts

## Testing & Validation

### Pre-Deployment Testing

1. **Build Validation**
   - `mkdocs build --strict` passes without errors
   - No broken internal links
   - All assets load correctly

2. **URL Redirect Testing**
   - Automated script to test all redirect mappings
   - HTTP status codes (301/302)
   - Verify final destination URLs

3. **Content Review**
   - Visual inspection of all major pages
   - Product pages render correctly
   - Blog posts display properly
   - Search functionality works

4. **Cross-Browser Testing**
   - Chrome, Firefox, Safari, Edge
   - Mobile browsers (iOS Safari, Chrome Mobile)

5. **Performance Testing**
   - Lighthouse scores (aim for 90+ across all metrics)
   - Page load times
   - Build times

### Post-Deployment Validation

1. **Live Site Verification**
   - All pages accessible
   - Redirects working
   - Search functional
   - Analytics tracking

2. **SEO Check**
   - Sitemap.xml generated
   - Robots.txt configured
   - Meta descriptions present
   - Canonical URLs correct

3. **Monitoring**
   - GitHub Actions build logs
   - Broken link monitoring
   - User feedback collection

## Migration Execution Plan

### Phase 1: Preparation (Week 1)

1. Set up Python environment and install dependencies
2. Create new branch for migration work
3. Initialize MkDocs project structure
4. Configure basic mkdocs.yml
5. Set up GitHub Actions workflow (test on branch)

### Phase 2: Content Migration (Week 2-3)

1. Develop and run automated migration script
2. Convert product pages to Markdown
3. Migrate news/blog posts
4. Convert static pages
5. Migrate assets (images, CSS, JS)
6. Manual review and cleanup

### Phase 3: Customization (Week 3-4)

1. Apply custom CSS for branding
2. Create theme overrides as needed
3. Implement custom components (product cards, etc.)
4. Configure blog categories and authors
5. Test navigation and search

### Phase 4: URL & Redirect Setup (Week 4)

1. Generate complete URL mapping
2. Configure redirects plugin
3. Test all redirect mappings
4. Create validation test suite
5. Document any URL changes

### Phase 5: Testing & QA (Week 5)

1. Build validation (strict mode)
2. Cross-browser testing
3. Mobile responsiveness check
4. Performance testing (Lighthouse)
5. Link checking
6. Search functionality testing
7. User acceptance testing

### Phase 6: Deployment (Week 6)

1. Final review and sign-off
2. Merge migration branch to main
3. Monitor GitHub Actions deployment
4. Verify live site
5. Update documentation (README, etc.)
6. Announce migration
7. Monitor for issues

### Rollback Plan

If critical issues arise post-deployment:

1. **Immediate rollback:** Revert main branch to previous commit
2. **GitHub Pages:** Previous version automatically deploys
3. **Investigation:** Debug issues in separate branch
4. **Redeployment:** Fix and redeploy when ready

Keep Jekyll branch as backup for 30 days post-migration.

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Broken URLs after migration | High | Medium | Comprehensive redirect testing, URL validation script |
| Content not converting cleanly | Medium | High | Manual review process, migration script with fallbacks |
| Visual design issues | Low | Medium | Browser testing, responsive design checks |
| Search not working properly | Medium | Low | Test search extensively, Material search is robust |
| Build pipeline failures | High | Low | Test GitHub Actions on branch first, monitor logs |
| Performance regression | Low | Low | Lighthouse testing, MkDocs typically faster than Jekyll |
| SEO impact from URL changes | Medium | Low | Proper redirects (301), preserve meta tags, sitemap |

## Success Metrics

### Technical Metrics

- Build time: ≤ 60 seconds (target: 30 seconds)
- Lighthouse Performance: ≥ 90
- Lighthouse Accessibility: ≥ 95
- All redirects return correct HTTP status codes
- Zero broken internal links
- Search latency: < 100ms

### User Experience Metrics

- Mobile usability score: Excellent (Google Search Console)
- Page load time: < 2 seconds (3G connection)
- Time to interactive: < 3 seconds
- Search result relevance: User feedback

### Maintenance Metrics

- Content update workflow: Simpler than Jekyll (subjective)
- Build success rate: > 99%
- Time to onboard new contributor: < 30 minutes

## Future Enhancements

Post-migration opportunities:

1. **Versioned Documentation** - Use mike plugin for per-product version docs
2. **API Documentation** - Integrate OpenAPI specs with MkDocs
3. **Interactive Examples** - Code playground integrations
4. **Improved Search** - Consider Algolia DocSearch for enhanced search
5. **Social Cards** - Auto-generate social media preview cards
6. **Internationalization** - Multi-language support if needed
7. **Dark Mode Enhancements** - Fine-tune dark mode styling
8. **Analytics Dashboard** - Better analytics integration (Umami, etc.)

## Conclusion

This migration from Jekyll to MkDocs Material will modernize the OBiBa website with better documentation features, simpler maintenance, and a more polished user experience. The phased approach with comprehensive testing ensures a smooth transition while preserving all existing URLs for SEO and user continuity.

The Python-based toolchain aligns better with OBiBa's technology stack and provides a more maintainable foundation for future enhancements.
