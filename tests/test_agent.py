import pytest
import yaml
from unittest.mock import patch
from sshcms.agent import run_agent

def test_run_agent_success(capsys):
    mock_page = {
        'path': '/test',
        'title': 'Test Page',
        'content': 'Hello World',
        'links': [],
        'headings': [{'id': 'h1', 'label': 'Heading 1'}]
    }
    
    with patch('sshcms.agent.ContentManager') as MockCM:
        instance = MockCM.return_value
        instance.get_page.return_value = mock_page
        
        run_agent('/test')
        
        captured = capsys.readouterr()
        output = yaml.safe_load(captured.out)
        
        assert output['path'] == '/test'
        assert output['title'] == 'Test Page'
        assert output['content'] == 'Hello World'
        assert output['links'] == []
        assert output['headings'] == [{'id': 'h1', 'label': 'Heading 1'}]
        assert 'type' not in output

def test_run_agent_not_found(capsys):
    with patch('sshcms.agent.ContentManager') as MockCM:
        instance = MockCM.return_value
        instance.get_page.return_value = None
        
        with pytest.raises(SystemExit) as e:
            run_agent('/nonexistent')
        
        assert e.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Page /nonexistent not found" in captured.err
