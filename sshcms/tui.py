import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Markdown, ListView, ListItem, Input
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from .content import ContentManager
from .parser import WikiParser
from .state import StateManager

class PageItem(ListItem):
    def __init__(self, path: str, label: str):
        super().__init__()
        self.path = path
        self.label = label

    def compose(self) -> ComposeResult:
        yield Static(self.label)

class SSHCMSApp(App):
    CSS = """
    Screen {
        background: #1a1a1a;
    }
    #main-container {
        layout: horizontal;
    }
    #sidebar {
        width: 30;
        background: #2a2a2a;
        border-right: tall #444;
    }
    #content-pane {
        width: 1fr;
        padding: 1 2;
    }
    ListItem {
        padding: 0 1;
    }
    .selected {
        background: #444;
        text-style: bold;
    }
    #search-input {
        margin: 1 0;
        border: tall #444;
    }
    #search-overlay {
        display: none;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("/", "toggle_search", "Search"),
        Binding("backspace", "go_back", "Back"),
        Binding("esc", "clear_search", "Clear Search"),
    ]

    def __init__(self, start_path="/", **kwargs):
        super().__init__(**kwargs)
        self.cm = ContentManager()
        self.sm = StateManager()
        self.current_path = start_path
        self.history = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-container"):
            with Vertical(id="sidebar"):
                yield Input(placeholder="Search...", id="search-input")
                yield ListView(id="page-list")
            with Vertical(id="content-pane"):
                yield Markdown(id="content-view")
        yield Footer()

    def on_mount(self) -> None:
        # Create a session for auditing
        self.session_id = self.sm.create_session(
            path=self.current_path,
            username=os.environ.get("USER", "unknown"),
            fingerprint=os.environ.get("SSH_KEY_FINGERPRINT", "unknown")
        )
        self.load_page(self.current_path)

    def load_page(self, path: str) -> None:
        self.current_path = path
        content_data = self.cm.get_page(path)
        
        if content_data:
            content_text = content_data.get('content', '# Page Not Found')
            
            # Convert wiki links [[Page|Label]] to Markdown [Label](/path)
            def wiki_to_markdown(target, label):
                if target.startswith(('http://', 'https://', 'ssh://')):
                    return f"[{label}]({target})"
                return f"[{label}](/{target.lstrip('/')})"
            
            rendered_text = WikiParser.render_wiki_links(content_text, wiki_to_markdown)
            self.query_one("#content-view", Markdown).update(rendered_text)
            
            # Update sidebar with links found on page, unless searching
            search_input = self.query_one("#search-input", Input)
            if not search_input.value:
                links = content_data.get('links', [])
                page_list = self.query_one("#page-list", ListView)
                page_list.clear()
                for link in links:
                    if link['type'] == 'local':
                        page_list.append(PageItem(link['href'], link['label']))
        else:
            self.query_one("#content-view", Markdown).update("# 404 Not Found")


    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, PageItem):
            self.history.append(self.current_path)
            self.load_page(item.path)

    def action_go_back(self) -> None:
        if self.history:
            prev_path = self.history.pop()
            self.load_page(prev_path)

    def update_sidebar_results(self, query: str) -> None:
        page_list = self.query_one("#page-list", ListView)
        page_list.clear()
        
        if query:
            results = self.cm.search(query)
            for page in results:
                page_list.append(PageItem(page['path'], page['title']))
        else:
            # Restore links from current page if search is cleared
            content_data = self.cm.get_page(self.current_path)
            if content_data:
                links = content_data.get('links', [])
                for link in links:
                    if link['type'] == 'local':
                        page_list.append(PageItem(link['href'], link['label']))

    def on_input_changed(self, event: Input.Changed) -> None:
        self.update_sidebar_results(event.value)

    def action_toggle_search(self) -> None:
        self.query_one("#search-input", Input).focus()

    def action_clear_search(self) -> None:
        search_input = self.query_one("#search-input", Input)
        search_input.value = ""
        self.update_sidebar_results("")
        search_input.focus()
