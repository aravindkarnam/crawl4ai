import pytest
from unittest.mock import patch, Mock
from crawl4ai.scraper.filters.size_filter import SizeFilter
import requests

class TestSizeFilter:
    @pytest.fixture
    def min_size(self):
        return 1000  # 1 KB

    @pytest.fixture
    def max_size(self):
        return 5000  # 5 KB

    @pytest.fixture
    def filter(self, min_size, max_size):
        return SizeFilter(min_size, max_size)

    @patch('requests.head')
    def test_apply_within_size_range(self, mock_head, filter):
        mock_response = Mock()
        mock_response.headers = {'Content-Length': '3000'}
        mock_head.return_value = mock_response

        url = "http://example.com"
        assert filter.apply(url) == True

    @patch('requests.head')
    def test_apply_below_min_size(self, mock_head, filter):
        mock_response = Mock()
        mock_response.headers = {'Content-Length': '500'}
        mock_head.return_value = mock_response

        url = "http://example.com"
        assert filter.apply(url) == False

    @patch('requests.head')
    def test_apply_above_max_size(self, mock_head, filter):
        mock_response = Mock()
        mock_response.headers = {'Content-Length': '6000'}
        mock_head.return_value = mock_response

        url = "http://example.com"
        assert filter.apply(url) == False

    @patch('requests.head')
    def test_apply_no_content_length_header(self, mock_head, filter):
        mock_response = Mock()
        mock_response.headers = {}
        mock_head.return_value = mock_response

        url = "http://example.com"
        assert filter.apply(url) == False

    @patch('requests.head')
    def test_apply_request_exception(self, mock_head, filter):
        mock_head.side_effect = requests.RequestException("Connection error")

        url = "http://example.com"
        assert filter.apply(url) == False
