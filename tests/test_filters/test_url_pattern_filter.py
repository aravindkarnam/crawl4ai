import pytest
import re
from crawl4ai.scraper.filters.url_pattern_filter import URLPatternFilter

class TestURLPatternFilter:
    @pytest.fixture
    def pattern(self):
        return re.compile(r'^https?://.*\.example\.com/.*$')

    @pytest.fixture
    def filter(self, pattern):
        return URLPatternFilter(pattern)

    def test_apply_url_matches_pattern(self, filter):
        url = "http://sub.example.com/path"
        assert filter.apply(url) == True

    def test_apply_url_does_not_match_pattern(self, filter):
        url = "http://notexample.com/path"
        assert filter.apply(url) == False

    def test_apply_url_partial_match(self, filter):
        url = "http://example.org"
        assert filter.apply(url) == False

    def test_apply_generic_pattern(self):
        pattern = re.compile(r'.*')
        url_filter = URLPatternFilter(pattern)
        url = "http://any.url/whatever"
        assert url_filter.apply(url) == True

    def test_apply_specific_pattern(self):
        pattern = re.compile(r'^https://specific.example.com/path$')
        url_filter = URLPatternFilter(pattern)
        
        matching_url = "https://specific.example.com/path"
        non_matching_url = "https://specific.example.com/another_path"
        
        assert url_filter.apply(matching_url) == True
        assert url_filter.apply(non_matching_url) == False
