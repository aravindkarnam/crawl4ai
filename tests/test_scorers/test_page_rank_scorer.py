import pytest
from crawl4ai.scraper.scorers.page_rank_scorer import PageRankScorer

class TestPageRankScorer:
    @pytest.fixture
    def scorer(self):
        return PageRankScorer(damping_factor=0.85, max_iterations=100)

    def test_initialization(self, scorer):
        assert scorer.damping_factor == 0.85
        assert scorer.max_iterations == 100
        assert len(scorer.scores) == 0
        assert len(scorer.links) == 0

    def test_add_link(self, scorer):
        scorer.add_link("http://a.com", "http://b.com")
        scorer.add_link("http://a.com", "http://c.com")
        scorer.add_link("http://b.com", "http://c.com")

        assert len(scorer.links) == 2
        assert len(scorer.links["http://a.com"]) == 2
        assert len(scorer.links["http://b.com"]) == 1

    def test_score_single_node(self, scorer):
        scorer.add_link("http://a.com", "http://a.com")
        score = scorer.score("http://a.com")
        assert score == pytest.approx(1.0)

    def test_score_two_nodes(self, scorer):
        scorer.add_link("http://a.com", "http://b.com")
        scorer.add_link("http://b.com", "http://a.com")

        score_a = scorer.score("http://a.com")
        score_b = scorer.score("http://b.com")

        assert score_a == pytest.approx(score_b)
        assert score_a + score_b == pytest.approx(1.0)

    def test_score_three_nodes(self, scorer):
        scorer.add_link("http://a.com", "http://b.com")
        scorer.add_link("http://b.com", "http://c.com")
        scorer.add_link("http://c.com", "http://a.com")

        score_a = scorer.score("http://a.com")
        score_b = scorer.score("http://b.com")
        score_c = scorer.score("http://c.com")

        assert score_a == pytest.approx(score_b)
        assert score_b == pytest.approx(score_c)
        assert score_a + score_b + score_c == pytest.approx(1.0)

    def test_score_complex_graph(self, scorer):
        scorer.add_link("http://a.com", "http://b.com")
        scorer.add_link("http://a.com", "http://c.com")
        scorer.add_link("http://b.com", "http://c.com")
        scorer.add_link("http://c.com", "http://a.com")
        scorer.add_link("http://d.com", "http://c.com")

        score_a = scorer.score("http://a.com")
        score_b = scorer.score("http://b.com")
        score_c = scorer.score("http://c.com")
        score_d = scorer.score("http://d.com")

        assert score_a + score_b + score_c + score_d == pytest.approx(1.0)
        assert score_c > score_a > score_b > score_d

    def test_score_nonexistent_url(self, scorer):
        scorer.add_link("http://a.com", "http://b.com")
        score = scorer.score("http://c.com")
        assert score == 0.0

    def test_custom_damping_factor(self):
        scorer = PageRankScorer(damping_factor=0.5, max_iterations=100)
        scorer.add_link("http://a.com", "http://b.com")
        scorer.add_link("http://b.com", "http://a.com")

        score_a = scorer.score("http://a.com")
        assert score_a == pytest.approx(0.5, rel=1e-2)

   