import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from .parser import WikiParser

class ContentManager:
    def __init__(self, site_dir: str = "site"):
        path = Path(site_dir)
        if path.is_absolute():
            self.site_dir = path.resolve()
        else:
            # Resolve relative to project root (parent of sshcms package)
            self.site_dir = (Path(__file__).parent.parent / path).resolve()

    def resolve_path(self, path: str) -> Optional[Path]:
        if path == "/" or not path:
            return self.site_dir / "index.md"
        
        # Remove leading slash and add .md extension
        rel_path = path.lstrip("/")
        if not rel_path.endswith(".md"):
            rel_path += ".md"
        
        # Secure path resolution to prevent traversal
        try:
            target_path = (self.site_dir / rel_path).resolve()
            if not target_path.is_relative_to(self.site_dir):
                return None
            return target_path
        except (OSError, RuntimeError):
            return None

    def get_page(self, path: str) -> Optional[Dict[str, Any]]:
        file_path = self.resolve_path(path)
        
        if file_path is None or not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from first H1 or filename
        title = file_path.stem.replace('-', ' ').title()
        for line in content.splitlines():
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        return {
            'path': path,
            'title': title,
            'content': content,
            'links': WikiParser.parse_links(content),
            'headings': WikiParser.extract_headings(content)
        }

    def search(self, query: str) -> List[Dict[str, Any]]:
        results = []
        query = query.lower()
        for path_str in self.list_pages():
            page = self.get_page(path_str)
            if page and (query in page['content'].lower() or query in page['title'].lower()):
                results.append(page)
        return results

    def list_pages(self) -> List[str]:
        pages = []
        for path in self.site_dir.rglob("*.md"):
            # Convert file path to URL path
            rel_path = path.relative_to(self.site_dir).with_suffix('')
            url_path = "/" + str(rel_path).replace(os.sep, '/').replace('index', '')
            if url_path == "//":
                url_path = "/"
            pages.append(url_path)
        return sorted(list(set(pages)))
