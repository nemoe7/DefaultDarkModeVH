# scripts/assets_util.py
from pathlib import Path
from typing import List, Union
from PIL import Image, ImageFile

# Resolve the directory of this file
_BASE_DIR = Path(__file__).resolve().parent
_ASSETS_DIR = _BASE_DIR / "assets"

if not _ASSETS_DIR.exists():
  raise FileNotFoundError(f"Assets folder not found: {_ASSETS_DIR}")

def path(filename: Union[str, Path]) -> Path:
  """Return full path to a file in the assets folder."""
  return _ASSETS_DIR / filename

def load_image(filename: Union[str, Path]) -> ImageFile:
  """Load and return an image from assets."""
  return Image.open(path(filename))

def list(pattern: str = "*") -> List[Path]:
  """List asset files with optional glob pattern."""
  return [p for p in _ASSETS_DIR.glob(pattern) if p.is_file()]

def exists(filename: Union[str, Path]) -> bool:
  """Check if a file exists in the assets folder."""
  return (_ASSETS_DIR / filename).exists()
