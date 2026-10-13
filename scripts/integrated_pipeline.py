import sys
import time
from pathlib import Path

import cv2
import numpy as np

# Allow imports from the scripts directory.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tracking_controller import PanTiltController


# Configuration
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

CENTRE_X = IMAGE_WIDTH // 2
CENTRE_Y = IMAGE_HEIGHT // 2

IMAGE_DIR = ROOT / "images"
RESULTS_DIR = ROOT / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def detect_ball(frame):
    """
    Detect the largest sufficiently large red object.

    Returns:
        (centre_x, centre_y) if detected, otherwise None.
    """

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red occupies both ends of the HSV hue range.
    lower_red_1 = np.array([0, 100, 80])
    upper_red_1 = np.array([10, 255, 255])

    lower_red_2 = np.array([170, 100, 80])
    upper_red_2 = np.array([179, 255, 255])

    mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)

    mask = cv2.bitwise_or(mask_1, mask_2)

    # Remove small noise and fill small gaps.
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

    x, y, width, height = cv2.boundingRect(contour)

    centre_x = x + width // 2
    centre_y = y + height // 2

    return (centre_x, centre_y)


def main():
    controller = PanTiltController()

    test_images = [
        "ball_left.jpg",
        "ball_top_left.jpg",
        "ball_top.jpg",
        "ball_centre.jpg",
        "ball_right.jpg",
        "ball_bottom_right.jpg",
        "ball_bottom.jpg",
    ]

    print("INTEGRATED BALL-TRACKING SIMULATION")
    print("=" * 82)

    print(
        f"{'Image':<24}"
        f"{'Ball centre':<18}"
        f"{'Error X':<12}"
        f"{'Error Y':<12}"
        f"{'Pan':<8}"
        f"{'Tilt':<8}"
    )

    print("-" * 82)

    total_time = 0.0
    processed = 0

    for image_name in test_images:
        image_path = IMAGE_DIR / image_name

        frame = cv2.imread(str(image_path))

        if frame is None:
            print(f"WARNING: Cannot load {image_path}")
            continue

        start_time = time.perf_counter()

        ball_centre = detect_ball(frame)

        if ball_centre is not None:
            ball_x, ball_y = ball_centre

            error_x = ball_x - CENTRE_X
            error_y = ball_y - CENTRE_Y

            pan, tilt = controller.update(error_x, error_y)

            # Draw the detected ball.
            cv2.rectangle(
                frame,
                (ball_x - 30, ball_y - 30),
                (ball_x + 30, ball_y + 30),
                (0, 255, 0),
                2,
            )

            cv2.circle(
                frame,
                ball_centre,
                5,
                (255, 255, 255),
                -1,
            )

            # Draw the image centre.
            cv2.drawMarker(
                frame,
                (CENTRE_X, CENTRE_Y),
                (255, 0, 0),
                cv2.MARKER_CROSS,
                20,
                2,
            )

            cv2.putText(
                frame,
                f"Error: ({error_x}, {error_y})",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2,
            )

            output_path = RESULTS_DIR / (
                "integrated_" + image_name
            )

            cv2.imwrite(str(output_path), frame)

            centre_text = str(ball_centre)

        else:
            # Hold the previous angles if no ball is detected.
            pan, tilt = controller.update(
                0,
                0,
                target_found=False,
            )

            centre_text = "Not detected"
            error_x = None
            error_y = None

        elapsed = time.perf_counter() - start_time

        total_time += elapsed
        processed += 1

        error_x_text = (
            str(error_x) if error_x is not None else "-"
        )

        error_y_text = (
            str(error_y) if error_y is not None else "-"
        )

        print(
            f"{image_name:<24}"
            f"{centre_text:<18}"
            f"{error_x_text:<12}"
            f"{error_y_text:<12}"
            f"{pan:<8.2f}"
            f"{tilt:<8.2f}"
        )

    print("-" * 82)

    if processed:
        average_time_ms = (total_time / processed) * 1000

        print(f"Images processed: {processed}")
        print(
            f"Average processing time per image: "
            f"{average_time_ms:.3f} ms"
        )

        print(
            "Approximate processing rate: "
            f"{processed / total_time:.2f} images/second"
            if total_time > 0
            else "Processing rate unavailable"
        )

    print("\nIntegrated simulation completed.")
    print(f"Annotated images saved in: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
