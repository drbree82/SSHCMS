import sys
import yaml
import argparse
from .content import ContentManager

def run_agent(path: str = "/"):
    cm = ContentManager()
    page = cm.get_page(path)

    if not page:
        print(f"Error: Page {path} not found", file=sys.stderr)
        sys.exit(1)

    output = {
        'type': 'page',
        'path': page['path'],
        'title': page['title'],
        'content_text': page['content'],
        'links': page['links'],
        'anchors': [{'id': h['id'], 'label': h['label']} for h in page['headings']]
    }

    print(yaml.dump(output, sort_keys=False))

def main():
    parser = argparse.ArgumentParser(description="SSHCMS Agent Mode")
    parser.add_argument("path", nargs="?", default="/", help="Path to the page")
    args = parser.parse_args()
    run_agent(args.path)

if __name__ == "__main__":
    main()
