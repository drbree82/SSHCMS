import pytest
from unittest.mock import patch, MagicMock, mock_open
from sshcms.render import generate_feed

def test_generate_feed_no_crash():
    with patch('sshcms.render.ContentManager') as mock_cm_class, \
         patch('sshcms.render.Path.mkdir'), \
         patch('builtins.open', mock_open()) as mocked_file:
        
        mock_cm = MagicMock()
        mock_cm.site_dir = MagicMock()
        
        # Mock posts_dir = cm.site_dir / "posts"
        posts_dir = MagicMock()
        mock_cm.site_dir.__truediv__.return_value = posts_dir
        posts_dir.exists.return_value = True
        
        # Mock posts_dir.glob("*.md")
        mock_post = MagicMock()
        mock_post.relative_to.return_value.with_suffix.return_value = MagicMock()
        mock_post.stat().st_mtime = 1600000000.0
        posts_dir.glob.return_value = [mock_post]
        
        # Mock cm.get_page(path)
        mock_cm.get_page.return_value = {
            'title': 'Test Post',
            'content': 'Test content'
        }
        
        mock_cm_class.return_value = mock_cm
        
        # This should run without crashing
        generate_feed()
        
        # Verify that open was called to write the feed
        mocked_file.assert_called()
