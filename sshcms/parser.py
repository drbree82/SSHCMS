import re
from typing import List, Dict, Any

class WikiParser:
    # Regex for [[Page]] or [[Page|Label]]
    # Group 1: Page/URL
    # Group 2: |Label (optional)
    WIKI_LINK_PATTERN = re.compile(r'(?<!\[)\[\[([^\]|\[]+)(?:\|([^\]]*))?\]\]')

    @staticmethod
    def parse_links(text: str) -> List[Dict[str, Any]]:
        links = []
        for match in WikiParser.WIKI_LINK_PATTERN.finditer(text):
            target = match.group(1).strip()
            if not target:
                continue
            label = match.group(2).strip() if match.group(2) is not None else target
            
            if target.startswith('ssh://'):
                link_type = 'ssh'
                href = target
            elif target.startswith('http://') or target.startswith('https://'):
                link_type = 'web'
                href = target
            else:
                link_type = 'local'
                # Ensure local links start with /
                href = f"/{target.lstrip('/')}"
            
            links.append({
                'href': href,
                'label': label,
                'type': link_type
            })
        return links

    @staticmethod
    def render_wiki_links(text: str, replacement_func):
        """
        Replaces [[Page|Label]] with something else.
        replacement_func takes (target, label) and returns the replacement string.
        """
        def replace(match):
            target = match.group(1).strip()
            label = match.group(2).strip() if match.group(2) else target
            return replacement_func(target, label)
        
        return WikiParser.WIKI_LINK_PATTERN.sub(replace, text)

    @staticmethod
    def extract_headings(text: str) -> List[Dict[str, str]]:
        headings = []
        # Match lines starting with #
        for line in text.splitlines():
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                # Create a simple ID: lowercase, remove punctuation, replace spaces with hyphens
                heading_id = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                headings.append({
                    'id': heading_id,
                    'label': title,
                    'level': level
                })
        return headings
