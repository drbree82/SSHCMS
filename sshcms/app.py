import sys
import os
import argparse
from .content import ContentManager
from .parser import WikiParser
from .state import StateManager

def main():
    parser = argparse.ArgumentParser(description="SSHCMS TUI")
    parser.add_argument("--agent", action="store_true", help="Run in agent mode")
    parser.add_argument("--page", default="/", help="Starting path")
    args = parser.parse_args()

    if args.agent:
        from .agent import run_agent
        run_agent(args.page)
        return

    from .tui import SSHCMSApp
    app = SSHCMSApp(start_path=args.page)
    app.run()

if __name__ == "__main__":
    main()

