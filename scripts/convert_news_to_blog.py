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
JEKYLL_INCLUDES = Path('_includes/themes/bootstrap/news')
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
    
    def extract_include_path(self, content):
        """Extract the include file path from Jekyll include statement"""
        # Pattern: {% include themes/bootstrap/section.html ... sectionBody="themes/bootstrap/news/opal-5.7-release.html" %}
        pattern = r'sectionBody="([^"]+)"'
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        return None
    
    def extract_section_title(self, content):
        """Extract section title from Jekyll include statement"""
        pattern = r'sectionTitle="([^"]+)"'
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        return None
    
    def read_include_file(self, include_path):
        """Read the content from the include file"""
        # Path is relative to _includes directory
        full_path = Path('_includes') / include_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            logger.warning(f"Include file not found: {full_path}")
            return ""
    
    def extract_date_from_path(self, path: Path) -> datetime:
        """Try to extract date from file path or content"""
        # Use file modification time as date
        if path.exists():
            mtime = path.stat().st_mtime
            return datetime.fromtimestamp(mtime)
        
        # Default to a reasonable date if can't determine
        return datetime(2024, 1, 1)
    
    def clean_html_to_markdown(self, html_content):
        """Convert simple HTML to Markdown"""
        content = html_content
        
        # Convert paragraphs
        content = re.sub(r'<p>\s*', '\n', content)
        content = re.sub(r'\s*</p>', '\n', content)
        
        # Convert links
        content = re.sub(r'<a\s+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', content)
        
        # Convert bold
        content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
        content = re.sub(r'<b>(.*?)</b>', r'**\1**', content)
        
        # Convert italic
        content = re.sub(r'<i>(.*?)</i>', r'*\1*', content)
        content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
        
        # Convert unordered lists
        content = re.sub(r'<ul[^>]*>', '\n', content)
        content = re.sub(r'</ul>', '\n', content)
        content = re.sub(r'<li[^>]*>', '- ', content)
        content = re.sub(r'</li>', '\n', content)
        
        # Remove remaining HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        
        # Clean up whitespace
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = content.strip()
        
        return content
    
    def convert_news_item(self, news_path: Path, category: str) -> bool:
        """Convert a single news item to blog post"""
        if not news_path.exists():
            return False
        
        logger.info(f"Converting news item: {news_path}")
        
        # Read index.html content
        with open(news_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter, body = self.parse_frontmatter(content)
        
        # Extract title from include statement
        title = self.extract_section_title(body)
        if not title:
            title = news_path.parent.name.replace('-', ' ').title()
        
        # Extract include file path
        include_path = self.extract_include_path(body)
        if include_path:
            # Read the actual content from the include file
            html_content = self.read_include_file(include_path)
            body = self.clean_html_to_markdown(html_content)
        else:
            logger.warning(f"No include path found in {news_path}")
            body = ""
        
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
            'date': post_date.date(),  # Use date object instead of string
            'categories': [category],
            'authors': ['obiba']
        }
        
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
