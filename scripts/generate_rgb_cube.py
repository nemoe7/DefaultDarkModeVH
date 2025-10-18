import numpy as np
from PIL import Image

def generate_full_rgb_proper(output="rgb_full_4096.png"):
  width, height = 4096, 4096
  total_pixels = width * height  # 16,777,216

  # Create flat array of sequential numbers 0 .. 16,777,215
  i = np.arange(total_pixels, dtype=np.uint32)

  # Extract R,G,B
  r = (i % 256).astype(np.uint8)
  g = ((i // 256) % 256).astype(np.uint8)
  b = ((i // 65536) % 256).astype(np.uint8)

  # Stack and reshape to image
  img_array = np.stack((r, g, b), axis=-1).reshape((height, width, 3))

  Image.fromarray(img_array, mode="RGB").save(output)
  print(f"Saved: {output}")

generate_full_rgb_proper()
