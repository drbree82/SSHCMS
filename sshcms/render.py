import os
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from .content import ContentManager

def generate_feed():
    cm = ContentManager()
    posts_dir = cm.site_dir / "posts"
    
    if not posts_dir.exists():
        print("No posts directory found.")
        return

    posts = []
    for post_file in posts_dir.glob("*.md"):
        path = "/" + str(post_file.relative_to(cm.site_dir).with_suffix('')).replace(os.sep, '/')
        page = cm.get_page(path)
        if page:
            title = page.get('title')
            content = page.get('content')
            if not title or not content:
                continue
                
            mtime = post_file.stat().st_mtime
            date = datetime.fromtimestamp(mtime).isoformat()
            posts.append({
                'title': title,
                'link': f"ssh://sshcms{path}",
                'date': date,
                'content': content[:200] + "...",
                'mtime': mtime,
                'path': path
            })

    posts.sort(key=lambda x: (-x['mtime'], x['path']))

    feed = ET.Element('feed', {'xmlns': 'http://www.w3.org/2005/Atom'})
    ET.SubElement(feed, 'title').text = "SSHCMS Feed"
    ET.SubElement(feed, 'link', {'href': 'ssh://sshcms/feed'})
    ET.SubElement(feed, 'updated').text = datetime.now().isoformat()
    ET.SubElement(feed, 'id').text = "tag:sshcms.local,2026:feed"

    for post in posts:
        entry = ET.SubElement(feed, 'entry')
        ET.SubElement(entry, 'title').text = post['title']
        ET.SubElement(entry, 'link', {'href': post['link']})
        ET.SubElement(entry, 'updated').text = post['date']
        
        entry_id = f"tag:sshcms.local,2026:{post['path'].strip('/').replace('/', '-')}"
        ET.SubElement(entry, 'id').text = entry_id
        ET.SubElement(entry, 'summary').text = post['content']

    ET.indent(feed)
    atom_feed = '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(feed, encoding='utf-8').decode('utf-8')

    base_dir = Path(__file__).resolve().parent.parent
    public_dir = base_dir / "public"
    public_dir.mkdir(exist_ok=True)
    
    feed_file = public_dir / "feed.xml"
    with open(feed_file, 'w', encoding='utf-8') as f:
        f.write(atom_feed)
    
    print(f"Feed generated at {feed_file}")

if __name__ == "__main__":
    generate_feed()
