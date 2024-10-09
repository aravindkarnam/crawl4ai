from datetime import datetime
import requests
from .url_filter import URLFilter

class DateFilter(URLFilter):
    def __init__(self, min_date: datetime, max_date: datetime):
        self.min_date = min_date
        self.max_date = max_date

    def apply(self, url: str) -> bool:
        try:
            response = requests.head(url, timeout=5)
            if 'Last-Modified' in response.headers:
                last_modified = datetime.strptime(response.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S GMT')
                return self.min_date <= last_modified <= self.max_date
        except requests.RequestException as e:
            print(f"Error checking last-modified date for {url}: {e}")
        return False