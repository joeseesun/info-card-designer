#!/usr/bin/env python3
"""
Smart split for info card images.
- Only splits if height > min_total (default 1400px)
- Finds natural break points (background-color rows) instead of hard-cutting
- Never cuts through text
Usage: python3 split_card.py <image_path> [max_slice=1200] [min_total=1400]
"""

import sys
import os
import numpy as np
from PIL import Image


def find_break_points(img_array, bg_color, max_slice=1200, min_slice=600):
    """Find rows that are entirely background color (natural gaps between content).
    Returns list of y-positions to split at."""
    height = img_array.shape[0]

    # Find rows where all pixels match background color (with tolerance)
    tolerance = 15
    if len(img_array.shape) == 3:
        # RGB/RGBA image
        diff = np.abs(img_array[:, :, :3].astype(int) - np.array(bg_color[:3]).astype(int))
        is_bg_row = np.all(diff <= tolerance, axis=(1, 2))
    else:
        diff = np.abs(img_array.astype(int) - bg_color[0])
        is_bg_row = np.all(diff <= tolerance, axis=1)

    # Find contiguous runs of background rows (gaps between content)
    # A gap must be at least 8px tall to count as a natural break
    min_gap = 8
    gaps = []
    in_gap = False
    gap_start = 0

    for y in range(height):
        if is_bg_row[y]:
            if not in_gap:
                in_gap = True
                gap_start = y
        else:
            if in_gap:
                gap_len = y - gap_start
                if gap_len >= min_gap:
                    # Use the middle of the gap as the break point
                    gaps.append((gap_start + gap_len // 2, gap_len))
                in_gap = False

    # Now pick break points that keep slices between min_slice and max_slice
    break_points = []
    last_break = 0

    for gap_y, gap_len in gaps:
        distance = gap_y - last_break
        if distance >= max_slice:
            # We've gone too far, find the best gap before this point
            # Look back for the closest gap that's within range
            best = None
            for gy, gl in gaps:
                d = gy - last_break
                if min_slice <= d <= max_slice:
                    best = gy
            if best:
                break_points.append(best)
                last_break = best
            else:
                # No good gap found, use this one even if it's a bit over
                break_points.append(gap_y)
                last_break = gap_y
        elif distance >= min_slice and gap_y + min_slice >= height:
            # Near the end, and we have enough for a decent slice
            break_points.append(gap_y)
            last_break = gap_y

    return break_points


def detect_bg_color(img):
    """Detect background color by sampling corners."""
    pixels = []
    w, h = img.size
    for x, y in [(5, 5), (w-5, 5), (5, h-5), (w-5, h-5)]:
        pixels.append(img.getpixel((x, y)))
    # Most common corner pixel
    from collections import Counter
    return Counter(pixels).most_common(1)[0][0]


def split_card(image_path, max_slice=1200, min_total=1400):
    img = Image.open(image_path)
    width, height = img.size

    if height <= min_total:
        print(f"No split needed ({height}px ≤ {min_total}px threshold)")
        return [image_path]

    base_dir = os.path.dirname(image_path)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    # Remove existing -N suffix if re-splitting
    if base_name.endswith(("-1", "-2", "-3", "-4", "-5")):
        base_name = base_name[:-2]

    bg_color = detect_bg_color(img)
    img_array = np.array(img)

    break_points = find_break_points(img_array, bg_color, max_slice=max_slice)

    if not break_points:
        print(f"No natural break points found, keeping as single image")
        return [image_path]

    # Create slices
    cuts = [0] + break_points + [height]
    parts = []

    for i in range(len(cuts) - 1):
        top = cuts[i]
        bottom = cuts[i + 1]
        slice_h = bottom - top

        # Skip tiny trailing slices (< 200px)
        if slice_h < 200 and i == len(cuts) - 2:
            # Merge with previous slice
            if parts:
                prev_path = parts[-1]
                prev_top = cuts[i - 1]
                cropped = img.crop((0, prev_top, width, bottom))
                cropped.save(prev_path, "PNG")
                print(f"  Updated: {prev_path} ({bottom - prev_top}px, merged tiny tail)")
                continue

        cropped = img.crop((0, top, width, bottom))
        out_path = os.path.join(base_dir, f"{base_name}-{i+1}.png")
        cropped.save(out_path, "PNG")
        parts.append(out_path)
        print(f"  Saved: {out_path} ({slice_h}px)")

    return parts


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: split_card.py <image_path> [max_slice=1200] [min_total=1400]")
        sys.exit(1)

    path = sys.argv[1]
    max_s = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    min_t = int(sys.argv[3]) if len(sys.argv) > 3 else 1400
    result = split_card(path, max_s, min_t)
    print(f"\nResult: {len(result)} file(s)")
    for p in result:
        print(f"  {p}")
