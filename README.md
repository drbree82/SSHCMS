# SSHCMS

A terminal-first CMS served over SSH.

## Features

- TUI interface powered by Textual.
- Wiki-style linking (`[[Page]]`).
- Agent-facing structured output.
- Atom feed generation.
- No cookies, server-side state.

## Installation

```bash
uv sync
```

## Usage

### Human TUI
```bash
uv run sshcms --page /path/to/page
```

### Agent Mode
```bash
uv run sshcms --agent /path/to/page
# or
uv run sshcms-agent /path/to/page
```

### Feed Generation
```bash
uv run sshcms-feed
```

## Architecture
 
- `site/`: Markdown content.
- `state/`: User and session state.
- `public/`: Generated static assets (e.g., feed.xml).
 
## Deployment
 
To serve SSHCMS as a shell for a specific user, add the following to your `/etc/ssh/sshd_config`:
 
```ssh
Match User sshcms-user
    ForceCommand uv run sshcms
```
 
Then create the user:
 
```bash
sudo useradd -m -s /bin/false sshcms-user
```
 
Ensure the `sshcms-user` has access to the project directory and `uv`.

