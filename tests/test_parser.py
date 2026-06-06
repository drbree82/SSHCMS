from sshcms.parser import WikiParser

def test_parse_links():
    text = "Welcome to [[About]] and [[posts/first-post|First Post]]. Check [[ssh://terminal.shop|Shop]] or [[https://example.com|Web]]."
    links = WikiParser.parse_links(text)
    
    assert len(links) == 4
    assert links[0] == {'href': '/About', 'label': 'About', 'type': 'local'}
    assert links[1] == {'href': '/posts/first-post', 'label': 'First Post', 'type': 'local'}
    assert links[2] == {'href': 'ssh://terminal.shop', 'label': 'Shop', 'type': 'ssh'}
    assert links[3] == {'href': 'https://example.com', 'label': 'Web', 'type': 'web'}

def test_extract_headings():
    text = "# Main Title\nSome text\n## Sub Heading\nMore text\n### Small Heading"
    headings = WikiParser.extract_headings(text)
    
    assert len(headings) == 3
    assert headings[0] == {'id': 'main-title', 'label': 'Main Title', 'level': 1}
    assert headings[1] == {'id': 'sub-heading', 'label': 'Sub Heading', 'level': 2}
    assert headings[2] == {'id': 'small-heading', 'label': 'Small Heading', 'level': 3}

def test_extract_headings_punctuation():
    text = "## Hello, World!"
    headings = WikiParser.extract_headings(text)
    assert len(headings) == 1
    assert headings[0] == {'id': 'hello-world', 'label': 'Hello, World!', 'level': 2}

def test_parser_edge_cases():
    # Local wiki link
    assert WikiParser.parse_links("[[about]]")[0] == {'href': '/about', 'label': 'about', 'type': 'local'}
    
    # Labelled local wiki link
    assert WikiParser.parse_links("[[posts/hello|Hello Post]]")[0] == {'href': '/posts/hello', 'label': 'Hello Post', 'type': 'local'}
    
    # SSH link
    assert WikiParser.parse_links("[[ssh://terminal.shop|Terminal Shop]]")[0] == {'href': 'ssh://terminal.shop', 'label': 'Terminal Shop', 'type': 'ssh'}
    

def test_wiki_link_hardening():
    # Normal wiki links
    assert WikiParser.parse_links("[[About]]")[0] == {'href': '/About', 'label': 'About', 'type': 'local'}
    assert WikiParser.parse_links("[[About Page]]")[0] == {'href': '/About Page', 'label': 'About Page', 'type': 'local'}
    assert WikiParser.parse_links("[[posts/hello]]")[0] == {'href': '/posts/hello', 'label': 'posts/hello', 'type': 'local'}

    # Multiple wiki links
    text = "[[About]] and [[posts/hello]]"
    links = WikiParser.parse_links(text)
    assert len(links) == 2
    assert links[0] == {'href': '/About', 'label': 'About', 'type': 'local'}
    assert links[1] == {'href': '/posts/hello', 'label': 'posts/hello', 'type': 'local'}

    # Empty wiki-link targets
    assert WikiParser.parse_links("[[ ]]") == []
    assert WikiParser.parse_links("[[  ]]") == []

    # Malformed / incomplete wiki links (should not crash and should be handled safely)
    # [[|Label]] - target is empty, should be skipped
    assert WikiParser.parse_links("[[|Label]]") == []
    
    # [[About|]] - target is About, label is empty string
    links = WikiParser.parse_links("[[About|]]")
    assert len(links) == 1
    assert links[0] == {'href': '/About', 'label': '', 'type': 'local'}

    # Nested brackets or other weirdness that doesn't match the regex
    assert WikiParser.parse_links("[[[About]]]") == []
    assert WikiParser.parse_links("[[About") == []
    assert WikiParser.parse_links("[[About]] [[About]]") == [
        {'href': '/About', 'label': 'About', 'type': 'local'},
        {'href': '/About', 'label': 'About', 'type': 'local'}
    ]
    
