import requests
from .url_filter import URLFilter

class SizeFilter(URLFilter):
    def __init__(self, min_size: int, max_size: int):
        self.min_size = min_size
        self.max_size = max_size

    def apply(self, url: str) -> bool:
        try:
            response = requests.head(url, timeout=5)
            if 'Content-Length' in response.headers:
                content_length = int(response.headers['Content-Length'])
                return self.min_size <= content_length <= self.max_size
        except requests.RequestException as e:
            print(f"Error checking content size for {url}: {e}")
        return False