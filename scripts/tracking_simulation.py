import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent)
)

from tracking_controller import PanTiltController

WIDTH = 640
HEIGHT = 480

FRAME_CENTRE_X = WIDTH // 2
FRAME_CENTRE_Y = HEIGHT // 2

controller = PanTiltController()

# Simulated ball positions.
# The ball moves left to right and then back.
positions = [
    (100, 240),
    (180, 240),
    (260, 240),
    (320, 240),
    (400, 240),
    (480, 240),
    (540, 240),
    (480, 240),
    (400, 240),
    (320, 240),
]

print("Ball-tracking simulation")
print("-" * 75)
print(
    f"{'Ball position':<20}"
    f"{'Error X':<12}"
    f"{'Error Y':<12}"
    f"{'Pan angle':<14}"
    f"{'Tilt angle':<14}"
)
print("-" * 75)

for ball_x, ball_y in positions:
    error_x = ball_x - FRAME_CENTRE_X
    error_y = ball_y - FRAME_CENTRE_Y

    pan, tilt = controller.update(error_x, error_y)

    print(
        f"{str((ball_x, ball_y)):<20}"
        f"{error_x:<12}"
        f"{error_y:<12}"
        f"{pan:<14.2f}"
        f"{tilt:<14.2f}"
    )

print("-" * 75)
print("Simulation completed.")