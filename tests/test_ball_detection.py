import sys
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

# Import the detector's image-processing dependencies.
import numpy as np


def detect_ball(image):
    """Detect a red ball and return its bounding-box centre."""

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red_1 = np.array([0, 100, 80])
    upper_red_1 = np.array([10, 255, 255])

    lower_red_2 = np.array([170, 100, 80])
    upper_red_2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)

    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, kernel
    )

    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE, kernel
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    if not contours:
        return None

    contour = max(contours, key=cv2.contourArea)

    if cv2.contourArea(contour) <= 100:
        return None

    x, y, w, h = cv2.boundingRect(contour)

    return (x + w // 2, y + h // 2)


def main():
    image_dir = ROOT / "images"

    test_names = [
        "left",
        "right",
        "top",
        "bottom",
        "centre",
        "top_left",
        "bottom_right",
    ]

    passed = 0

    for name in test_names:
        path = image_dir / f"ball_{name}.jpg"
        image = cv2.imread(str(path))

        if image is None:
            print(f"FAIL: Could not load {path}")
            continue

        centre = detect_ball(image)

        if centre is None:
            print(f"FAIL: Ball not detected in {name}")
            continue

        print(f"PASS: {name:14s} detected at {centre}")
        passed += 1

    print(f"\nResults: {passed}/{len(test_names)} tests passed")

    if passed != len(test_names):
        raise SystemExit(1)


if __name__ == "__main__":
    main()