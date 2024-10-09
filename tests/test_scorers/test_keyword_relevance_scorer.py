import pytest
from crawl4ai.scraper.scorers.keyword_relevance_scorer import KeywordRelevanceScorer

class TestKeywordRelevanceScorer:
    def test_score_with_matches(self):
        scorer = KeywordRelevanceScorer(["python", "programming", "test"])
        url = "https://www.example.com/python-programming-tutorial"
        assert scorer.score(url) == pytest.approx(2/3)

    def test_score_without_matches(self):
        scorer = KeywordRelevanceScorer(["irrelevant", "words"])
        url = "https://www.example.com/python-programming-tutorial"
        assert scorer.score(url) == 0.0

    def test_score_case_insensitive(self):
        scorer = KeywordRelevanceScorer(["PYTHON", "Programming"])
        url = "https://www.example.com/python-programming-tutorial"
        assert scorer.score(url) == 1.0

    def test_score_empty_keywords(self):
        scorer = KeywordRelevanceScorer([])
        url = "https://www.example.com/python-programming-tutorial"
        assert scorer.score(url) == 0.0

    def test_score_partial_matches(self):
        scorer = KeywordRelevanceScorer(["python", "django", "flask"])
        url = "https://www.example.com/python-tutorial"
        assert scorer.score(url) == pytest.approx(1/3)