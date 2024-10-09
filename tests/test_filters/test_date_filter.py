import pytest
from datetime import datetime
from unittest.mock import patch, Mock
from crawl4ai.scraper.filters.date_filter import DateFilter
import requests

class TestDateFilter:
    @pytest.fixture
    def min_date(self):
        return datetime(2020, 1, 1)

    @pytest.fixture
    def max_date(self):
        return datetime(2021, 1, 1)

    @pytest.fixture
    def filter(self, min_date, max_date):
        return DateFilter(min_date, max_date)

    @patch('requests.head')
    def test_apply_within_date_range(self, mock_head, filter):
        mock_response = Mock()
        mock_response.headers = {'Last-Modified': 'Mon, 01 Jun 2020 10:00:00 GMT'}
        mock_head.return_value = mock_response

        url = "http://example.com"
        assert filter.apply(url) == True

    @patch('requests.head')
    def test_apply_outside_date_range(self, mock_head, filter):
        mock_response = Mock()
        mock_response.headers = {'Last-Modified': 'Mon, 01 Jun 2019 10:00:00 GMT'}
        mock_head.return_value = mock_response

        url = "http://example.com"
        assert filter.apply(url) == False

    @patch('requests.head')
    def test_apply_no_last_modified_header(self, mock_head, filter):
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
