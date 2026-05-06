#!/bin/bash
# Build validation script

set -e

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "=== MkDocs Build Validation ==="
echo

echo "1. Testing build (non-strict for migration phase)..."
mkdocs build --clean
if [ $? -eq 0 ]; then
    echo "✓ Build completed successfully"
else
    echo "✗ Build failed"
    exit 1
fi
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
    print('⚠ Found some broken links (expected during migration):')
    for link in broken_links[:10]:
        print(f'  {link}')
    if len(broken_links) > 10:
        print(f'  ... and {len(broken_links) - 10} more')
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
