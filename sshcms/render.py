import os
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape
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
            # Use file mtime as date
            mtime = post_file.stat().st_mtime
            date = datetime.fromtimestamp(mtime).isoformat()
            posts.append({
                'title': page['title'],
                'link': f"ssh://sshcms{path}", # Placeholder for SSH link
                'date': date,
                'content': page['content'][:200] + "..."
            })

    # Sort posts by date descending
    posts.sort(key=lambda x: x['date'], reverse=True)

    atom_feed = f'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{escape("SSHCMS Feed")}</title>
  <link href="ssh://sshcms/feed" />
  <updated>{datetime.now().isoformat()}</updated>
  <id>tag:sshcms.local,2026:feed</id>
'''
    for post in posts:
        atom_feed += f'''  <entry>
    <title>{escape(post['title'])}</title>
    <link href="{escape(post['link'])}" />
    <updated>{post['date']}</updated>
    <id>tag:sshcms.local,2026:{escape(post['title'].lower().replace(' ', '-'))}</id>
    <summary>{escape(post['content'])}</summary>
  </entry>
'''
    atom_feed += "</feed>"

    # Write to public/ relative to the package base
    base_dir = Path(__file__).resolve().parent.parent
    public_dir = base_dir / "public"
    public_dir.mkdir(exist_ok=True)
    
    feed_file = public_dir / "feed.xml"
    with open(feed_file, 'w', encoding='utf-8') as f:
        f.write(atom_feed)
    
    print(f"Feed generated at {feed_file}")

if __name__ == "__main__":
    generate_feed()
