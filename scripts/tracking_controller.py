class PanTiltController:
    def __init__(
        self,
        pan_angle=90.0,
        tilt_angle=90.0,
        min_angle=60.0,
        max_angle=120.0,
        deadband=8.0,
        gain=0.04,
        smoothing=0.25,
    ):
        self.pan_angle = pan_angle
        self.tilt_angle = tilt_angle

        self.min_angle = min_angle
        self.max_angle = max_angle

        self.deadband = deadband
        self.gain = gain
        self.smoothing = smoothing

    def update(self, error_x, error_y, target_found=True):
        # Hold position when the target disappears.
        if not target_found:
            return self.pan_angle, self.tilt_angle

        # Ignore small errors.
        if abs(error_x) < self.deadband:
            error_x = 0

        if abs(error_y) < self.deadband:
            error_y = 0

        # Convert image error into desired angle changes.
        # The signs will be calibrated on the actual bracket.
        pan_change = -self.gain * error_x
        tilt_change = self.gain * error_y

        # Smooth the angle changes.
        self.pan_angle += self.smoothing * pan_change
        self.tilt_angle += self.smoothing * tilt_change

        # Enforce conservative angle limits.
        self.pan_angle = max(
            self.min_angle,
            min(self.max_angle, self.pan_angle)
        )

        self.tilt_angle = max(
            self.min_angle,
            min(self.max_angle, self.tilt_angle)
        )

        return self.pan_angle, self.tilt_angle