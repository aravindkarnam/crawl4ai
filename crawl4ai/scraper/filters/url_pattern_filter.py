import re
from .url_filter import URLFilter
from re import Pattern
import logging

class URLPatternFilter(URLFilter):
    def __init__(self, pattern: Pattern):
        self.pattern = pattern
    
    def apply(self, url: str) -> bool:
        # Use re.match to see if the URL matches the pattern
        if bool(re.match(self.pattern, url)):
            return True
        else:
            logging.info(f"Skipping {url} as per pattern filter")
            return False
    
