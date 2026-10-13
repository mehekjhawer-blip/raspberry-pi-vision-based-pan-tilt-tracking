import csv
import time
from pathlib import Path

import cv2

from tracking_controller import PanTiltController

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images"
RESULTS_DIR = ROOT / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = RESULTS_DIR / "tracking_results.csv"

WIDTH = 640
HEIGHT = 480

CENTRE_X = WIDTH // 2
CENTRE_Y = HEIGHT // 2


def detect_ball(frame):
    import numpy as np

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower1 = np.array([0, 100, 80])
    upper1 = np.array([10, 255, 255])

    lower2 = np.array([170, 100, 80])
    upper2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)

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
    controller = PanTiltController()

    images = sorted(IMAGE_DIR.glob("ball_*.jpg"))

    if not images:
        print("No test images found.")
        print("Run scripts/generate_test_images.py first.")
        return

    rows = []
    absolute_errors = []

    for image_path in images:
        frame = cv2.imread(str(image_path))

        if frame is None:
            print(f"Skipping unreadable image: {image_path}")
            continue

        start = time.perf_counter()

        centre = detect_ball(frame)

        elapsed_ms = (time.perf_counter() - start) * 1000

        if centre is None:
            pan, tilt = controller.update(
                0, 0, target_found=False
            )

            error_x = None
            error_y = None

            print(f"{image_path.name}: no ball detected")

        else:
            ball_x, ball_y = centre

            error_x = ball_x - CENTRE_X
            error_y = ball_y - CENTRE_Y

            pan, tilt = controller.update(error_x, error_y)

            absolute_errors.append(
                (abs(error_x), abs(error_y))
            )

            print(
                f"{image_path.name}: "
                f"centre={centre}, "
                f"errors=({error_x}, {error_y}), "
                f"processing={elapsed_ms:.3f} ms"
            )

        rows.append([
            image_path.name,
            centre,
            error_x,
            error_y,
            f"{pan:.2f}",
            f"{tilt:.2f}",
            f"{elapsed_ms:.3f}",
        ])

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "image",
            "ball_centre",
            "error_x_pixels",
            "error_y_pixels",
            "simulated_pan_degrees",
            "simulated_tilt_degrees",
            "processing_time_ms",
        ])

        writer.writerows(rows)

    print(f"\nResults saved to: {OUTPUT_FILE}")

    if absolute_errors:
        mean_x = sum(x for x, _ in absolute_errors) / len(
            absolute_errors
        )

        mean_y = sum(y for _, y in absolute_errors) / len(
            absolute_errors
        )

        print(f"Mean absolute horizontal error: {mean_x:.2f} pixels")
        print(f"Mean absolute vertical error: {mean_y:.2f} pixels")


if __name__ == "__main__":
    main()