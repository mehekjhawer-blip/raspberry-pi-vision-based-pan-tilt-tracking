import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "scripts")
)

from tracking_controller import PanTiltController

controller = PanTiltController()

print("Initial angles:")
print("Pan:", controller.pan_angle)
print("Tilt:", controller.tilt_angle)

print("\nBall moves to the right:")
pan, tilt = controller.update(100, 0)
print(f"Pan: {pan:.2f}, Tilt: {tilt:.2f}")

print("\nBall moves below the centre:")
pan, tilt = controller.update(0, 100)
print(f"Pan: {pan:.2f}, Tilt: {tilt:.2f}")

print("\nBall disappears:")
old_pan = controller.pan_angle
old_tilt = controller.tilt_angle

pan, tilt = controller.update(0, 0, target_found=False)

print(f"Pan: {pan:.2f}, Tilt: {tilt:.2f}")

assert pan == old_pan
assert tilt == old_tilt

print("\nController simulation completed successfully.")