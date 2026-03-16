#!/usr/bin/env python3
"""
Split a tall info card image into multiple equal-height slices.
Usage: python3 split_card.py <image_path> [max_height=1200]
Output: card-1.png, card-2.png, ... in same directory as input
"""

import sys
import os
from PIL import Image


def split_card(image_path, max_height=1200):
    img = Image.open(image_path)
    width, height = img.size

    if height <= max_height:
        print(f"No split needed ({height}px ≤ {max_height}px)")
        return [image_path]

    base_dir = os.path.dirname(image_path)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    # Remove existing -N suffix if re-splitting
    if base_name.endswith(("-1", "-2", "-3", "-4")):
        base_name = base_name[:-2]

    num_parts = (height + max_height - 1) // max_height
    # Distribute height evenly to avoid a tiny last slice
    slice_height = height // num_parts

    parts = []
    for i in range(num_parts):
        top = i * slice_height
        bottom = height if i == num_parts - 1 else (i + 1) * slice_height
        cropped = img.crop((0, top, width, bottom))
        out_path = os.path.join(base_dir, f"{base_name}-{i+1}.png")
        cropped.save(out_path, "PNG")
        parts.append(out_path)
        print(f"  Saved: {out_path} ({bottom - top}px)")

    return parts


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: split_card.py <image_path> [max_height=1200]")
        sys.exit(1)

    path = sys.argv[1]
    max_h = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    result = split_card(path, max_h)
    print(f"\nResult: {len(result)} file(s)")
    for p in result:
        print(f"  {p}")
