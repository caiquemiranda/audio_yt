from urllib.parse import urlparse

class URLValidator:
    @staticmethod
    def is_valid_youtube_url(url: str) -> bool:
        try:
            parsed_url = urlparse(url)
            return 'youtube.com' in parsed_url.netloc or 'youtu.be' in parsed_url.netloc
        except:
            return False 