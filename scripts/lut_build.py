# scripts/lut_build.py
from pathlib import Path
import numpy as np
from PIL import Image
from tqdm import tqdm

_ASSETS_DIR = Path(__file__).parent / "assets"

def build_lut_anysize(original_path, darkened_path, out_npy, use_full_array_threshold=16_777_216):
  """
  Build a LUT from arbitrary-size images.
  - Stores a dict for small images (unique colors)
  - Stores a full 256x256x256x3 array for large LUTs
  - Fully transparent pixels (alpha == 0) are ignored
  """
  # Load as RGBA to detect transparency
  original_img = Image.open(original_path).convert("RGBA")
  darkened_img = Image.open(darkened_path).convert("RGBA")

  orig = np.array(original_img, dtype=np.uint8)
  dark = np.array(darkened_img, dtype=np.uint8)

  if orig.shape != dark.shape:
    raise ValueError(f"Original and darkened images must have the same dimensions. Got {orig.shape} and {dark.shape}")

  # Flatten
  orig_flat = orig.reshape(-1, 4)  # RGBA
  dark_flat = dark.reshape(-1, 4)

  # Filter out fully transparent pixels
  mask = orig_flat[:, 3] != 0  # alpha != 0
  orig_rgb = orig_flat[mask][:, :3]  # drop alpha
  dark_rgb = dark_flat[mask][:, :3]

  num_pixels = len(orig_rgb)
  print(f"Total pixels: {len(orig_flat)}, Used (non-transparent): {num_pixels}")

  # Decide storage method
  if num_pixels < use_full_array_threshold:
    print("Building LUT as a dict (unique colors only)...")
    lut_dict = {}
    for o, d in tqdm(zip(orig_rgb, dark_rgb), total=num_pixels):
      lut_dict[tuple(o)] = tuple(d)
    np.save(_ASSETS_DIR / out_npy, lut_dict)
    print(f"LUT dict saved with {len(lut_dict)} unique colors to /assets/{out_npy}")
  else:
    print("Building full 256x256x256 LUT array...")
    lut_array = np.zeros((256, 256, 256, 3), dtype=np.uint8)
    for o, d in tqdm(zip(orig_rgb, dark_rgb), total=num_pixels):
      r, g, b = o
      lut_array[r, g, b] = d
    np.save(_ASSETS_DIR / out_npy, lut_array)
    print(f"Full LUT array saved to /assets/{out_npy}")

  return out_npy

if __name__ == "__main__":
  import sys

  if len(sys.argv) < 3:
    print("Usage: python lut_build.py <original_image> <transformed_image> [<out_npy>]")
    sys.exit(1)

  original_image = sys.argv[1]
  transformed_image = sys.argv[2]
  if len(sys.argv) == 4:
    out_npy = sys.argv[3]
    if not out_npy.endswith(".npy"):
      out_npy += ".npy"
  else:
    out_npy = "lut_" + Path(original_image).stem + "_" + Path(transformed_image).stem + ".npy"

  build_lut_anysize(original_image, transformed_image, out_npy)
