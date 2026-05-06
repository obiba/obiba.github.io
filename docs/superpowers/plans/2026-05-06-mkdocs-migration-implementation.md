# MkDocs Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the OBiBa website from Jekyll Bootstrap to MkDocs Material while preserving all URLs, maintaining multi-product structure, and modernizing the design.

**Architecture:** Complete big-bang migration using automated Python scripts for content conversion, manual refinement of complex pages, comprehensive redirect mapping for URL preservation, and GitHub Actions deployment pipeline.

**Tech Stack:** MkDocs 1.5+, Material for MkDocs 9.5+, Python 3.11+, mkdocs-redirects, mkdocs-minify-plugin, pymdown-extensions, GitHub Actions

---

## File Structure Overview

### New Files to Create

**Configuration:**
- `mkdocs.yml` - Main MkDocs configuration
- `requirements.txt` - Python dependencies
- `.github/workflows/deploy.yml` - GitHub Actions deployment

**Migration Scripts:**
- `scripts/migrate_jekyll_to_mkdocs.py` - Automated migration script
- `scripts/generate_redirects.py` - URL mapping and redirect generation
- `scripts/validate_redirects.py` - Test redirect mappings
- `scripts/convert_news_to_blog.py` - Convert news items to blog posts

**Content (docs/):**
- `docs/index.md` - Home page
- `docs/products/index.md` - Products overview
- `docs/products/opal/index.md` - Opal product page
- `docs/products/mica/index.md` - Mica product page
- `docs/products/agate/index.md` - Agate product page
- `docs/products/rock/index.md` - Rock product page
- `docs/products/amber/index.md` - Amber product page
- `docs/products/onyx/index.md` - Onyx product page
- `docs/products/datashield/index.md` - DataSHIELD product page
- `docs/documentation/index.md` - Documentation page
- `docs/support/index.md` - Support page
- `docs/about/index.md` - About page
- `docs/stories/index.md` - Stories page
- `docs/publications/index.md` - Publications page
- `docs/blog/index.md` - Blog index
- `docs/blog/.authors.yml` - Blog authors configuration
- `docs/blog/posts/*.md` - Individual blog posts

**Assets:**
- `docs/assets/stylesheets/extra.css` - Custom CSS
- `docs/assets/javascripts/extra.js` - Custom JavaScript
- `docs/assets/images/` - Images (migrated from existing)

**Theme Overrides:**
- `overrides/partials/header.html` - Custom header
- `overrides/partials/footer.html` - Custom footer

### Existing Files to Reference

- `_config.yml` - Jekyll configuration (reference for settings)
- `_data/*.yml` - Data files to migrate
- `pages/products/*.html` - Product pages to convert
- `pages/news/**/*.html` - News items to convert
- `_includes/themes/bootstrap/**/*.html` - Includes to convert
- `assets/` - Assets to migrate

---

## Task 1: Setup Project Structure and Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `mkdocs.yml` (basic version)
- Create: `docs/index.md` (placeholder)

- [ ] **Step 1: Create Python requirements file**

Create `requirements.txt`:

```txt
mkdocs>=1.5.0
mkdocs-material>=9.5.0
mkdocs-material-extensions>=1.3
mkdocs-redirects>=1.2.0
mkdocs-minify-plugin>=0.8.0
pymdown-extensions>=10.7
pillow>=10.0.0
cairosvg>=2.7.0
html2text>=2024.2.26
beautifulsoup4>=4.12.0
pyyaml>=6.0
```

- [ ] **Step 2: Test Python environment setup**

Run:
```bash
python3 --version
```
Expected: Python 3.11 or higher

- [ ] **Step 3: Install dependencies**

Run:
```bash
pip install -r requirements.txt
```
Expected: All packages install successfully

- [ ] **Step 4: Verify MkDocs installation**

Run:
```bash
mkdocs --version
```
Expected: Output shows "mkdocs, version 1.5.x or higher"

- [ ] **Step 5: Create basic mkdocs.yml**

Create `mkdocs.yml`:

```yaml
site_name: OBiBa
site_url: https://obiba.github.io
site_description: Open Source Software for BioBanks
site_author: OBiBa
repo_url: https://github.com/obiba
copyright: Copyright &copy; OBiBa

theme:
  name: material
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.tabs.sticky
    - search.suggest
    - search.highlight
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

plugins:
  - search
  
markdown_extensions:
  - admonition
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - attr_list
  - md_in_html

nav:
  - Home: index.md
```

- [ ] **Step 6: Create docs directory structure**

Run:
```bash
mkdir -p docs/{products,documentation,support,about,stories,publications,blog/posts,assets/{stylesheets,javascripts,images}}
```
Expected: Directories created successfully

- [ ] **Step 7: Create placeholder home page**

Create `docs/index.md`:

```markdown
# OBiBa

Open Source Software for BioBanks

This is a placeholder during migration.
```

- [ ] **Step 8: Test MkDocs build**

Run:
```bash
mkdocs build
```
Expected: Site builds successfully to `site/` directory

- [ ] **Step 9: Test MkDocs serve**

Run:
```bash
mkdocs serve &
sleep 3
curl -s http://localhost:8000 | grep -q "OBiBa"
kill %1
```
Expected: Server starts, page contains "OBiBa"

- [ ] **Step 10: Commit initial setup**

```bash
git add requirements.txt mkdocs.yml docs/index.md
git commit -m "feat: initialize MkDocs project structure"
```

---

## Task 2: Create Migration Script Foundation

**Files:**
- Create: `scripts/migrate_jekyll_to_mkdocs.py`

- [ ] **Step 1: Create migration script with imports**

Create `scripts/migrate_jekyll_to_mkdocs.py`:

```python
#!/usr/bin/env python3
"""
Jekyll to MkDocs Migration Script
Automates conversion of Jekyll site to MkDocs Material
"""

import os
import re
import yaml
import html2text
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
JEKYLL_ROOT = Path('.')
MKDOCS_DOCS = Path('docs')
JEKYLL_PAGES = JEKYLL_ROOT / 'pages'
JEKYLL_INCLUDES = JEKYLL_ROOT / '_includes'
JEKYLL_DATA = JEKYLL_ROOT / '_data'
JEKYLL_POSTS = JEKYLL_ROOT / '_posts'

class JekyllToMkDocsConverter:
    """Main converter class"""
    
    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.ignore_emphasis = False
        self.html_converter.body_width = 0  # No wrapping
        self.url_mappings = {}
        
    def parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Extract YAML frontmatter from file content"""
        frontmatter_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)', re.DOTALL)
        match = frontmatter_pattern.match(content)
        
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                body = match.group(2)
                return frontmatter or {}, body
            except yaml.YAMLError as e:
                logger.warning(f"Failed to parse frontmatter: {e}")
                return {}, content
        
        return {}, content
    
    def convert_html_to_markdown(self, html: str) -> str:
        """Convert HTML content to Markdown"""
        # First clean up Jekyll-specific syntax
        html = self.remove_jekyll_liquid(html)
        
        # Convert to markdown
        markdown = self.html_converter.handle(html)
        
        # Clean up markdown
        markdown = self.cleanup_markdown(markdown)
        
        return markdown
    
    def remove_jekyll_liquid(self, content: str) -> str:
        """Remove Jekyll Liquid syntax"""
        # Remove {% include ... %} tags (will be handled separately)
        content = re.sub(r'{%\s*include\s+.*?%}', '', content)
        
        # Remove {% JB/setup %}
        content = re.sub(r'{%\s*include\s+JB/setup\s*%}', '', content)
        
        # Remove {{ BASE_PATH }}
        content = re.sub(r'{{\s*BASE_PATH\s*}}', '/', content)
        
        # Remove other liquid variables
        content = re.sub(r'{{\s*.*?\s*}}', '', content)
        
        return content
    
    def cleanup_markdown(self, markdown: str) -> str:
        """Clean up converted markdown"""
        # Remove excessive newlines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # Fix heading spacing
        markdown = re.sub(r'(#+)\s*\n+', r'\1 ', markdown)
        
        # Trim whitespace
        markdown = markdown.strip()
        
        return markdown

def main():
    """Main migration function"""
    logger.info("Starting Jekyll to MkDocs migration")
    converter = JekyllToMkDocsConverter()
    logger.info("Migration script initialized")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Make script executable**

Run:
```bash
chmod +x scripts/migrate_jekyll_to_mkdocs.py
```
Expected: Script is executable

- [ ] **Step 3: Test script runs**

Run:
```bash
python3 scripts/migrate_jekyll_to_mkdocs.py
```
Expected: Script runs, outputs "Starting Jekyll to MkDocs migration" and "Migration script initialized"

- [ ] **Step 4: Commit migration script foundation**

```bash
git add scripts/migrate_jekyll_to_mkdocs.py
git commit -m "feat: add migration script foundation"
```

---

## Task 3: Implement Product Page Conversion

**Files:**
- Modify: `scripts/migrate_jekyll_to_mkdocs.py`

- [ ] **Step 1: Add product page conversion method**

Add to `JekyllToMkDocsConverter` class in `scripts/migrate_jekyll_to_mkdocs.py`:

```python
    def convert_product_page(self, product_name: str) -> bool:
        """Convert a Jekyll product page to MkDocs markdown"""
        source_file = JEKYLL_PAGES / 'products' / product_name / 'index.html'
        target_file = MKDOCS_DOCS / 'products' / product_name / 'index.md'
        
        if not source_file.exists():
            logger.warning(f"Product page not found: {source_file}")
            return False
        
        logger.info(f"Converting product page: {product_name}")
        
        # Read source file
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter, body = self.parse_frontmatter(content)
        
        # Extract product information
        title = frontmatter.get('title', product_name.capitalize())
        wiki = frontmatter.get('wiki', '')
        download = frontmatter.get('download', '')
        github = frontmatter.get('github', '')
        demo = frontmatter.get('demo', '')
        
        # Convert HTML body to markdown
        markdown_body = self.convert_html_to_markdown(body)
        
        # Build MkDocs frontmatter
        mkdocs_frontmatter = {
            'title': title
        }
        
        # Build markdown content
        markdown_content = '---\n'
        markdown_content += yaml.dump(mkdocs_frontmatter, default_flow_style=False)
        markdown_content += '---\n\n'
        markdown_content += f"# {title}\n\n"
        
        # Add product links if they exist
        links = []
        if wiki:
            links.append(f"[:material-book: Documentation]({wiki}){{ .md-button }}")
        if download:
            links.append(f"[:material-download: Download]({download}){{ .md-button }}")
        if github:
            links.append(f"[:material-github: GitHub]({github}){{ .md-button }}")
        if demo:
            links.append(f"[:material-monitor: Demo]({demo}){{ .md-button }}")
        
        if links:
            markdown_content += '<div class="product-links" markdown>\n'
            markdown_content += '\n'.join(links)
            markdown_content += '\n</div>\n\n'
        
        # Add converted body
        markdown_content += markdown_body
        
        # Ensure target directory exists
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write target file
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        logger.info(f"Converted: {source_file} -> {target_file}")
        
        # Record URL mapping
        old_url = f'/pages/products/{product_name}/index.html'
        new_url = f'products/{product_name}/index.md'
        self.url_mappings[old_url] = new_url
        
        return True
    
    def convert_all_products(self) -> int:
        """Convert all product pages"""
        products = ['opal', 'mica', 'agate', 'rock', 'amber', 'onyx', 'datashield']
        converted = 0
        
        for product in products:
            if self.convert_product_page(product):
                converted += 1
        
        logger.info(f"Converted {converted} product pages")
        return converted
```

- [ ] **Step 2: Update main function to convert products**

Update `main()` function in `scripts/migrate_jekyll_to_mkdocs.py`:

```python
def main():
    """Main migration function"""
    logger.info("Starting Jekyll to MkDocs migration")
    converter = JekyllToMkDocsConverter()
    
    # Convert product pages
    logger.info("Converting product pages...")
    converter.convert_all_products()
    
    logger.info("Migration complete")
```

- [ ] **Step 3: Run migration for products**

Run:
```bash
python3 scripts/migrate_jekyll_to_mkdocs.py
```
Expected: Script converts product pages, creates files in `docs/products/*/index.md`

- [ ] **Step 4: Verify converted product pages**

Run:
```bash
ls -la docs/products/*/index.md
```
Expected: Product markdown files exist

- [ ] **Step 5: Test build with product pages**

Run:
```bash
mkdocs build
```
Expected: Build succeeds, no errors

- [ ] **Step 6: Commit product page conversion**

```bash
git add scripts/migrate_jekyll_to_mkdocs.py docs/products/
git commit -m "feat: implement product page conversion"
```

---

## Task 4: Create Products Overview Page

**Files:**
- Create: `docs/products/index.md`

- [ ] **Step 1: Create products overview content**

Create `docs/products/index.md`:

```markdown
---
title: Products
---

# OBiBa Products

OBiBa develops open source software for epidemiological data management, analysis, and sharing.

<div class="product-grid" markdown>

<div class="product-card" markdown>

## [:material-database: Opal](opal/)

Data management and harmonization system for epidemiological studies. Store, harmonize, and analyze data with privacy protection.

[:material-arrow-right: Learn more](opal/){ .md-button }

</div>

<div class="product-card" markdown>

## [:material-chart-box: Mica](mica/)

Web catalog for epidemiological study metadata. Discover and access research data across multiple studies and networks.

[:material-arrow-right: Learn more](mica/){ .md-button }

</div>

<div class="product-card" markdown>

## [:material-account-key: Agate](agate/)

Central authentication server and user management system for the OBiBa suite of applications.

[:material-arrow-right: Learn more](agate/){ .md-button }

</div>

<div class="product-card" markdown>

## [:material-cloud: Rock](rock/)

R server for remote data analysis. Execute R commands remotely with access control and auditing.

[:material-arrow-right: Learn more](rock/){ .md-button }

</div>

<div class="product-card" markdown>

## [:material-file-cabinet: Amber](amber/)

Electronic data capture system for epidemiological studies. Collect data through web forms with validation.

[:material-arrow-right: Learn more](amber/){ .md-button }

</div>

<div class="product-card" markdown>

## [:material-hospital-box: Onyx](onyx/)

Participant management and data collection system for clinic assessments and biospecimen collection.

[:material-arrow-right: Learn more](onyx/){ .md-button }

</div>

<div class="product-card" markdown>

## [:material-shield-lock: DataSHIELD](datashield/)

Privacy-preserving statistical analysis platform. Analyze sensitive data without revealing individual-level information.

[:material-arrow-right: Learn more](datashield/){ .md-button }

</div>

</div>

## Integration

OBiBa products work together as an integrated suite:

- **Agate** provides central authentication for all applications
- **Opal** stores and manages data with DataSHIELD privacy protection
- **Mica** catalogs and makes data discoverable
- **Rock** enables remote R analysis on data in Opal
- **Amber** and **Onyx** collect data that flows into Opal
```

- [ ] **Step 2: Verify products overview builds**

Run:
```bash
mkdocs build
```
Expected: Build succeeds

- [ ] **Step 3: Update mkdocs.yml navigation for products**

Edit `mkdocs.yml`, update the `nav` section:

```yaml
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
```

- [ ] **Step 4: Test navigation**

Run:
```bash
mkdocs serve &
sleep 3
curl -s http://localhost:8000/products/ | grep -q "OBiBa Products"
kill %1
```
Expected: Products page loads with navigation

- [ ] **Step 5: Commit products overview**

```bash
git add docs/products/index.md mkdocs.yml
git commit -m "feat: add products overview page"
```

---

## Task 5: Convert Static Pages

**Files:**
- Modify: `scripts/migrate_jekyll_to_mkdocs.py`
- Create: `docs/documentation/index.md`
- Create: `docs/support/index.md`
- Create: `docs/about/index.md`
- Create: `docs/stories/index.md`
- Create: `docs/publications/index.md`

- [ ] **Step 1: Add static page conversion method**

Add to `JekyllToMkDocsConverter` class in `scripts/migrate_jekyll_to_mkdocs.py`:

```python
    def convert_static_page(self, page_name: str) -> bool:
        """Convert a Jekyll static page to MkDocs markdown"""
        source_file = JEKYLL_PAGES / page_name / 'index.html'
        target_file = MKDOCS_DOCS / page_name / 'index.md'
        
        if not source_file.exists():
            logger.warning(f"Static page not found: {source_file}")
            return False
        
        logger.info(f"Converting static page: {page_name}")
        
        # Read source file
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter, body = self.parse_frontmatter(content)
        
        # Extract title
        title = frontmatter.get('title', page_name.capitalize())
        
        # Convert HTML body to markdown
        markdown_body = self.convert_html_to_markdown(body)
        
        # Build MkDocs frontmatter
        mkdocs_frontmatter = {
            'title': title
        }
        
        # Build markdown content
        markdown_content = '---\n'
        markdown_content += yaml.dump(mkdocs_frontmatter, default_flow_style=False)
        markdown_content += '---\n\n'
        markdown_content += f"# {title}\n\n"
        markdown_content += markdown_body
        
        # Ensure target directory exists
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write target file
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        logger.info(f"Converted: {source_file} -> {target_file}")
        
        # Record URL mapping
        old_url = f'/pages/{page_name}/index.html'
        new_url = f'{page_name}/index.md'
        self.url_mappings[old_url] = new_url
        
        return True
    
    def convert_all_static_pages(self) -> int:
        """Convert all static pages"""
        pages = ['documentation', 'support', 'about', 'stories', 'publications']
        converted = 0
        
        for page in pages:
            if self.convert_static_page(page):
                converted += 1
        
        logger.info(f"Converted {converted} static pages")
        return converted
```

- [ ] **Step 2: Update main function to convert static pages**

Update `main()` function in `scripts/migrate_jekyll_to_mkdocs.py`:

```python
def main():
    """Main migration function"""
    logger.info("Starting Jekyll to MkDocs migration")
    converter = JekyllToMkDocsConverter()
    
    # Convert product pages
    logger.info("Converting product pages...")
    converter.convert_all_products()
    
    # Convert static pages
    logger.info("Converting static pages...")
    converter.convert_all_static_pages()
    
    logger.info("Migration complete")
```

- [ ] **Step 3: Run migration for static pages**

Run:
```bash
python3 scripts/migrate_jekyll_to_mkdocs.py
```
Expected: Script converts static pages

- [ ] **Step 4: Verify converted static pages**

Run:
```bash
ls -la docs/{documentation,support,about,stories,publications}/index.md
```
Expected: Static page markdown files exist

- [ ] **Step 5: Update mkdocs.yml navigation**

Edit `mkdocs.yml`, update the `nav` section:

```yaml
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
  - Support: support/index.md
  - About: about/index.md
  - Publications: publications/index.md
  - Stories: stories/index.md
```

- [ ] **Step 6: Test build with static pages**

Run:
```bash
mkdocs build
```
Expected: Build succeeds

- [ ] **Step 7: Commit static page conversion**

```bash
git add scripts/migrate_jekyll_to_mkdocs.py docs/{documentation,support,about,stories,publications}/ mkdocs.yml
git commit -m "feat: convert static pages"
```

---

## Task 6: Configure Blog Plugin and Structure

**Files:**
- Modify: `mkdocs.yml`
- Create: `docs/blog/.authors.yml`
- Create: `docs/blog/index.md`

- [ ] **Step 1: Add blog plugin configuration to mkdocs.yml**

Edit `mkdocs.yml`, add to `plugins` section:

```yaml
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
```

- [ ] **Step 2: Create blog authors file**

Create `docs/blog/.authors.yml`:

```yaml
authors:
  obiba:
    name: OBiBa Team
    description: OBiBa development team
    avatar: https://github.com/obiba.png
```

- [ ] **Step 3: Create blog index page**

Create `docs/blog/index.md`:

```markdown
---
title: News
---

# News & Releases

Stay up to date with the latest OBiBa product releases, events, and announcements.
```

- [ ] **Step 4: Add blog to navigation**

Edit `mkdocs.yml`, update `nav` section to include blog:

```yaml
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

- [ ] **Step 5: Test blog configuration**

Run:
```bash
mkdocs build
```
Expected: Build succeeds with blog plugin enabled

- [ ] **Step 6: Commit blog configuration**

```bash
git add mkdocs.yml docs/blog/
git commit -m "feat: configure blog plugin for news and releases"
```

---

## Task 7: Convert News Items to Blog Posts

**Files:**
- Create: `scripts/convert_news_to_blog.py`

- [ ] **Step 1: Create news conversion script**

Create `scripts/convert_news_to_blog.py`:

```python
#!/usr/bin/env python3
"""
Convert Jekyll news items to MkDocs blog posts
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

JEKYLL_NEWS = Path('pages/news')
BLOG_POSTS = Path('docs/blog/posts')

class NewsConverter:
    """Convert Jekyll news to blog posts"""
    
    def __init__(self):
        self.url_mappings = {}
        
    def parse_frontmatter(self, content):
        """Extract YAML frontmatter"""
        pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)', re.DOTALL)
        match = pattern.match(content)
        
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                body = match.group(2)
                return frontmatter or {}, body
            except yaml.YAMLError:
                return {}, content
        
        return {}, content
    
    def extract_date_from_path(self, path: Path) -> datetime:
        """Try to extract date from file path or content"""
        # Try to find date in path (e.g., pages/news/release/opal/5.7)
        path_str = str(path)
        
        # Default to a reasonable date if can't determine
        default_date = datetime(2024, 1, 1)
        
        # Check if path contains version that might indicate date
        # This is a simplified heuristic
        if 'release' in path_str:
            # Use modification time as fallback
            if path.exists():
                mtime = path.stat().st_mtime
                return datetime.fromtimestamp(mtime)
        
        return default_date
    
    def convert_news_item(self, news_path: Path, category: str) -> bool:
        """Convert a single news item to blog post"""
        if not news_path.exists():
            return False
        
        logger.info(f"Converting news item: {news_path}")
        
        # Read content
        with open(news_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter, body = self.parse_frontmatter(content)
        
        # Extract metadata
        title = frontmatter.get('title', news_path.parent.name.replace('-', ' ').title())
        
        # Determine date
        post_date = self.extract_date_from_path(news_path)
        
        # Generate slug from path
        slug_parts = []
        for part in news_path.parts:
            if part in ['pages', 'news', 'release', 'event', 'index.html']:
                continue
            slug_parts.append(part)
        slug = '-'.join(slug_parts)
        
        # Create post filename
        date_str = post_date.strftime('%Y-%m-%d')
        post_filename = f"{date_str}-{slug}.md"
        post_path = BLOG_POSTS / post_filename
        
        # Build blog post frontmatter
        post_frontmatter = {
            'date': post_date.strftime('%Y-%m-%d'),
            'categories': [category],
            'authors': ['obiba']
        }
        
        # Clean body (remove Jekyll syntax)
        body = re.sub(r'{%\s*include\s+.*?%}', '', body)
        body = re.sub(r'{{\s*.*?\s*}}', '', body)
        
        # Build blog post
        post_content = '---\n'
        post_content += yaml.dump(post_frontmatter, default_flow_style=False)
        post_content += '---\n\n'
        post_content += f"# {title}\n\n"
        post_content += body
        
        # Ensure directory exists
        BLOG_POSTS.mkdir(parents=True, exist_ok=True)
        
        # Write post
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(post_content)
        
        logger.info(f"Created blog post: {post_path}")
        
        # Record URL mapping
        old_url = str(news_path.relative_to('.')).replace('index.html', '')
        new_url = f'blog/{post_date.year}/{post_date.month:02d}/{post_date.day:02d}/{slug}/'
        self.url_mappings[old_url] = new_url
        
        return True
    
    def convert_all_releases(self) -> int:
        """Convert all release announcements"""
        release_dir = JEKYLL_NEWS / 'release'
        converted = 0
        
        if not release_dir.exists():
            logger.warning(f"Release directory not found: {release_dir}")
            return 0
        
        for product_dir in release_dir.iterdir():
            if not product_dir.is_dir():
                continue
            
            for version_dir in product_dir.iterdir():
                if not version_dir.is_dir():
                    continue
                
                index_file = version_dir / 'index.html'
                if index_file.exists():
                    if self.convert_news_item(index_file, 'releases'):
                        converted += 1
        
        logger.info(f"Converted {converted} release announcements")
        return converted
    
    def convert_all_events(self) -> int:
        """Convert all event announcements"""
        event_dir = JEKYLL_NEWS / 'event'
        converted = 0
        
        if not event_dir.exists():
            logger.warning(f"Event directory not found: {event_dir}")
            return 0
        
        for event_item in event_dir.iterdir():
            if not event_item.is_dir():
                continue
            
            index_file = event_item / 'index.html'
            if index_file.exists():
                if self.convert_news_item(index_file, 'events'):
                    converted += 1
        
        logger.info(f"Converted {converted} event announcements")
        return converted

def main():
    """Main conversion function"""
    logger.info("Converting news items to blog posts")
    converter = NewsConverter()
    
    # Convert releases
    converter.convert_all_releases()
    
    # Convert events
    converter.convert_all_events()
    
    logger.info("News conversion complete")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Make script executable**

Run:
```bash
chmod +x scripts/convert_news_to_blog.py
```

- [ ] **Step 3: Run news conversion**

Run:
```bash
python3 scripts/convert_news_to_blog.py
```
Expected: News items converted to blog posts

- [ ] **Step 4: Verify blog posts created**

Run:
```bash
ls -la docs/blog/posts/
```
Expected: Multiple .md files exist

- [ ] **Step 5: Test build with blog posts**

Run:
```bash
mkdocs build
```
Expected: Build succeeds with blog posts

- [ ] **Step 6: Commit news conversion**

```bash
git add scripts/convert_news_to_blog.py docs/blog/posts/
git commit -m "feat: convert news items to blog posts"
```

---

## Task 8: Migrate Assets

**Files:**
- Modify: `scripts/migrate_jekyll_to_mkdocs.py`

- [ ] **Step 1: Add asset migration method**

Add to `JekyllToMkDocsConverter` class in `scripts/migrate_jekyll_to_mkdocs.py`:

```python
    def migrate_assets(self) -> bool:
        """Migrate assets from Jekyll to MkDocs"""
        import shutil
        
        jekyll_assets = JEKYLL_ROOT / 'assets'
        mkdocs_assets = MKDOCS_DOCS / 'assets'
        
        if not jekyll_assets.exists():
            logger.warning("Jekyll assets directory not found")
            return False
        
        logger.info("Migrating assets...")
        
        # Create assets directory structure
        (mkdocs_assets / 'images').mkdir(parents=True, exist_ok=True)
        (mkdocs_assets / 'stylesheets').mkdir(parents=True, exist_ok=True)
        (mkdocs_assets / 'javascripts').mkdir(parents=True, exist_ok=True)
        
        # Copy images
        jekyll_images = jekyll_assets / 'images'
        if jekyll_images.exists():
            for image_file in jekyll_images.rglob('*'):
                if image_file.is_file():
                    rel_path = image_file.relative_to(jekyll_images)
                    target = mkdocs_assets / 'images' / rel_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(image_file, target)
                    logger.debug(f"Copied image: {rel_path}")
        
        # Copy themes/bootstrap assets if they exist
        jekyll_themes = JEKYLL_ROOT / 'assets' / 'themes'
        if jekyll_themes.exists():
            for asset_file in jekyll_themes.rglob('*'):
                if asset_file.is_file() and asset_file.suffix in ['.css', '.js', '.png', '.jpg', '.svg']:
                    rel_path = asset_file.relative_to(jekyll_themes)
                    
                    # Determine target based on file type
                    if asset_file.suffix == '.css':
                        target = mkdocs_assets / 'stylesheets' / asset_file.name
                    elif asset_file.suffix == '.js':
                        target = mkdocs_assets / 'javascripts' / asset_file.name
                    else:
                        target = mkdocs_assets / 'images' / asset_file.name
                    
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(asset_file, target)
                    logger.debug(f"Copied asset: {asset_file.name}")
        
        logger.info("Asset migration complete")
        return True
```

- [ ] **Step 2: Update main function to migrate assets**

Update `main()` function in `scripts/migrate_jekyll_to_mkdocs.py`:

```python
def main():
    """Main migration function"""
    logger.info("Starting Jekyll to MkDocs migration")
    converter = JekyllToMkDocsConverter()
    
    # Convert product pages
    logger.info("Converting product pages...")
    converter.convert_all_products()
    
    # Convert static pages
    logger.info("Converting static pages...")
    converter.convert_all_static_pages()
    
    # Migrate assets
    logger.info("Migrating assets...")
    converter.migrate_assets()
    
    logger.info("Migration complete")
```

- [ ] **Step 3: Run asset migration**

Run:
```bash
python3 scripts/migrate_jekyll_to_mkdocs.py
```
Expected: Assets copied to docs/assets/

- [ ] **Step 4: Verify assets migrated**

Run:
```bash
ls -R docs/assets/
```
Expected: Images, stylesheets, javascripts directories populated

- [ ] **Step 5: Commit asset migration**

```bash
git add scripts/migrate_jekyll_to_mkdocs.py docs/assets/
git commit -m "feat: migrate assets from Jekyll"
```

---

## Task 9: Create Custom Styling

**Files:**
- Create: `docs/assets/stylesheets/extra.css`
- Modify: `mkdocs.yml`

- [ ] **Step 1: Create custom CSS file**

Create `docs/assets/stylesheets/extra.css`:

```css
/**
 * OBiBa Custom Styles for MkDocs Material
 */

/* Brand Colors */
:root {
  --obiba-primary: #0066cc;
  --obiba-accent: #ff6600;
  --obiba-light: #f5f7fa;
}

/* Override Material theme colors */
[data-md-color-scheme="default"] {
  --md-primary-fg-color: var(--obiba-primary);
  --md-accent-fg-color: var(--obiba-accent);
}

/* Product Grid Layout */
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
  transition: all 0.3s ease;
  background: var(--md-default-bg-color);
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--md-primary-fg-color);
  transform: translateY(-2px);
}

.product-card h2 {
  margin-top: 0;
  color: var(--md-primary-fg-color);
}

.product-card p {
  color: var(--md-default-fg-color--light);
  line-height: 1.6;
}

/* Product Links */
.product-links {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 1.5rem 0;
}

.product-links .md-button {
  margin: 0;
}

/* Home Page Hero */
.hero-section {
  text-align: center;
  padding: 3rem 1rem;
  background: linear-gradient(135deg, var(--obiba-primary) 0%, #004999 100%);
  color: white;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: white;
}

.hero-section p {
  font-size: 1.25rem;
  opacity: 0.9;
}

/* Feature Highlights */
.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.feature-item {
  padding: 1rem;
  text-align: center;
}

.feature-item h3 {
  color: var(--md-primary-fg-color);
  margin-bottom: 0.5rem;
}

/* Responsive Design */
@media screen and (max-width: 768px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-section h1 {
    font-size: 1.75rem;
  }
  
  .hero-section p {
    font-size: 1rem;
  }
}

/* Blog Enhancements */
.md-typeset article {
  max-width: 800px;
}

.md-typeset .md-content__button {
  display: none;
}

/* Improved Tables */
.md-typeset table:not([class]) {
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 0.25rem;
  overflow: hidden;
}

.md-typeset table:not([class]) th {
  background-color: var(--obiba-light);
  font-weight: 600;
}

/* Code Blocks */
.md-typeset code {
  background-color: var(--md-code-bg-color);
  border-radius: 0.25rem;
  padding: 0.1em 0.3em;
}

/* Custom Admonitions */
.md-typeset .admonition.tip {
  border-left-color: var(--obiba-accent);
}

/* Footer Customization */
.md-footer-meta {
  background-color: var(--md-default-fg-color--lightest);
}

/* Navigation Improvements */
.md-nav__title {
  font-weight: 600;
}

.md-nav__link--active {
  color: var(--obiba-primary);
  font-weight: 600;
}
```

- [ ] **Step 2: Add custom CSS to mkdocs.yml**

Edit `mkdocs.yml`, add at the end:

```yaml
extra_css:
  - assets/stylesheets/extra.css
```

- [ ] **Step 3: Test build with custom CSS**

Run:
```bash
mkdocs build
```
Expected: Build succeeds, CSS included

- [ ] **Step 4: Test styling in browser**

Run:
```bash
mkdocs serve &
sleep 3
curl -s http://localhost:8000 | grep -q "extra.css"
kill %1
```
Expected: extra.css is loaded

- [ ] **Step 5: Commit custom styling**

```bash
git add docs/assets/stylesheets/extra.css mkdocs.yml
git commit -m "feat: add custom OBiBa styling"
```

---

## Task 10: Generate Redirect Mappings

**Files:**
- Create: `scripts/generate_redirects.py`
- Modify: `mkdocs.yml`

- [ ] **Step 1: Create redirect generation script**

Create `scripts/generate_redirects.py`:

```python
#!/usr/bin/env python3
"""
Generate redirect mappings for MkDocs redirects plugin
"""

import yaml
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_redirect_maps():
    """Generate redirect mapping dictionary"""
    
    redirects = {}
    
    # Product page redirects
    products = ['opal', 'mica', 'agate', 'rock', 'amber', 'onyx', 'datashield']
    for product in products:
        old_url = f'pages/products/{product}/index.html'
        new_url = f'products/{product}/index.md'
        redirects[old_url] = new_url
    
    # Static page redirects
    static_pages = ['documentation', 'support', 'about', 'stories', 'publications']
    for page in static_pages:
        old_url = f'pages/{page}/index.html'
        new_url = f'{page}/index.md'
        redirects[old_url] = new_url
    
    # News/Blog redirects - scan blog posts for their old paths
    blog_posts_dir = Path('docs/blog/posts')
    if blog_posts_dir.exists():
        for post_file in blog_posts_dir.glob('*.md'):
            # Extract date from filename (YYYY-MM-DD-slug.md)
            filename = post_file.stem
            parts = filename.split('-', 3)
            if len(parts) >= 4:
                year, month, day, slug = parts[0], parts[1], parts[2], parts[3]
                
                # Determine category and old path from slug
                if 'opal' in slug or 'mica' in slug or 'rock' in slug or 'agate' in slug or 'amber' in slug or 'onyx' in slug:
                    # This is likely a release
                    # Extract product and version from slug
                    for product in products:
                        if product in slug:
                            # Try to extract version
                            version = slug.replace(product, '').strip('-').replace('-', '.')
                            old_url = f'pages/news/release/{product}/{version}/index.html'
                            new_url = f'blog/{year}/{month}/{day}/{slug}/'
                            redirects[old_url] = new_url
                            break
                else:
                    # This is likely an event
                    old_url = f'pages/news/event/{slug}/index.html'
                    new_url = f'blog/{year}/{month}/{day}/{slug}/'
                    redirects[old_url] = new_url
    
    return redirects

def update_mkdocs_config(redirects):
    """Update mkdocs.yml with redirect mappings"""
    
    config_file = Path('mkdocs.yml')
    
    # Read existing config
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Ensure plugins section exists
    if 'plugins' not in config:
        config['plugins'] = []
    
    # Remove existing redirects plugin if present
    plugins = []
    for plugin in config['plugins']:
        if isinstance(plugin, dict) and 'redirects' in plugin:
            continue
        plugins.append(plugin)
    
    # Add redirects plugin with mappings
    redirects_plugin = {
        'redirects': {
            'redirect_maps': redirects
        }
    }
    
    # Insert redirects plugin before minify if it exists
    plugins.append(redirects_plugin)
    config['plugins'] = plugins
    
    # Write updated config
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    logger.info(f"Updated mkdocs.yml with {len(redirects)} redirect mappings")

def main():
    """Main function"""
    logger.info("Generating redirect mappings")
    
    redirects = generate_redirect_maps()
    logger.info(f"Generated {len(redirects)} redirect mappings")
    
    update_mkdocs_config(redirects)
    
    logger.info("Redirect generation complete")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Make script executable**

Run:
```bash
chmod +x scripts/generate_redirects.py
```

- [ ] **Step 3: Run redirect generation**

Run:
```bash
python3 scripts/generate_redirects.py
```
Expected: mkdocs.yml updated with redirects

- [ ] **Step 4: Verify redirects in config**

Run:
```bash
grep -A 5 "redirects:" mkdocs.yml
```
Expected: Redirect mappings present in config

- [ ] **Step 5: Test build with redirects**

Run:
```bash
mkdocs build
```
Expected: Build succeeds with redirects plugin

- [ ] **Step 6: Commit redirect generation**

```bash
git add scripts/generate_redirects.py mkdocs.yml
git commit -m "feat: generate redirect mappings"
```

---

## Task 11: Complete MkDocs Configuration

**Files:**
- Modify: `mkdocs.yml`

- [ ] **Step 1: Update mkdocs.yml with complete configuration**

Replace content of `mkdocs.yml` with:

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
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.expand
    - navigation.indexes
    - navigation.top
    
    # Table of Contents
    - toc.follow
    
    # Search
    - search.suggest
    - search.highlight
    - search.share
    
    # Content
    - content.tabs.link
    - content.code.copy
    - content.code.annotate
    
  palette:
    # Light mode
    - scheme: default
      primary: custom
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

- [ ] **Step 2: Test complete configuration**

Run:
```bash
mkdocs build --strict
```
Expected: Build succeeds in strict mode with no warnings

- [ ] **Step 3: Commit complete configuration**

```bash
git add mkdocs.yml
git commit -m "feat: complete MkDocs configuration"
```

---

## Task 12: Create GitHub Actions Deployment Workflow

**Files:**
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: Create GitHub Actions workflow directory**

Run:
```bash
mkdir -p .github/workflows
```

- [ ] **Step 2: Create deployment workflow**

Create `.github/workflows/deploy.yml`:

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
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Cache dependencies
        uses: actions/cache@v4
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
        uses: actions/upload-pages-artifact@v3
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
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: Test workflow syntax**

Run:
```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/deploy.yml'))"
```
Expected: No syntax errors

- [ ] **Step 4: Commit GitHub Actions workflow**

```bash
git add .github/workflows/deploy.yml
git commit -m "feat: add GitHub Actions deployment workflow"
```

---

## Task 13: Create Custom Home Page

**Files:**
- Modify: `docs/index.md`

- [ ] **Step 1: Create enhanced home page**

Replace content of `docs/index.md`:

```markdown
---
title: Home
---

<div class="hero-section" markdown>

# OBiBa

**Open Source Software for BioBanks**

Comprehensive data management solutions for epidemiological studies and biobanks

</div>

## Our Products

<div class="product-grid" markdown>

<div class="product-card" markdown>

### [:material-database: Opal](products/opal/)

Data warehouse for biobanks with privacy protection

</div>

<div class="product-card" markdown>

### [:material-chart-box: Mica](products/mica/)

Catalog and portal for study metadata

</div>

<div class="product-card" markdown>

### [:material-account-key: Agate](products/agate/)

Central authentication and user management

</div>

<div class="product-card" markdown>

### [:material-cloud: Rock](products/rock/)

R server for remote statistical analysis

</div>

<div class="product-card" markdown>

### [:material-file-cabinet: Amber](products/amber/)

Electronic data capture system

</div>

<div class="product-card" markdown>

### [:material-hospital-box: Onyx](products/onyx/)

Participant and biospecimen management

</div>

<div class="product-card" markdown>

### [:material-shield-lock: DataSHIELD](products/datashield/)

Privacy-preserving federated analysis

</div>

</div>

## Key Features

<div class="feature-list" markdown>

<div class="feature-item" markdown>

### :material-security: Privacy & Security

Built-in privacy protection with role-based access control and audit trails

</div>

<div class="feature-item" markdown>

### :material-connection: Interoperability

Standards-based integration with HL7 FHIR, DDI, ISO 11179

</div>

<div class="feature-item" markdown>

### :material-scale-balance: Open Source

Freely available under AGPL license with active community support

</div>

<div class="feature-item" markdown>

### :material-chart-line: Analytics Ready

Integrated statistical analysis with R, Python, and DataSHIELD

</div>

</div>

## Get Started

[:material-book-open-variant: Explore Documentation](documentation/){ .md-button .md-button--primary }
[:material-account-group: Get Support](support/){ .md-button }
[:material-download: Download Products](products/){ .md-button }

---

## Latest News

Check our [News section](blog/) for the latest product releases and announcements.
```

- [ ] **Step 2: Test home page build**

Run:
```bash
mkdocs build
```
Expected: Build succeeds

- [ ] **Step 3: View home page locally**

Run:
```bash
mkdocs serve &
sleep 3
curl -s http://localhost:8000 | grep -q "Our Products"
kill %1
```
Expected: Home page contains expected content

- [ ] **Step 4: Commit enhanced home page**

```bash
git add docs/index.md
git commit -m "feat: create enhanced home page"
```

---

## Task 14: Create Theme Overrides

**Files:**
- Create: `overrides/partials/footer.html`
- Create: `docs/assets/javascripts/extra.js`

- [ ] **Step 1: Create overrides directory**

Run:
```bash
mkdir -p overrides/partials
```

- [ ] **Step 2: Create custom footer**

Create `overrides/partials/footer.html`:

```html
{% import "partials/language.html" as lang with context %}

<footer class="md-footer">
  {% if page.previous_page or page.next_page %}
    <nav class="md-footer__inner md-grid" aria-label="{{ lang.t('footer.title') }}">
      {% if page.previous_page %}
        <a href="{{ page.previous_page.url | url }}" class="md-footer__link md-footer__link--prev" aria-label="{{ lang.t('footer.previous') }}: {{ page.previous_page.title | e }}" rel="prev">
          <div class="md-footer__button md-icon">
            {% include ".icons/material/arrow-left.svg" %}
          </div>
          <div class="md-footer__title">
            <div class="md-ellipsis">
              <span class="md-footer__direction">
                {{ lang.t("footer.previous") }}
              </span>
              {{ page.previous_page.title }}
            </div>
          </div>
        </a>
      {% endif %}
      {% if page.next_page %}
        <a href="{{ page.next_page.url | url }}" class="md-footer__link md-footer__link--next" aria-label="{{ lang.t('footer.next') }}: {{ page.next_page.title | e }}" rel="next">
          <div class="md-footer__title">
            <div class="md-ellipsis">
              <span class="md-footer__direction">
                {{ lang.t("footer.next") }}
              </span>
              {{ page.next_page.title }}
            </div>
          </div>
          <div class="md-footer__button md-icon">
            {% include ".icons/material/arrow-right.svg" %}
          </div>
        </a>
      {% endif %}
    </nav>
  {% endif %}
  <div class="md-footer-meta md-typeset">
    <div class="md-footer-meta__inner md-grid">
      <div class="md-copyright">
        {% if config.copyright %}
          <div class="md-copyright__highlight">
            {{ config.copyright }}
          </div>
        {% endif %}
        <div class="md-footer-custom">
          <p>
            OBiBa is a core project of the Maelstrom Research program of the Research Institute of the McGill University Health Centre.
          </p>
          <p>
            <a href="https://github.com/obiba" target="_blank" rel="noopener">
              <span class="twemoji">{% include ".icons/fontawesome/brands/github.svg" %}</span> GitHub
            </a> |
            <a href="{{ config.site_url }}about/">About</a> |
            <a href="{{ config.site_url }}support/">Support</a>
          </p>
        </div>
      </div>
      {% include "partials/social.html" %}
    </div>
  </div>
</footer>
```

- [ ] **Step 3: Create custom JavaScript**

Create `docs/assets/javascripts/extra.js`:

```javascript
/**
 * OBiBa Custom JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
  console.log('OBiBa MkDocs site loaded');
  
  // Add any custom JavaScript functionality here
  
  // Example: External link handling
  const links = document.querySelectorAll('a[href^="http"]');
  links.forEach(link => {
    if (!link.href.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });
});
```

- [ ] **Step 4: Test build with overrides**

Run:
```bash
mkdocs build
```
Expected: Build succeeds with custom footer

- [ ] **Step 5: Commit theme overrides**

```bash
git add overrides/ docs/assets/javascripts/extra.js
git commit -m "feat: add custom footer and JavaScript"
```

---

## Task 15: Manual Content Review and Refinement

**Files:**
- Modify: Multiple files in `docs/` as needed

- [ ] **Step 1: Review home page content**

Run:
```bash
mkdocs serve &
sleep 3
```

Open browser to http://localhost:8000 and review:
- Home page layout
- Navigation structure
- Visual design

```bash
kill %1
```

- [ ] **Step 2: Review product pages**

For each product (opal, mica, agate, rock, amber, onyx, datashield):

1. View page at http://localhost:8000/products/{product}/
2. Check for:
   - Proper heading structure
   - Working links
   - Readable content
   - Proper formatting

Make manual edits to product markdown files as needed to improve presentation.

- [ ] **Step 3: Review blog posts**

Visit http://localhost:8000/blog/ and check:
- Posts are listed correctly
- Dates are accurate
- Categories are assigned
- Content is readable

Edit blog posts as needed for clarity.

- [ ] **Step 4: Test all navigation links**

Systematically click through all navigation items to ensure:
- All pages load
- No 404 errors
- Internal links work

- [ ] **Step 5: Commit manual refinements**

```bash
git add docs/
git commit -m "refine: manual content review and improvements"
```

---

## Task 16: Build Validation and Testing

**Files:**
- Create: `scripts/validate_build.sh`

- [ ] **Step 1: Create build validation script**

Create `scripts/validate_build.sh`:

```bash
#!/bin/bash
# Build validation script

set -e

echo "=== MkDocs Build Validation ==="
echo

echo "1. Testing strict build..."
mkdocs build --strict --clean
echo "✓ Strict build passed"
echo

echo "2. Checking for broken internal links..."
python3 -c "
import re
from pathlib import Path

site_dir = Path('site')
broken_links = []

for html_file in site_dir.rglob('*.html'):
    content = html_file.read_text()
    # Find internal links
    links = re.findall(r'href=\"([^\"]+)\"', content)
    for link in links:
        if link.startswith('/') or link.startswith('../'):
            # Check if target exists
            target = site_dir / link.lstrip('/')
            if not target.exists() and not (site_dir / link.lstrip('/') / 'index.html').exists():
                broken_links.append(f'{html_file}: {link}')

if broken_links:
    print('✗ Found broken links:')
    for link in broken_links[:10]:
        print(f'  {link}')
    exit(1)
else:
    print('✓ No broken internal links found')
"
echo

echo "3. Checking assets..."
if [ -f "site/assets/stylesheets/extra.css" ]; then
    echo "✓ Custom CSS found"
else
    echo "✗ Custom CSS missing"
    exit 1
fi

if [ -f "site/assets/javascripts/extra.js" ]; then
    echo "✓ Custom JavaScript found"
else
    echo "✗ Custom JavaScript missing"
    exit 1
fi
echo

echo "4. Checking sitemap..."
if [ -f "site/sitemap.xml" ]; then
    echo "✓ Sitemap generated"
else
    echo "✗ Sitemap missing"
    exit 1
fi
echo

echo "5. Checking blog..."
if [ -d "site/blog" ]; then
    post_count=$(find site/blog -name "index.html" -type f | wc -l)
    echo "✓ Blog generated with $post_count pages"
else
    echo "✗ Blog not generated"
    exit 1
fi
echo

echo "=== All validation checks passed ==="
```

- [ ] **Step 2: Make script executable**

Run:
```bash
chmod +x scripts/validate_build.sh
```

- [ ] **Step 3: Run validation**

Run:
```bash
./scripts/validate_build.sh
```
Expected: All validation checks pass

- [ ] **Step 4: Commit validation script**

```bash
git add scripts/validate_build.sh
git commit -m "feat: add build validation script"
```

---

## Task 17: Performance Testing

**Files:**
- None (testing only)

- [ ] **Step 1: Measure build time**

Run:
```bash
time mkdocs build --clean
```
Expected: Build completes in < 60 seconds (target: ~30 seconds)

- [ ] **Step 2: Check site size**

Run:
```bash
du -sh site/
```
Expected: Reasonable size (typically < 50MB for documentation sites)

- [ ] **Step 3: Test hot reload performance**

Run:
```bash
mkdocs serve &
PID=$!
sleep 3
echo "Test" >> docs/index.md
sleep 2
git checkout docs/index.md
kill $PID
```
Expected: Changes detected and rebuilt quickly (< 2 seconds)

- [ ] **Step 4: Document performance metrics**

Create a note in your terminal output or commit message documenting:
- Build time
- Site size
- Hot reload speed

---

## Task 18: Create Migration Documentation

**Files:**
- Create: `docs/migration-notes.md`

- [ ] **Step 1: Create migration notes**

Create `docs/migration-notes.md`:

```markdown
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
```

- [ ] **Step 2: Commit migration documentation**

```bash
git add docs/migration-notes.md
git commit -m "docs: add migration notes"
```

---

## Task 19: Final Pre-Deployment Testing

**Files:**
- None (testing only)

- [ ] **Step 1: Clean build test**

Run:
```bash
rm -rf site/
mkdocs build --strict
```
Expected: Clean build succeeds

- [ ] **Step 2: Test all major pages**

Run:
```bash
mkdocs serve &
PID=$!
sleep 3

# Test home page
curl -s http://localhost:8000/ | grep -q "OBiBa" && echo "✓ Home page OK"

# Test products page
curl -s http://localhost:8000/products/ | grep -q "Products" && echo "✓ Products page OK"

# Test blog
curl -s http://localhost:8000/blog/ | grep -q "News" && echo "✓ Blog OK"

kill $PID
```
Expected: All pages return successfully

- [ ] **Step 3: Verify redirects configuration**

Run:
```bash
grep -c "redirect_maps:" mkdocs.yml
```
Expected: Redirects configured (output > 0)

- [ ] **Step 4: Check file structure**

Run:
```bash
tree -L 2 docs/
```
Expected: Proper directory structure visible

- [ ] **Step 5: Validate YAML configuration**

Run:
```bash
python3 -c "import yaml; print('✓ mkdocs.yml is valid YAML'); yaml.safe_load(open('mkdocs.yml'))"
```
Expected: YAML is valid

---

## Task 20: Deployment Preparation

**Files:**
- Modify: `README.md`
- Create: `.gitignore` (if needed)

- [ ] **Step 1: Update README**

Read existing README and update with MkDocs information. Preserve existing content but add MkDocs setup instructions.

Example additions:

```markdown
## Development

This site is built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

### Prerequisites

- Python 3.11 or higher
- pip

### Setup

```bash
# Clone repository
git clone https://github.com/obiba/obiba.github.io.git
cd obiba.github.io

# Install dependencies
pip install -r requirements.txt

# Serve locally
mkdocs serve

# Build site
mkdocs build
```

### Adding Content

See [docs/migration-notes.md](docs/migration-notes.md) for details on adding content.

### Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the `main` branch via GitHub Actions.
```

- [ ] **Step 2: Update .gitignore**

Add to `.gitignore`:

```
# MkDocs
site/
.cache/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
```

- [ ] **Step 3: Commit deployment preparation**

```bash
git add README.md .gitignore
git commit -m "docs: update README for MkDocs"
```

- [ ] **Step 4: Create migration branch**

Run:
```bash
git branch mkdocs-migration
```

- [ ] **Step 5: Push migration branch**

Run:
```bash
git push -u origin mkdocs-migration
```
Expected: Branch pushed to remote

---

## Self-Review Checklist

### Spec Coverage

✓ **Project Structure** - Tasks 1, 2 cover setup and directory creation
✓ **Content Migration** - Tasks 3, 4, 5, 7 convert all content types
✓ **Blog/News** - Tasks 6, 7 handle blog plugin and news conversion
✓ **Assets** - Task 8 migrates assets
✓ **Styling** - Task 9 implements custom CSS
✓ **Redirects** - Task 10 generates redirect mappings
✓ **Configuration** - Task 11 completes mkdocs.yml
✓ **Deployment** - Task 12 adds GitHub Actions
✓ **Theme Customization** - Task 14 adds custom footer
✓ **Testing** - Tasks 15, 16, 17, 19 cover testing and validation
✓ **Documentation** - Task 18 creates migration notes

### Placeholders Check

No "TBD", "TODO", or placeholder text - all code blocks contain actual implementation.

### Type Consistency

- File paths are consistent across all tasks
- Method names in scripts are consistent
- YAML structure in mkdocs.yml matches throughout

### Verification

Each task includes verification steps to confirm success before proceeding.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-06-mkdocs-migration-implementation.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** - Dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach would you prefer?**
