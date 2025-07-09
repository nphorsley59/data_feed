from enum import Enum
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


class Directory(str, Enum):
    PACKAGE_ROOT = BASE_DIR / "data_feed"
    CACHE = PACKAGE_ROOT / "cache"
