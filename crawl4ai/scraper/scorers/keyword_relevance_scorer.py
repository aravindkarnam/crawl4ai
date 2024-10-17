from .url_scorer import URLScorer
from typing import List

class KeywordRelevanceScorer(URLScorer):
    def __init__(self, keywords: List[str]):
        self.keywords = keywords  
    
    def score(self, url: str) -> float:
        lower_url = url.lower()
        matches = sum(1 for keyword in self.keywords if keyword.lower() in lower_url)
        if not self.keywords:
            return 0.0 
        return matches / len(self.keywords)  
