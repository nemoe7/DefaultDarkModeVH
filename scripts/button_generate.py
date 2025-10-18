from pathlib import Path
from PIL import Image
import random

_ASSETS_DIR = Path(__file__).parent / "assets"

random.seed(1)

def rotate_180(image: Image.Image) -> Image.Image:
  return image.rotate(180)

def flip_horizontal(image: Image.Image) -> Image.Image:
  return image.transpose(Image.FLIP_LEFT_RIGHT)

def flip_vertical(image: Image.Image) -> Image.Image:
  return image.transpose(Image.FLIP_TOP_BOTTOM)

def generate_button(template_filename, width, height, suffix="", bottom_border=2):
  # Load the template image
  template = Image.open(_ASSETS_DIR / template_filename)

  # Create a new image with the desired dimensions
  button = Image.new("RGB", (width, height), (0, 0, 0))

  # Get color of outer border
  box = template.crop((0, 0, 1, 1))

  # Get inner border tiles
  border_top = template.crop((1, 1, template.width - 2, 2))
  border_top_right = template.crop((template.width - 2, 1, template.width - 1, 2))
  border_bottom = template.crop((2, template.height - 3, template.width - 1, template.height - 1))
  border_bottom_left = template.crop((1, template.height - 3, 2, template.height - 1))
  border_left = template.crop((1, 2, 2, template.height - 3))
  border_right = template.crop((template.width - 2, 2, template.width - 1, template.height - 3))

  # Get center
  center = template.crop((2, 2, template.width - 2, template.height - 3))

  # Construct image
  box = box.resize((width, height))
  button.paste(box, (0, 0, width, height))

  remaining = width - 2
  current = 1
  while (remaining > border_top.width):
    button.paste(border_top, (current, 1))
    remaining -= border_top.width
    current += border_top.width
    border_top = rotate_180(border_top)

  if remaining > 0:
    border_top = border_top.crop((0, 0, remaining, border_top.height))
    button.paste(border_top, (current, 1))

  button.paste(border_top_right, (width - 2, 1))

  remaining = width - 3
  current = 2
  while (remaining > border_bottom.width):
    button.paste(border_bottom, (current, height - 3))
    remaining -= border_bottom.width
    current += border_bottom.width
    border_bottom = rotate_180(border_bottom)
  if remaining > 0:
    border_bottom = border_bottom.crop((0, 0, remaining, border_bottom.height))
    button.paste(border_bottom, (current, height - 3))

  button.paste(border_bottom_left, (1, height - 3))

  remaining = height - 5
  current = 2
  while (remaining > border_left.height):
    button.paste(border_left, (1, current))
    remaining -= border_left.height
    current += border_left.height
    border_left = rotate_180(border_left)
  if remaining > 0:
    border_left = border_left.crop((0, 0, border_left.width, remaining))
    button.paste(border_left, (1, current))

  remaining = height - 5
  current = 2
  while (remaining > border_right.height):
    button.paste(border_right, (width - 2, current))
    remaining -= border_right.height
    current += border_right.height
    center = rotate_180(center)
  if remaining > 0:
    border_right = border_right.crop((0, 0, border_right.width, remaining))
    button.paste(border_right, (width - 2, current))

  remaining_height = height - 5
  current_y = 2
  while remaining_height > center.height:
    remaining_width = width - 4
    current_x = 2
    while remaining_width > center.width:
      button.paste(center, (current_x, current_y))
      remaining_width -= center.width
      current_x += center.width
      center = rotate_180(center)
    if remaining_width > 0:
      center_rem = center.crop((0, 0, remaining_width, center.height))
      button.paste(center_rem, (current_x, current_y))
    remaining_height -= center.height
    current_y += center.height
    center = flip_vertical(center)
  if remaining_height > 0:
    center_rem = center.crop((0, 0, center.width, remaining_height))
    remaining_width = width - 4
    current_x = 2
    while remaining_width > center.width:
      button.paste(center_rem, (current_x, current_y))
      remaining_width -= center_rem.width
      current_x += center_rem.width
      center_rem = rotate_180(center_rem)
    if remaining_width > 0:
      center_rem = center_rem.crop((0, 0, remaining_width, center_rem.height))
      button.paste(center_rem, (current_x, current_y))

  # Save the button image
  if width == height:
    filename = f"button/{width}/button_{width}{suffix}.png"
  else:
    filename = f"button/{width}_{height}/button_{width}_{height}{suffix}.png"
  if (not Path(_ASSETS_DIR / filename).exists()):
    Path(_ASSETS_DIR / filename).parent.mkdir(parents=True, exist_ok=True)
  button.save(_ASSETS_DIR / filename)
  print(f"Button saved to /assets/{filename}")
  return filename

# Example usage
# generate_button("button_template.png", width=100, height=100, bottom_border=2)
if __name__ == "__main__":
  import sys

  if len(sys.argv) < 2:
    print("Usage: python generate_button.py <width> [height]")
    sys.exit(1)

  width = int(sys.argv[1])
  height = int(sys.argv[2]) if len(sys.argv) > 2 else width

  template_list = [
    "",
    "_hover",
    "_inactive",
    "_bg"
  ]

  for template in template_list:
    generate_button(_ASSETS_DIR / "button" / "_template" / f"button_template{template}.png", width, height, template)
