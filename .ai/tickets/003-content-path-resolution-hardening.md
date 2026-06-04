Make content path resolution safer and clearer.

Read:
- spec.md
- tests/test_content.py
- sshcms/content.py

Modify only:
- sshcms/content.py
- tests/test_content.py

Focus:
- / resolves to index.md
- /about resolves to about.md
- /posts/hello resolves to posts/hello.md
- missing pages return None
- traversal attempts cannot escape site/
- behaviour is explicit, not accidental fallback magic

Run:
uv run pytest -v

Success:
- tests pass
- only content.py and test_content.py changed
