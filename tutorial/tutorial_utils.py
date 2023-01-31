import os
from urllib.request import urlretrieve


def setup():
    """Download the tutorial database if it doesn't already exist"""
    if not os.path.exists("geography.db"):
        urlretrieve(
            "https://storage.googleapis.com/ibis-tutorial-data/geography.db",
            "geography.db"
        )
