from .url_scorer import URLScorer
from collections import defaultdict

class PageRankScorer(URLScorer):
    def __init__(self, damping_factor: float = 0.85, max_iterations: int = 100, convergence_threshold: float = 1e-6):
        self.damping_factor = damping_factor
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.scores = defaultdict(float)
        self.links = defaultdict(list)
        self.actual_iterations = 0

    def add_link(self, from_url: str, to_url: str):
        self.links[from_url].append(to_url)
        # Initialize scores for both URLs
        self.scores[from_url] = 0.0
        self.scores[to_url] = 0.0

    def score(self, url: str) -> float:
        if url not in self.scores:
            return 0.0

        # Initialize scores
        num_pages = len(self.scores)
        for u in self.scores:
            self.scores[u] = 1 / num_pages

        # Run PageRank algorithm
        for i in range(self.max_iterations):
            new_scores = defaultdict(float)
            for from_url, to_urls in self.links.items():
                if to_urls:
                    for to_url in to_urls:
                        new_scores[to_url] += self.scores[from_url] / len(to_urls)

            # Apply damping factor and normalize
            total_score = 0
            max_diff = 0
            for u in self.scores:
                new_score = (1 - self.damping_factor) / num_pages + self.damping_factor * new_scores[u]
                max_diff = max(max_diff, abs(new_score - self.scores[u]))
                self.scores[u] = new_score
                total_score += self.scores[u]

            # Normalize scores
            for u in self.scores:
                self.scores[u] /= total_score

            self.actual_iterations = i + 1

            # Check for convergence
            if max_diff < self.convergence_threshold:
                break

        return self.scores[url]
