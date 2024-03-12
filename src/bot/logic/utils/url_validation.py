from urllib.request import urlopen


def url_validation(url: str) -> bool:
    try:
        urlopen(url)
    except Exception:
        return False
    return True
