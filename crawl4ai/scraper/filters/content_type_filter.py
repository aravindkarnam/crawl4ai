import requests
from .url_filter import URLFilter

class ContentTypeFilter(URLFilter):
    def __init__(self, contentType: str):
        self.contentType = contentType.lower()  # Convert to lowercase during initialization
    
    def apply(self, url: str) -> bool:
        try:
            # Send a HEAD request to avoid downloading the entire content
            response = requests.head(url, timeout=5)
            if 'Content-Type' in response.headers:
                # Perform case-insensitive comparison
                return self.contentType in response.headers['Content-Type'].lower()
        except requests.RequestException as e:
            print(f"Error checking content type for {url}: {e}")
        return False
