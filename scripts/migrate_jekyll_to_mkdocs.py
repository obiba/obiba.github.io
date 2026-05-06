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
    
    def convert_product_page(self, product_name: str) -> bool:
        """Convert a Jekyll product page to MkDocs markdown"""
        # Check for both .html and .md source files
        html_source = JEKYLL_PAGES / 'products' / product_name / 'index.html'
        md_source = JEKYLL_PAGES / 'products' / product_name / 'index.md'
        
        if html_source.exists():
            source_file = html_source
        elif md_source.exists():
            source_file = md_source
        else:
            logger.warning(f"Product page not found: {html_source} or {md_source}")
            return False
        
        target_file = MKDOCS_DOCS / 'products' / product_name / 'index.md'
        
        logger.info(f"Converting product page: {product_name}")
        
        # Read source file
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter, body = self.parse_frontmatter(content)
        
        # Extract product information
        title = frontmatter.get('title', product_name.capitalize())
        menu = frontmatter.get('menu', {})
        wiki = menu.get('wiki', {}).get('href', '') if isinstance(menu.get('wiki'), dict) else ''
        download = menu.get('download', {}).get('href', '') if isinstance(menu.get('download'), dict) else ''
        github = menu.get('github', {}).get('href', '') if isinstance(menu.get('github'), dict) else ''
        demo = menu.get('demo', {}).get('href', '') if isinstance(menu.get('demo'), dict) else ''
        
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
        # Only add external links (not internal anchors like #download)
        if wiki and not wiki.startswith('#'):
            links.append(f"[:material-book: Documentation]({wiki}){{ .md-button }}")
        if download and not download.startswith('#'):
            links.append(f"[:material-download: Download]({download}){{ .md-button }}")
        if github and not github.startswith('#'):
            links.append(f"[:material-github: GitHub]({github}){{ .md-button }}")
        if demo and not demo.startswith('#'):
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

def main():
    """Main migration function"""
    logger.info("Starting Jekyll to MkDocs migration")
    converter = JekyllToMkDocsConverter()
    
    # Convert product pages
    logger.info("Converting product pages...")
    converter.convert_all_products()
    
    logger.info("Migration complete")

if __name__ == '__main__':
    main()
