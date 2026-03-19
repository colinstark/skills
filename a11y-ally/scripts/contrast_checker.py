"""
WCAG3 APCA Contrast Checker

Implements the Accessible Perceptual Contrast Algorithm (APCA) v0.0.98G-4g
for evaluating color contrast according to WCAG3 guidelines.

Reference: https://github.com/Myndex/apca-w3
"""

import re
import math
from typing import Tuple, Union


_SA98G = {
    "mainTRC": 2.4,
    "sRco": 0.2126729,
    "sGco": 0.7151522,
    "sBco": 0.0721750,
    "normBG": 0.56,
    "normTXT": 0.57,
    "revTXT": 0.62,
    "revBG": 0.65,
    "blkThrs": 0.022,
    "blkClmp": 1.414,
    "scaleBoW": 1.14,
    "scaleWoB": 1.14,
    "loBoWoffset": 0.027,
    "loWoBoffset": 0.027,
    "deltaYmin": 0.0005,
    "loClip": 0.1,
}


def _parse_hex(color: str) -> Tuple[int, int, int, float]:
    hex_match = re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color.strip())
    if not hex_match:
        raise ValueError(f"Invalid hex color: {color}")

    hex_val = hex_match.group(1)
    if len(hex_val) == 3:
        r, g, b = (int(c * 2, 16) for c in hex_val)
    else:
        r, g, b = int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16)

    return (r, g, b, 1.0)


def _parse_rgba(color: str) -> Tuple[int, int, int, float]:
    rgba_match = re.match(
        r"^rgba?\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*([01]?\.?\d*))?\s*\)$",
        color.strip(),
        re.IGNORECASE,
    )
    if not rgba_match:
        raise ValueError(f"Invalid rgba color: {color}")

    r, g, b = (
        int(rgba_match.group(1)),
        int(rgba_match.group(2)),
        int(rgba_match.group(3)),
    )
    a = float(rgba_match.group(4)) if rgba_match.group(4) is not None else 1.0

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    a = max(0.0, min(1.0, a))

    return (r, g, b, a)


def parse_color(color: str) -> Tuple[int, int, int, float]:
    """
    Parse a color string into RGBA tuple.

    Supports:
    - #RGB
    - #RRGGBB
    - rgb(r, g, b)
    - rgba(r, g, b, a)

    Returns: (r, g, b, a) tuple where r,g,b are 0-255 and a is 0.0-1.0
    """
    color = color.strip()

    if color.startswith("#"):
        return _parse_hex(color)
    elif color.lower().startswith("rgb"):
        return _parse_rgba(color)
    else:
        raise ValueError(f"Unsupported color format: {color}")


def alpha_blend(
    fg: Tuple[int, int, int, float], bg: Tuple[int, int, int, float]
) -> Tuple[int, int, int, float]:
    """
    Blend foreground color with background using alpha channel.
    Blending is done in gamma-encoded space (standard web approach).
    """
    alpha = max(0.0, min(1.0, fg[3]))
    comp_blend = 1.0 - alpha

    r = round(bg[0] * comp_blend + fg[0] * alpha)
    g = round(bg[1] * comp_blend + fg[1] * alpha)
    b = round(bg[2] * comp_blend + fg[2] * alpha)

    return (min(255, r), min(255, g), min(255, b), 1.0)


def srgb_to_y(rgb: Tuple[int, int, int, float]) -> float:
    """
    Convert sRGB color to luminance (Y).
    Uses APCA's modified luminance calculation with 2.4 exponent.
    """

    def linearize(channel: int) -> float:
        return math.pow(channel / 255.0, _SA98G["mainTRC"])

    return (
        _SA98G["sRco"] * linearize(rgb[0])
        + _SA98G["sGco"] * linearize(rgb[1])
        + _SA98G["sBco"] * linearize(rgb[2])
    )


def apca_contrast(txt_y: float, bg_y: float) -> float:
    """
    Calculate APCA contrast value between text and background luminance.

    IMPORTANT: Polarity matters! First argument is text, second is background.

    Returns: Signed Lc value (-106 to ~108)
    - Positive: dark text on light background
    - Negative: light text on dark background
    """
    if math.isnan(txt_y) or math.isnan(bg_y):
        return 0.0
    if min(txt_y, bg_y) < 0.0 or max(txt_y, bg_y) > 1.1:
        return 0.0

    if txt_y > _SA98G["blkThrs"]:
        txt_y_clamped = txt_y
    else:
        txt_y_clamped = txt_y + math.pow(_SA98G["blkThrs"] - txt_y, _SA98G["blkClmp"])

    if bg_y > _SA98G["blkThrs"]:
        bg_y_clamped = bg_y
    else:
        bg_y_clamped = bg_y + math.pow(_SA98G["blkThrs"] - bg_y, _SA98G["blkClmp"])

    if abs(bg_y_clamped - txt_y_clamped) < _SA98G["deltaYmin"]:
        return 0.0

    if bg_y_clamped > txt_y_clamped:
        sapc = (
            math.pow(bg_y_clamped, _SA98G["normBG"])
            - math.pow(txt_y_clamped, _SA98G["normTXT"])
        ) * _SA98G["scaleBoW"]

        if sapc < _SA98G["loClip"]:
            output = 0.0
        else:
            output = sapc - _SA98G["loBoWoffset"]
    else:
        sapc = (
            math.pow(bg_y_clamped, _SA98G["revBG"])
            - math.pow(txt_y_clamped, _SA98G["revTXT"])
        ) * _SA98G["scaleWoB"]

        if sapc > -_SA98G["loClip"]:
            output = 0.0
        else:
            output = sapc + _SA98G["loWoBoffset"]

    return output * 100.0


def get_contrast_value(foreground: str, background: str) -> float:
    """
    Calculate APCA contrast value between two colors.

    Args:
        foreground: Text/foreground color (with optional alpha)
        background: Background color

    Returns: Signed Lc contrast value
    """
    fg = parse_color(foreground)
    bg = parse_color(background)

    if fg[3] < 1.0:
        fg = alpha_blend(fg, bg)

    txt_y = srgb_to_y(fg)
    bg_y = srgb_to_y(bg)

    return apca_contrast(txt_y, bg_y)


def passes_contrast(foreground: str, background: str, threshold: float = 45.0) -> bool:
    """
    Check if two colors pass the WCAG3 APCA contrast threshold.

    Args:
        foreground: Text/foreground color (supports hex, rgb, rgba)
        background: Background color
        threshold: Minimum Lc contrast required (default: 45 for large text)

    Returns: True if contrast meets threshold, False otherwise

    Threshold Guidelines:
        - Lc 45: Minimum for large/bold text (~3:1 in WCAG 2)
        - Lc 60: Minimum for body text (~4.5:1 in WCAG 2)
        - Lc 75: Preferred for body text
        - Lc 90: Enhanced readability
    """
    contrast = get_contrast_value(foreground, background)
    return abs(contrast) >= threshold


if __name__ == "__main__":
    test_cases = [
        ("#333333", "#ffffff", 45),
        ("#777777", "#ffffff", 45),
        ("#000000", "#ffffff", 45),
        ("rgba(0,0,0,0.5)", "#ffffff", 45),
        ("#ff0000", "#0000ff", 45),
        ("#888888", "#ffffff", 60),
    ]

    print("WCAG3 APCA Contrast Checker Tests\n")
    print(f"{'Foreground':<25} {'Background':<15} {'Lc Value':>10} {'Passes?':>8}")
    print("-" * 65)

    for fg, bg, thresh in test_cases:
        lc = get_contrast_value(fg, bg)
        passed = passes_contrast(fg, bg, thresh)
        print(f"{fg:<25} {bg:<15} {lc:>10.1f} {str(passed):>8}")
