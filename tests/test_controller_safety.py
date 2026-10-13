import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "scripts")
)

from tracking_controller import PanTiltController

controller = PanTiltController()

# Test 1: Deadband
print("Test 1: Deadband")

initial_pan = controller.pan_angle
initial_tilt = controller.tilt_angle

pan, tilt = controller.update(3, 4)

assert pan == initial_pan
assert tilt == initial_tilt

print("PASS: Small errors do not change the angles.")

# Test 2: Angle limits
print("\nTest 2: Angle limits")

for _ in range(10000):
    pan, tilt = controller.update(-10000, 10000)

assert 60 <= pan <= 120
assert 60 <= tilt <= 120

print(f"PASS: Pan = {pan:.2f}, Tilt = {tilt:.2f}")

# Test 3: Target disappears
print("\nTest 3: Target disappears")

old_pan = controller.pan_angle
old_tilt = controller.tilt_angle

pan, tilt = controller.update(
    100,
    -100,
    target_found=False
)

assert pan == old_pan
assert tilt == old_tilt

print("PASS: Controller holds its position.")

# Test 4: Angles remain valid over repeated updates
print("\nTest 4: Repeated updates")

for i in range(1000):
    error_x = (-1) ** i * 200
    error_y = (-1) ** (i + 1) * 150

    pan, tilt = controller.update(error_x, error_y)

    assert 60 <= pan <= 120
    assert 60 <= tilt <= 120

print("PASS: Angles remain within limits.")

print("\nAll controller safety tests passed.")