import pytest
from pathlib import Path
from sshcms.content import ContentManager

@pytest.fixture
def site_dir(tmp_path):
    d = tmp_path / "site"
    d.mkdir()
    (d / "index.md").write_text("# Home\nWelcome home.", encoding="utf-8")
    (d / "about.md").write_text("# About\nAbout me.", encoding="utf-8")
    posts = d / "posts"
    posts.mkdir()
    (posts / "first-post.md").write_text("# First Post\nHello world.", encoding="utf-8")
    return d

def test_resolve_path(site_dir):
    cm = ContentManager(site_dir=str(site_dir))
    
    assert cm.resolve_path("/") == site_dir / "index.md"
    assert cm.resolve_path("/about") == site_dir / "about.md"
    assert cm.resolve_path("/posts/first-post") == site_dir / "posts/first-post.md"

def test_path_traversal(site_dir):
    cm = ContentManager(site_dir=str(site_dir))
    # Attempt to traverse out of site_dir
    assert cm.resolve_path("/../secret.txt") is None
    assert cm.resolve_path("/posts/../../secret.txt") is None
    assert cm.resolve_path("/about/../../etc/passwd") is None

def test_get_page(site_dir):
    cm = ContentManager(site_dir=str(site_dir))
    
    page = cm.get_page("/about")
    assert page is not None
    assert page['title'] == "About"
    assert "About me." in page['content']
    assert page['path'] == "/about"
    
    assert cm.get_page("/nonexistent") is None


def test_get_page_title_from_h1(site_dir):
    (site_dir / "custom.md").write_text("# Custom Title\nContent", encoding="utf-8")
    cm = ContentManager(site_dir=str(site_dir))
    page = cm.get_page("/custom")
    assert page['title'] == "Custom Title"

def test_list_pages(site_dir):
    cm = ContentManager(site_dir=str(site_dir))
    pages = cm.list_pages()
    assert "/" in pages
    assert "/about" in pages
    assert "/posts/first-post" in pages
    assert len(pages) == 3
    assert pages == sorted(pages)

def test_list_pages_with_index_in_name(site_dir):
    (site_dir / "index-of-things.md").write_text("# Index\nContent", encoding="utf-8")
    cm = ContentManager(site_dir=str(site_dir))
    pages = cm.list_pages()
    assert "/index-of-things" in pages
