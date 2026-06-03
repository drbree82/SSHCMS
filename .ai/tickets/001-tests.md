# Ticket 001 — Add baseline tests

## Goal

Add pytest coverage before changing behaviour.

## Relevant files

- spec.md
- pyproject.toml
- sshcms/parser.py
- sshcms/content.py
- sshcms/state.py
- sshcms/render.py

## Constraints

- Do not modify TUI yet.
- Do not rewrite the application.
- Do not inspect .venv, state, public/feed.xml, or uv.lock.
- Keep changes minimal.

## Acceptance criteria

- pytest is added as a dev dependency if missing.
- tests/ directory exists.
- Parser tests cover headings and wiki links.
- Content tests cover /, /about, missing pages, and path traversal rejection.
- State tests cover creating/loading session state.
- Render tests cover feed generation without crashing.

## Commands to verify

uv run pytest
