import pytest
from crawl4ai.scraper.scorers.link_depth_scorer import LinkDepthScorer

class TestLinkDepthScorer:
    @pytest.fixture
    def seed_url(self):
        return "https://example.com"

    @pytest.fixture
    def scorer(self, seed_url):
        return LinkDepthScorer(seed_url)

    def test_score_root_url(self, scorer, seed_url):
        assert scorer.score(seed_url) == 1.0

    def test_score_first_level(self, scorer, seed_url):
        url = f"{seed_url}/page"
        assert scorer.score(url) == 0.5

    def test_score_second_level(self, scorer, seed_url):
        url = f"{seed_url}/category/page"
        assert scorer.score(url) == 1/3

    def test_score_third_level(self, scorer, seed_url):
        url = f"{seed_url}/category/subcategory/page"
        assert scorer.score(url) == 1/4

    def test_score_multiple_urls(self, scorer, seed_url):
        urls = [
            f"{seed_url}",
            f"{seed_url}/page1",
            f"{seed_url}/category/page2",
            f"{seed_url}/category/subcategory/page3"
        ]
        expected_scores = [1.0, 0.5, 1/3, 1/4]
        
        for url, expected_score in zip(urls, expected_scores):
            assert scorer.score(url) == pytest.approx(expected_score)

    def test_depths_storage(self, scorer, seed_url):
        urls = [
            f"{seed_url}",
            f"{seed_url}/page1",
            f"{seed_url}/category/page2",
            f"{seed_url}/category/subcategory/page3"
        ]
        
        for url in urls:
            scorer.score(url)
        
        assert scorer.depths == {
            f"{seed_url}": 0,
            f"{seed_url}/page1": 1,
            f"{seed_url}/category/page2": 2,
            f"{seed_url}/category/subcategory/page3": 3
        }

    def test_different_seed_url(self):
        seed_url = "https://different.com"
        scorer = LinkDepthScorer(seed_url)
        
        url = f"{seed_url}/a/b/c"
        assert scorer.score(url) == 1/4

    def test_url_with_query_params(self, scorer, seed_url):
        url = f"{seed_url}/page?param1=value1&param2=value2"
        assert scorer.score(url) == 0.5

    def test_url_with_fragment(self, scorer, seed_url):
        url = f"{seed_url}/page#section1"
        assert scorer.score(url) == 0.5