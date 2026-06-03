# SSHCMS Project Map

SSHCMS is an SSH-first CMS/protocol experiment.

Core files:
- spec.md: product/specification source of truth
- README.md: public project overview
- sshcms/parser.py: headings, links, wiki-link parsing
- sshcms/content.py: site markdown loading and path resolution
- sshcms/agent.py: machine/agent-readable output
- sshcms/render.py: Atom/feed generation
- sshcms/state.py: per-user/session state
- sshcms/tui.py: terminal UI
- sshcms/app.py: CLI entrypoint

Generated/ignored:
- .venv/
- state/
- public/feed.xml
- __pycache__/
- uv.lock
