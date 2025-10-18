# scripts/extract_all_assets.py
import os
import zipfile
import shutil
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

# assets_util helpers
from scripts.assets_util import path as asset_path, exists as asset_exists

# Directories (under scripts/assets/)
_JARS_DIR = asset_path("jars")
_EXTRACTED_DIR = asset_path("extracted_assets")
_DUPE_DIR = asset_path("dupe_assets")

# Shared state to coordinate duplicates across threads
_extracted_paths = set()      # set[str] of relative asset paths like "assets/foo/bar.png"
_extracted_paths_lock = threading.Lock()

def _write_zip_member_to(path_target: Path, zf: zipfile.ZipFile, member_name: str):
  """Write a single zip member to disk ensuring parent dirs exist."""
  path_target.parent.mkdir(parents=True, exist_ok=True)
  with zf.open(member_name) as src, open(path_target, "wb") as dst:
    shutil.copyfileobj(src, dst)

def extract_jar_assets(jar_path: Path):
  """
  Extract only entries under assets/ from jar_path.

  - First occurrence of a relative path goes to _EXTRACTED_DIR/<relative path>
  - Subsequent occurrences go to _DUPE_DIR/<jar_name>/<relative path>
  """
  extracted_members = []
  try:
    with zipfile.ZipFile(jar_path, "r") as zf:
      for info in zf.infolist():
        name = info.filename
        # only consider file entries inside 'assets/' (skip directories)
        if not name.startswith("assets/"):
          continue
        if name.endswith("/"):
          continue

        # normalize the relative path string (keep forward-slash form)
        rel = name

        # decide target atomically
        with _extracted_paths_lock:
          is_first = rel not in _extracted_paths
          if is_first:
            _extracted_paths.add(rel)

        if is_first:
          target = _EXTRACTED_DIR / rel
        else:
          # duplicate -> preserve jar folder structure under dupe_assets/<jar>/
          target = _DUPE_DIR / jar_path.stem / rel

        try:
          _write_zip_member_to(target, zf, name)
          extracted_members.append(str(rel))
        except Exception as e:
          # best-effort: report and continue
          print(f"[{jar_path.name}] failed to extract {name}: {e}")

  except zipfile.BadZipFile:
    print(f"Bad JAR (not a zip): {jar_path}")
  except Exception as e:
    print(f"Error processing {jar_path}: {e}")

  return { "jar": jar_path.name, "count": len(extracted_members) }

def main():
  if not asset_exists("jars"):
    raise FileNotFoundError(f"JAR folder not found: {_JARS_DIR}")

  jars = list(_JARS_DIR.rglob("*.jar"))
  if not jars:
    print("No .jar files found under:", _JARS_DIR)
    return

  _EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
  _DUPE_DIR.mkdir(parents=True, exist_ok=True)

  max_workers = os.cpu_count() or 4
  results = []

  with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = { executor.submit(extract_jar_assets, jar): jar for jar in jars }

    for future in tqdm(as_completed(futures), total=len(futures), desc="Extracting jars"):
      jar = futures[future]
      try:
        res = future.result()
        results.append(res)
      except Exception as e:
        print(f"Error extracting {jar.name}: {e}")

  # summary
  total_files = sum(r["count"] for r in results)
  print(f"\nDone. JARs processed: {len(results)}. Files extracted: {total_files}")
  print(f"Primary output: {_EXTRACTED_DIR}")
  print(f"Duplicates: {_DUPE_DIR}")

if __name__ == "__main__":
  main()
