import pytest
from unittest.mock import patch, MagicMock, mock_open
from sshcms.render import generate_feed
import xml.etree.ElementTree as ET

def test_generate_feed():
    with patch('sshcms.render.ContentManager') as mock_cm_class, \
         patch('sshcms.render.Path.mkdir'), \
         patch('builtins.open', mock_open()) as mocked_file:
        
        mock_cm = MagicMock()
        mock_cm.site_dir = MagicMock()
        
        posts_dir = MagicMock()
        mock_cm.site_dir.__truediv__.return_value = posts_dir
        posts_dir.exists.return_value = True
        
        mock_post = MagicMock()
        # Mock path generation: /posts/test.md -> /posts/test
        mock_post.relative_to.return_value.with_suffix.return_value = MagicMock()
        mock_post.relative_to.return_value.with_suffix.return_value.__str__.return_value = "posts/test"
        mock_post.stat().st_mtime = 1600000000.0
        posts_dir.glob.return_value = [mock_post]
        
        mock_cm.get_page.return_value = {
            'title': 'Test Post',
            'content': 'Test content'
        }
        
        mock_cm_class.return_value = mock_cm
        
        generate_feed()
        
        handle = mocked_file()
        handle.write.assert_called()
        
        written_content = handle.write.call_args[0][0]
        root = ET.fromstring(written_content)
        assert root.tag == '{http://www.w3.org/2005/Atom}feed'
        assert root.find('{http://www.w3.org/2005/Atom}title').text == 'SSHCMS Feed'
        
        entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        assert len(entries) == 1
        assert entries[0].find('{http://www.w3.org/2005/Atom}title').text == 'Test Post'
        assert entries[0].find('{http://www.w3.org/2005/Atom}summary').text == 'Test content...'

def test_generate_feed_skips_invalid_posts():
    with patch('sshcms.render.ContentManager') as mock_cm_class, \
         patch('sshcms.render.Path.mkdir'), \
         patch('builtins.open', mock_open()) as mocked_file:
        
        mock_cm = MagicMock()
        mock_cm.site_dir = MagicMock()
        
        posts_dir = MagicMock()
        mock_cm.site_dir.__truediv__.return_value = posts_dir
        posts_dir.exists.return_value = True
        
        post1 = MagicMock()
        post1.relative_to.return_value.with_suffix.return_value = MagicMock()
        post1.stat().st_mtime = 1600000000.0
        
        post2 = MagicMock()
        post2.relative_to.return_value.with_suffix.return_value = MagicMock()
        post2.stat().st_mtime = 1600000001.0
        
        posts_dir.glob.return_value = [post1, post2]
        
        mock_cm.get_page.side_effect = [
            {'title': 'Valid Post', 'content': 'Valid content'},
            {'content': 'Missing title'}
        ]
        
        mock_cm_class.return_value = mock_cm
        
        generate_feed()
        
        handle = mocked_file()
        written_content = handle.write.call_args[0][0]
        root = ET.fromstring(written_content)
        entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        assert len(entries) == 1
        assert entries[0].find('{http://www.w3.org/2005/Atom}title').text == 'Valid Post'

def test_generate_feed_stable_ordering():
    with patch('sshcms.render.ContentManager') as mock_cm_class, \
         patch('sshcms.render.Path.mkdir'), \
         patch('builtins.open', mock_open()) as mocked_file:
        
        mock_cm = MagicMock()
        mock_cm.site_dir = MagicMock()
        
        posts_dir = MagicMock()
        mock_cm.site_dir.__truediv__.return_value = posts_dir
        posts_dir.exists.return_value = True
        
        # Post 1: Oldest
        post1 = MagicMock()
        post1.relative_to.return_value.with_suffix.return_value = MagicMock()
        post1.relative_to.return_value.with_suffix.return_value.__str__.return_value = "posts/post1"
        post1.stat().st_mtime = 1600000000.0
        
        # Post 2: Newest, path 'post2'
        post2 = MagicMock()
        post2.relative_to.return_value.with_suffix.return_value = MagicMock()
        post2.relative_to.return_value.with_suffix.return_value.__str__.return_value = "posts/post2"
        post2.stat().st_mtime = 1600000010.0
        
        # Post 3: Newest, path 'post3'
        post3 = MagicMock()
        post3.relative_to.return_value.with_suffix.return_value = MagicMock()
        post3.relative_to.return_value.with_suffix.return_value.__str__.return_value = "posts/post3"
        post3.stat().st_mtime = 1600000010.0
        
        posts_dir.glob.return_value = [post1, post2, post3]
        
        mock_cm.get_page.side_effect = [
            {'title': 'Post 1', 'content': 'Content 1'},
            {'title': 'Post 2', 'content': 'Content 2'},
            {'title': 'Post 3', 'content': 'Content 3'},
        ]
        
        mock_cm_class.return_value = mock_cm
        
        generate_feed()
        
        handle = mocked_file()
        written_content = handle.write.call_args[0][0]
        root = ET.fromstring(written_content)
        entries = root.findall('{http://www.w3.org/2005/Atom}entry')
        
        assert len(entries) == 3
        # Order: mtime desc, path asc
        # post2 and post3 have same mtime, post2 path < post3 path
        # So: post2, post3, post1
        assert entries[0].find('{http://www.w3.org/2005/Atom}title').text == 'Post 2'
        assert entries[1].find('{http://www.w3.org/2005/Atom}title').text == 'Post 3'
        assert entries[2].find('{http://www.w3.org/2005/Atom}title').text == 'Post 1'
