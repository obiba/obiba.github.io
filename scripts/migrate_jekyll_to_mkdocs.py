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
