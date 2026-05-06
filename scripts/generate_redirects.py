#!/usr/bin/env python3
"""
Generate redirect mappings for MkDocs redirects plugin
"""

import yaml
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def slugify(text):
    """Simple slugification matching MkDocs behavior"""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def extract_title_from_post(post_path):
    """Extract the title (first H1) from a blog post"""
    with open(post_path, 'r') as f:
        in_frontmatter = False
        for line in f:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue
            if not in_frontmatter and line.startswith('# '):
                return line[2:].strip()
    return None

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
                year, month, day, filename_slug = parts[0], parts[1], parts[2], parts[3]
                
                # Get the title from the post to generate the correct slug
                title = extract_title_from_post(post_file)
                if title:
                    url_slug = slugify(title)
                else:
                    url_slug = filename_slug
                
                # Determine category and old path from filename slug
                if 'opal' in filename_slug or 'mica' in filename_slug or 'rock' in filename_slug or 'agate' in filename_slug or 'amber' in filename_slug or 'onyx' in filename_slug:
                    # This is likely a release
                    # Extract product and version from filename slug
                    for product in products:
                        if product in filename_slug:
                            # Try to extract version
                            version = filename_slug.replace(product, '').strip('-').replace('-', '.')
                            old_url = f'pages/news/release/{product}/{version}/index.html'
                            new_url = f'blog/{year}/{month}/{day}/{url_slug}/'
                            redirects[old_url] = new_url
                            break
                else:
                    # This is likely an event
                    old_url = f'pages/news/event/{filename_slug}/index.html'
                    new_url = f'blog/{year}/{month}/{day}/{url_slug}/'
                    redirects[old_url] = new_url
    
    return redirects

def update_mkdocs_config(redirects):
    """Update mkdocs.yml with redirect mappings"""
    
    config_file = Path('mkdocs.yml')
    
    # Read the file content as text
    with open(config_file, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Find the plugins section and tags plugin (to insert after it)
    plugins_idx = None
    tags_plugin_idx = None
    markdown_extensions_idx = None
    
    for i, line in enumerate(lines):
        if line.strip() == 'plugins:':
            plugins_idx = i
        elif plugins_idx is not None and '- tags:' in line:
            tags_plugin_idx = i
            # Find the end of the tags plugin block
            j = i + 1
            while j < len(lines):
                if lines[j].strip() and not lines[j].strip().startswith('#'):
                    indent = len(lines[j]) - len(lines[j].lstrip())
                    if indent <= 2:  # Back to plugin level or less
                        break
                j += 1
            tags_plugin_idx = j - 1
        elif line.strip() == 'markdown_extensions:':
            markdown_extensions_idx = i
            break  # Stop here as plugins section is before markdown_extensions
    
    # Remove existing redirects plugin if present (could be in wrong place)
    new_lines = []
    skip_until = None
    for i, line in enumerate(lines):
        if skip_until is not None:
            if i <= skip_until:
                continue
            skip_until = None
        
        # Check if this line contains a redirects plugin entry
        if '- redirects:' in line or (line.strip().startswith('-') and 'redirects' in line):
            # Find the end of this plugin block
            start_indent = len(line) - len(line.lstrip())
            j = i + 1
            while j < len(lines):
                if lines[j].strip() == '' or lines[j].strip().startswith('#'):
                    j += 1
                    continue
                next_indent = len(lines[j]) - len(lines[j].lstrip())
                if next_indent <= start_indent:
                    break
                j += 1
            skip_until = j - 1
            continue
        
        new_lines.append(line)
    
    # Generate the redirects plugin YAML
    redirects_yaml = [
        '  ',
        '  - redirects:',
        '      redirect_maps:'
    ]
    for old_url, new_url in sorted(redirects.items()):
        redirects_yaml.append(f'        {old_url}: {new_url}')
    
    # Insert after the tags plugin
    if tags_plugin_idx is not None:
        # Find the actual position in new_lines (accounting for removed lines)
        insert_idx = tags_plugin_idx + 1
        if insert_idx > len(new_lines):
            insert_idx = len(new_lines)
        
        # Recalculate position by finding tags plugin in new_lines
        for i, line in enumerate(new_lines):
            if '- tags:' in line:
                # Find end of tags block
                j = i + 1
                while j < len(new_lines):
                    if new_lines[j].strip() and not new_lines[j].strip().startswith('#'):
                        indent = len(new_lines[j]) - len(new_lines[j].lstrip())
                        if indent <= 2:
                            break
                    j += 1
                insert_idx = j
                break
        
        new_lines = new_lines[:insert_idx] + redirects_yaml + new_lines[insert_idx:]
    
    # Write the updated config
    with open(config_file, 'w') as f:
        f.write('\n'.join(new_lines))
    
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
