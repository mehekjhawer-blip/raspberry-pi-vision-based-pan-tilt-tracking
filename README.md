# Raspberry Pi 5 Pan-and-Tilt Ball Tracking

## Project objective

Develop a computer-vision system that detects a coloured ball
and tracks it using a pan-and-tilt mechanism.

## Target hardware

- Raspberry Pi 5
- Compatible camera module
- Two servo motors
- Separate servo power supply and buck converter

## Software

- Python 3
- OpenCV
- NumPy
- Picamera2 (for Raspberry Pi camera integration)
- rpi-hardware-pwm (for the planned PWM interface)

## Development environment

Initial software development was performed on Ubuntu 24.04 LTS
using synthetic images.

## Current features

- HSV-based red-ball detection
- Morphological noise reduction
- Contour detection
- Ball-centre calculation
- Proportional pan-and-tilt controller
- Deadband
- Servo angle limits
- Target-loss position hold
- CSV performance logging

## Tests completed

- Seven synthetic ball-position detection tests passed.
- Controller deadband test passed.
- Controller angle-limit test passed.
- Target-loss test passed.
- Repeated-update safety test passed.
- Integrated simulation completed successfully.

## Remaining work

- Install and configure Raspberry Pi OS.
- Verify the camera using Picamera2.
- Configure and test hardware PWM.
- Connect and test each servo independently.
- Integrate live camera frames with the controller.
- Calibrate tracking directions and controller gains.
- Measure actual tracking error, frame rate, and response time.

## Limitations

Current results are from software simulations using synthetic images.
They do not establish real-world tracking accuracy or hardware performance.
