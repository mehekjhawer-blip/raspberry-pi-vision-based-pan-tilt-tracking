import cv2
import numpy as np
from pathlib import Path

output_dir = Path("images")
output_dir.mkdir(parents=True, exist_ok=True)

width = 640
height = 480
radius = 30

# Test the ball at different positions
positions = {
    "left": (100, 240),
    "right": (540, 240),
    "top": (320, 80),
    "bottom": (320, 400),
    "centre": (320, 240),
    "top_left": (100, 80),
    "bottom_right": (540, 400),
}

for name, position in positions.items():
    image = np.zeros((height, width, 3), dtype=np.uint8)

    cv2.circle(
        image,
        position,
        radius,
        (0, 0, 255),
        -1
    )

    path = output_dir / f"ball_{name}.jpg"
    cv2.imwrite(str(path), image)

    print(f"Created {path}: ball position {position}")

print("All test images created.")