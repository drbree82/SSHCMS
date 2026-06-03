Build an MVP called **SSHCMS**.

Goal: a terminal-first CMS served over SSH. It should feel more like `lazygit`/`btop` than an old numbered-menu BBS.

Core idea:

* Content lives as plain Markdown/wiki-style files.
* Humans connect over SSH and get a rich TUI.
* Agents/tools can request structured output from the same content tree.
* No cookies. Any user state is deliberate server-side state.
* Open-source GPL-friendly architecture.
* Keep it simple, boring, inspectable, and easy to run.

Tech preference:

* Python.
* Use `uv`.
* Use `Textual` or another suitable Python TUI framework.
* Use OpenSSH integration where sensible, but for MVP it can also run locally as a TUI app first.
* Content should be plain files under `site/`.

MVP features:

1. Project structure

Create something like:

```text
sshcms/
  pyproject.toml
  README.md
  LICENSE
  sshcms/
    __init__.py
    app.py
    content.py
    parser.py
    render.py
    agent.py
    state.py
  site/
    index.md
    about.md
    posts/
      first-post.md
```

2. Markdown/wiki content

Support normal Markdown plus wiki links:

```md
# Welcome

This is my SSHCMS site.

[[About]]
[[posts/first-post|First Post]]
[[ssh://terminal.shop|Terminal Shop]]
[[https://example.com|Web fallback]]
```

Parse links into a canonical internal structure:

```yaml
href: /about
label: About
type: local
```

Support:

* `[[Page]]`
* `[[Page|Label]]`
* `[[ssh://host/path|Label]]`
* `[[https://url|Label]]`
* Markdown headings as anchors.

3. Human TUI renderer

Build a Textual TUI with:

* left navigation pane
* main content pane
* status/footer bar
* keyboard navigation
* mouse support if Textual supports it easily
* Enter follows selected link
* Backspace goes back
* `/` opens search or a placeholder search box
* `q` quits

The UI should have tasteful Unicode box-drawing/btop/lazygit-style flair, but not be bloated.

4. Agent renderer

Add a CLI mode:

```bash
uv run sshcms-agent /about
```

or:

```bash
uv run sshcms --agent /about
```

It should output structured JSON or YAML for the same page:

```yaml
type: page
path: /about
title: About
content_text: ...
links:
  - href: /posts/first-post
    label: First Post
    type: local
anchors:
  - id: heading-name
    label: Heading Name
```

5. Feed support

Generate Atom feed from Markdown files under `site/posts/`.

Command:

```bash
uv run sshcms-feed
```

Output:

```text
public/feed.xml
```

6. Server/SSH notes

Add documentation showing how to serve only the app through OpenSSH using `ForceCommand`.

Example config:

```conf
Match User sshcms
    ForceCommand /usr/local/bin/sshcms
    PermitTTY yes
    X11Forwarding no
    AllowTcpForwarding no
    AllowAgentForwarding no
    PermitTunnel no
```

Also document how public anonymous mode could work by ignoring inherited SSH usernames and treating identity as an app-layer concern.

7. State

Add a simple server-side state module for future use.

For now it can store JSON files like:

```text
state/
  users/
  sessions/
```

Session records should include:

* session UUID
* timestamp
* requested path
* username if available
* key fingerprint placeholder if available later

8. Keep it clean

Avoid overengineering.
Avoid databases in v0.
Avoid web frameworks unless absolutely needed.
No JavaScript.
No HTML dependency.
No authentication system beyond placeholders/documentation.
No Kubernetes yet; just leave architecture notes.

9. README

README should explain:

* what SSHCMS is
* why SSH instead of HTTP
* how to run locally
* how to add pages
* wiki link syntax
* agent output mode
* OpenSSH ForceCommand deployment idea
* design principles:

  * content first
  * renderer second
  * human and agent views share one source
  * anonymous by default
  * identity optional
  * no cookies
  * server-side intentional state

10. Acceptance criteria

After implementation, these commands should work:

```bash
uv sync
uv run sshcms
uv run sshcms --page /about
uv run sshcms --agent /about
uv run sshcms-feed
```

The TUI should be usable locally first. SSH deployment can be documented rather than fully automated for the first pass.

Focus on a working MVP, not perfection.

