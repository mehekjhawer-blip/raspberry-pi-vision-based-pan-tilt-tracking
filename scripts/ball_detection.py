import cv2
import numpy as np

IMAGE_PATH = "images/test_ball.jpg"

# Load the image
frame = cv2.imread(IMAGE_PATH)

if frame is None:
    raise SystemExit(
        f"ERROR: Could not load {IMAGE_PATH}. "
        "Run create_test_image.py first."
    )

height, width = frame.shape[:2]

# Centre of the image
frame_centre_x = width // 2
frame_centre_y = height // 2

# Convert BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Red occurs at both ends of the HSV hue range.
# These thresholds are initial values for our synthetic image.
lower_red_1 = np.array([0, 100, 80])
upper_red_1 = np.array([10, 255, 255])

lower_red_2 = np.array([170, 100, 80])
upper_red_2 = np.array([179, 255, 255])

mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)

mask = cv2.bitwise_or(mask1, mask2)

# Remove small noise
kernel = np.ones((5, 5), np.uint8)

mask = cv2.morphologyEx(
    mask,
    cv2.MORPH_OPEN,
    kernel
)

mask = cv2.morphologyEx(
    mask,
    cv2.MORPH_CLOSE,
    kernel
)

# Find contours
contours, _ = cv2.findContours(
    mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

if contours:
    # Select the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)

    if area > 100:
        x, y, w, h = cv2.boundingRect(largest_contour)

        ball_centre_x = x + w // 2
        ball_centre_y = y + h // 2

        # Draw bounding box
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Draw ball centre
        cv2.circle(
            frame,
            (ball_centre_x, ball_centre_y),
            5,
            (255, 255, 255),
            -1
        )

        # Draw image centre
        cv2.drawMarker(
            frame,
            (frame_centre_x, frame_centre_y),
            (255, 0, 0),
            cv2.MARKER_CROSS,
            20,
            2
        )

        # Calculate tracking error
        error_x = ball_centre_x - frame_centre_x
        error_y = ball_centre_y - frame_centre_y

        print("Ball detected!")
        print(f"Ball centre: ({ball_centre_x}, {ball_centre_y})")
        print(f"Image centre: ({frame_centre_x}, {frame_centre_y})")
        print(f"Horizontal error: {error_x} pixels")
        print(f"Vertical error: {error_y} pixels")
        print(f"Contour area: {area:.1f} pixels")

    else:
        print("No sufficiently large ball detected.")

else:
    print("No red ball detected.")

# Save results for inspection
cv2.imwrite("results/detection_result.jpg", frame)
cv2.imwrite("results/detection_mask.jpg", mask)

print("Annotated image: results/detection_result.jpg")
print("Detection mask: results/detection_mask.jpg")