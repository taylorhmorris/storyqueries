"""Test the QueryPixabay class"""

from unittest import mock

from storyqueries.pixabay import QueryPixabay


def test_pixabay_creates():
    """Test if the QueryPixabay class is created correctly"""
    pixabay = QueryPixabay(lang="fr", api_key="1234567890")
    assert pixabay.lang == "fr"
    assert pixabay.api_key == "1234567890"
    root = "https://pixabay.com/api/"
    query = "?key={api_key}&q={search_string}&lang={lang}"
    extra = "&image_type=photo&safesearch=true"
    assert pixabay.requester.base_url == root + query + extra


def test_pixabay_parse():
    """Test if the parse method works correctly"""
    pixabay = QueryPixabay(lang="fr", api_key="123456")
    s = '{"hits": [{"id": 1, "pageURL": "https://pixabay.com/photos/1"}]}'
    raw = mock.MagicMock()
    raw.status_code = 200
    raw.content = s.encode("utf-8")
    parsed = pixabay.parser.parse(raw)
    assert parsed["hits"][0]["id"] == 1
    assert parsed["hits"][0]["pageURL"] == "https://pixabay.com/photos/1"
