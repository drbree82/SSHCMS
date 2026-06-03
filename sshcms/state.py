import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class StateManager:
    def __init__(self, state_dir: str = "state"):
        if not os.path.isabs(state_dir):
            base = Path(__file__).resolve().parent.parent
            self.state_dir = (base / state_dir).resolve()
        else:
            self.state_dir = Path(state_dir).resolve()
            
        self.users_dir = self.state_dir / "users"
        self.sessions_dir = self.state_dir / "sessions"
        
        self.users_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self, username: Optional[str] = None, path: str = "/", fingerprint: Optional[str] = None) -> str:
        session_id = str(uuid.uuid4())
        session_data = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'requested_path': path,
            'username': username,
            'fingerprint': fingerprint
        }
        
        session_file = self.sessions_dir / f"{session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2)
        
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return None
        
        with open(session_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_user_state(self, username: str, state: Dict[str, Any]):
        user_file = self.users_dir / f"{username}.json"
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)

    def get_user_state(self, username: str) -> Optional[Dict[str, Any]]:
        user_file = self.users_dir / f"{username}.json"
        if not user_file.exists():
            return None
        
        with open(user_file, 'r', encoding='utf-8') as f:
            return json.load(f)
