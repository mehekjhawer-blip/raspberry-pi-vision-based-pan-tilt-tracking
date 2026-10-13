import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "scripts")
)

from tracking_controller import PanTiltController

controller = PanTiltController()

print("Initial position:")
print(f"Pan: {controller.pan_angle:.2f}")
print(f"Tilt: {controller.tilt_angle:.2f}")

# Situation 1: Ball visible on the right.
print("\n1. Ball detected on the right")

pan, tilt = controller.update(150, 0)

print(f"Pan: {pan:.2f}")
print(f"Tilt: {tilt:.2f}")

# Save the current position.
saved_pan = pan
saved_tilt = tilt

# Situation 2: Ball disappears.
print("\n2. Ball disappears")

pan, tilt = controller.update(
    0,
    0,
    target_found=False
)

assert pan == saved_pan
assert tilt == saved_tilt

print(f"Pan: {pan:.2f}")
print(f"Tilt: {tilt:.2f}")
print("PASS: Controller holds its position.")

# Situation 3: Ball reappears on the left.
print("\n3. Ball reappears on the left")

pan, tilt = controller.update(-150, 0)

print(f"Pan: {pan:.2f}")
print(f"Tilt: {tilt:.2f}")

assert 60 <= pan <= 120
assert 60 <= tilt <= 120

print("\nAll target-loss tests passed.")