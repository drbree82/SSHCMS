# Ticket 002 — Fix parser heading slug generation

## Read

- spec.md
- tests/test_parser.py
- sshcms/parser.py

## Modify only

- sshcms/parser.py
- tests/test_parser.py

## Goal

Fix heading slug generation so punctuation does not appear in anchor IDs.

## Required behaviour

Heading:

```markdown
## Hello, World!

should produce:

{"id": "hello-world", "label": "Hello, World!", "level": 2}

Also preserve existing heading behaviour:

# Main Title
## Sub Heading
### Small Heading

should still produce:

main-title
sub-heading
small-heading
Constraints
Do not modify content, render, state, agent, app, or TUI files.
Keep the parser implementation simple.
Do not rewrite the parser.
Run

uv run pytest -v

Success criteria
tests/test_parser.py includes the punctuation slug test
sshcms/parser.py implements the fix
only sshcms/parser.py and tests/test_parser.py changed
tests pass
