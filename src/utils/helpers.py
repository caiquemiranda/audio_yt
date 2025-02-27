import os

def get_default_download_path() -> str:
    return os.path.join(os.path.expanduser("~"), "Downloads") 