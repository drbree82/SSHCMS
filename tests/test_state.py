import pytest
from sshcms.state import StateManager

@pytest.fixture
def state_dir(tmp_path):
    d = tmp_path / "state"
    return d

def test_session_lifecycle(state_dir):
    sm = StateManager(state_dir=str(state_dir))
    
    session_id = sm.create_session(username="alice", path="/about")
    assert session_id is not None
    
    session = sm.get_session(session_id)
    assert session is not None
    assert session['username'] == "alice"
    assert session['requested_path'] == "/about"
    
    assert sm.get_session("nonexistent") is None

def test_user_state(state_dir):
    sm = StateManager(state_dir=str(state_dir))
    
    user_data = {"theme": "dark", "last_page": "/about"}
    sm.save_user_state("bob", user_data)
    
    loaded_data = sm.get_user_state("bob")
    assert loaded_data == user_data
    
    assert sm.get_user_state("unknown") is None
