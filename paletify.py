from PIL import Image
import numpy as np


def hex_to_rgb(hex_color):
    hex_color = hex_color.strip("#").strip()
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color code: '{hex_color}'")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def find_closest_palette_color(color, palette):
    palette = np.array(palette)
    original_alpha = (
        color[3] if len(color) == 4 else 255
    )  # Preserve original alpha, default to 255 (opaque) if not present
    color = np.array(color[:3])  # Consider only RGB, ignore alpha
    distances = np.sqrt(np.sum((palette - color) ** 2, axis=1))
    closest_color_index = np.argmin(distances)
    return tuple(palette[closest_color_index]) + (
        original_alpha,
    )  # Add alpha value back


def palletify_image(image_path, palette_string):
    # Parse the palette string
    palette = [
        hex_to_rgb(color.strip())
        for color in palette_string.split("\n")
        if color.strip().startswith("#")
    ]

    with Image.open(image_path) as img:
        img = img.convert("RGBA")  # Convert to RGBA
        pixels = np.array(img)

        # Apply the palette
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                closest_color = find_closest_palette_color(pixels[i, j], palette)
                pixels[i, j] = closest_color

        # Create and save the new image
        new_img = Image.fromarray(pixels.astype("uint8"), "RGBA")
        new_img.save("palletified_image.png")


# Your color palette as a multiline string
palette_string = """
# 1a1c2c
# 5d275d
# b13e53
# ef7d57
# ffcd75
# a7f070
# 38b764
# 257179
# 29366f
# 3b5dc9
# 41a6f6
# 73eff7
# f4f4f4
# 94b0c2
# 566c86
# 333c57
"""


# get path from input arg
import sys

if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    print("No image path given, using default")


palletify_image(image_path, palette_string)
