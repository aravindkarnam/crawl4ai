from .url_scorer import URLScorer
from collections import defaultdict

class LinkDepthScorer(URLScorer):
    def __init__(self, seed_url: str):
        self.seed_url = seed_url
        self.depths = defaultdict(int)

    def score(self, url: str) -> float:
        # Calculate the depth of the URL from the seed URL
        # For simplicity, assume the depth is the number of slashes in the URL path
        depth = url.split(self.seed_url)[1].count('/')
        self.depths[url] = depth
        return 1 / (depth + 1)