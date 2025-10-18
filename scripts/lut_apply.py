# scripts/lut_apply.py
from pathlib import Path
import numpy as np
from PIL import Image
from tqdm import tqdm

_ASSETS_DIR = Path(__file__).parent / "assets"

def apply_lut_to_image(input_path, lut_path):
  """Apply a LUT (dict or full array) to an image efficiently, preserving transparency."""
  img = Image.open(input_path).convert("RGBA")  # KEEP alpha
  arr = np.array(img, dtype=np.uint8)

  h, w, _ = arr.shape
  rgb_flat = arr[..., :3].reshape(-1, 3)  # only apply LUT to RGB
  alpha_flat = arr[..., 3].reshape(-1)    # store alpha separately

  # Load LUT
  lut_data = np.load(Path(lut_path).resolve(), allow_pickle=True)

  # Detect LUT type
  if isinstance(lut_data, dict):
    lut_dict = lut_data
    use_dict = True
  elif isinstance(lut_data, np.ndarray) and lut_data.dtype == object and lut_data.shape == ():  # 0-dim object array
    lut_dict = lut_data.item()
    if not isinstance(lut_dict, dict):
      raise ValueError("Loaded object array does not contain a dict")
    use_dict = True
  elif isinstance(lut_data, np.ndarray) and lut_data.shape == (256, 256, 256, 3):
    lut_array = lut_data
    use_dict = False
  else:
    raise ValueError("Unsupported LUT format. Must be a dict or full 256x256x256 array.")

  # Apply LUT
  if use_dict:
    # Vectorized dict mapping
    keys = [tuple(px) for px in rgb_flat]
    mapped_rgb = np.array([lut_dict.get(k, k) for k in tqdm(keys, desc="Applying LUT")], dtype=np.uint8)
  else:
    r, g, b = rgb_flat[:,0], rgb_flat[:,1], rgb_flat[:,2]
    mapped_rgb = lut_array[r, g, b]

  # Restore alpha channel
  out_img = np.zeros((h * w, 4), dtype=np.uint8)
  out_img[:, :3] = mapped_rgb
  out_img[:, 3] = alpha_flat

  out_img = out_img.reshape(h, w, 4)

  output_path = Path(input_path).with_name(Path(input_path).stem + "_" + Path(lut_path).stem + ".png")
  Image.fromarray(out_img).save(output_path)
  print(f"Saved transformed image to {output_path}")


if __name__ == "__main__":
  import sys

  if len(sys.argv) < 2:
    print("Usage: python lut_apply.py <input_image> [input_image_2] ...")
    sys.exit(1)

  input_npy = input("Enter the path to the LUT file: ").strip()
  if not input_npy:
    input_npy = _ASSETS_DIR / "lut_150.npy"
  elif not input_npy.lower().startswith("c:"):
    if not input_npy.endswith(".npy") == ".npy":
      input_npy += ".npy"
    input_npy = _ASSETS_DIR / input_npy

  input_npy = Path(input_npy).resolve()

  if not input_npy.exists():
    print(f"File not found: {input_npy}")
    sys.exit(1)

  for input_image in sys.argv[1:]:
    apply_lut_to_image(input_image, input_npy)
