import requests
from .url_filter import URLFilter
import logging

class ContentTypeFilter(URLFilter):
    def __init__(self, contentType: str):
        self.contentType = contentType.lower()  # Convert to lowercase during initialization
    
    def apply(self, url: str) -> bool:
        try:
            # Send a HEAD request to avoid downloading the entire content
            response = requests.head(url, timeout=5)
            if 'Content-Type' in response.headers:
                # Perform case-insensitive comparison
                if self.contentType in response.headers['Content-Type'].lower():
                    return True
                else:
                    logging.info(f"Skipping {url} as per content type filter")
                    return False
            
        except requests.RequestException as e:
            logging.error(f"Error checking content type for {url}: {e} in content type filter")
        return False
