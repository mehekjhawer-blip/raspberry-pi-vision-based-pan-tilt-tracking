import cv2
import numpy as np
from pathlib import Path

# Create a black image with resolution 640 x 480
height = 480
width = 640

image = np.zeros((height, width, 3), dtype=np.uint8)

# Draw a red ball
ball_center = (400, 200)
ball_radius = 35
ball_color = (0, 0, 255)  # Red in OpenCV's BGR format

cv2.circle(
    image,
    ball_center,
    ball_radius,
    ball_color,
    -1
)

# Save the image
output_path = Path("images/test_ball.jpg")
output_path.parent.mkdir(parents=True, exist_ok=True)

success = cv2.imwrite(str(output_path), image)

if success:
    print(f"Test image saved to: {output_path}")
    print(f"Image resolution: {width} x {height}")
    print(f"Ball centre: {ball_center}")
else:
    print("ERROR: Could not save test image.")