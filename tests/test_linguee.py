"""Test the QueryLinguee class"""

from unittest import mock

from storyqueries.linguee import QueryLinguee


def test_linguee_creates():
    """Test if the QueryLinguee class is created correctly"""
    linguee = QueryLinguee()
    root = "https://linguee.com/english-french/search"
    query = "?source=french&query={search_string}"
    assert linguee.requester.base_url == root + query


def test_linguee_parse():
    """Test if the parse method works correctly"""
    linguee = QueryLinguee()
    mock_response = mock.MagicMock()
    mock_response.text = """
        <html><body>
            <span class="tag_e"><span class="tag_s">ExSource</span>
            <span class="tag_t">ExTranslation</span></span>
        </body></html>
        """
    linguee.parser.parse(mock_response)
    examples = [
        {"source": "ExSource", "translation": "ExTranslation"},
    ]
    assert linguee.parser.parse(mock_response) == {
        "examples": examples,
        "expressions": [],
    }
