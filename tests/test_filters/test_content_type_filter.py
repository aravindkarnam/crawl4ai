import pytest
from unittest.mock import patch, Mock
import requests
from crawl4ai.scraper.filters.content_type_filter import ContentTypeFilter

class TestContentTypeFilter:
    @pytest.fixture
    def content_type_filter(self):
        return ContentTypeFilter("text/html")

    @pytest.fixture
    def mock_response(self):
        response = Mock()
        response.headers = {}
        return response

    @pytest.mark.parametrize("content_type,expected", [
        ("text/html; charset=utf-8", True),
        ("application/pdf", False),
        ("text/html", True),
        ("TEXT/HTML", True),
    ])
    def test_apply_with_different_content_types(self, content_type_filter, mock_response, content_type, expected):
        mock_response.headers['Content-Type'] = content_type
        with patch('requests.head', return_value=mock_response):
            assert content_type_filter.apply("http://example.com") == expected

    def test_apply_no_content_type_header(self, content_type_filter, mock_response):
        with patch('requests.head', return_value=mock_response):
            assert content_type_filter.apply("http://example.com") == False

    @pytest.mark.parametrize("exception", [
        requests.RequestException("Connection error"),
        requests.Timeout("Request timed out"),
        requests.ConnectionError("Connection failed"),
    ])
    def test_apply_request_exceptions(self, content_type_filter, exception):
        with patch('requests.head', side_effect=exception):
            assert content_type_filter.apply("http://example.com") == False

    def test_apply_different_content_types(self):
        html_filter = ContentTypeFilter("text/html")
        json_filter = ContentTypeFilter("application/json")
        
        mock_response = Mock()
        mock_response.headers = {'Content-Type': 'text/html; charset=utf-8'}
        
        with patch('requests.head', return_value=mock_response):
            assert html_filter.apply("http://example.com") == True
            assert json_filter.apply("http://example.com") == False

    def test_apply_partial_content_type_match(self):
        content_type_filter = ContentTypeFilter("application/json")
        mock_response = Mock()
        mock_response.headers = {'Content-Type': 'application/json; charset=utf-8'}
        
        with patch('requests.head', return_value=mock_response):
            assert content_type_filter.apply("http://example.com") == True
