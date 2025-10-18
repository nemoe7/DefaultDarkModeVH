# scripts/lut_extrapolate.py
from pathlib import Path
import numpy as np
from tqdm import tqdm
from scipy.spatial import cKDTree

_ASSETS_DIR = Path(__file__).parent / "assets"

def extrapolate_lut(sparse_npy, out_npy, chunk_size=500_000):
  """
  Extrapolate a small LUT (dict or partial array) to a full 256x256x256 LUT array.
  - Uses neighbor averaging for empty points.
  - Restores original LUT points exactly at the end.
  - sparse_npy: path to the input sparse LUT (.npy)
  - out_npy: path to save the full LUT
  - chunk_size: how many points to process per loop (memory-friendly)
  - k: number of nearest neighbors for averaging
  """
  lut_data = np.load(_ASSETS_DIR / sparse_npy, allow_pickle=True).item()

  # If it's already a full array, just copy
  if isinstance(lut_data, np.ndarray) and lut_data.shape == (256, 256, 256, 3):
    print("Input is already a full LUT. Copying...")
    np.save(_ASSETS_DIR / out_npy, lut_data)
    return out_npy

  # Convert dict to arrays
  colors = np.array(list(lut_data.keys()), dtype=np.float32)
  mapped = np.array(list(lut_data.values()), dtype=np.float32)
  k = len(colors)

  # Build KD-tree for nearest neighbor lookup
  tree = cKDTree(colors)

  # Use int16 to mark empty positions (-1)
  full_lut = np.full((256, 256, 256, 3), -1, dtype=np.int16)

  # Flatten LUT coordinates
  coords = np.indices((256, 256, 256)).reshape(3, -1).T

  print("Extrapolating LUT...")
  for start in tqdm(range(0, len(coords), chunk_size)):
    end = min(start + chunk_size, len(coords))
    chunk = coords[start:end]

    # Only extrapolate positions where full_lut is -1
    mask = (full_lut[chunk[:,0], chunk[:,1], chunk[:,2], 0] == -1)
    if not np.any(mask):
      continue

    to_fill = chunk[mask]
    dists, idxs = tree.query(to_fill, k=k, workers=-1)

    if k == 1:
      full_lut[to_fill[:,0], to_fill[:,1], to_fill[:,2]] = mapped[idxs]
    else:
      avg_colors = mapped[idxs].mean(axis=1)
      full_lut[to_fill[:,0], to_fill[:,1], to_fill[:,2]] = avg_colors.astype(np.int16)

  # Restore original LUT points exactly
  for o, d in zip(colors, mapped):
    r, g, b = o.astype(int)
    full_lut[r, g, b] = d.astype(np.int16)

  # Convert back to uint8 for saving
  full_lut = full_lut.astype(np.uint8)
  np.save(_ASSETS_DIR / out_npy, full_lut)
  print(f"Full LUT saved to /assets/{out_npy}")
  return out_npy


if __name__ == "__main__":
  import sys

  if len(sys.argv) < 2:
    print("Usage: python lut_extrapolate.py <sparse_npy> [<out_npy>]")
    sys.exit(1)

  sparse_npy = sys.argv[1]
  out_npy = (
    sys.argv[2] if len(sys.argv) >= 3
    else Path(sparse_npy).stem + "_ext.npy"
  )

  extrapolate_lut(sparse_npy, out_npy)
