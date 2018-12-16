from image_viewer.models.vector_2d import Vector2D
from image_viewer.models.view import View

GRAVITY = 9.8

MAX_SPEED_TILT = GRAVITY * 0.5
MIN_MOVE_TILT = GRAVITY * 0.1


def clamp(value, range):
    return max(min(value, range.stop), range.start)


class AccelerometerControls:
    def __init__(self, accelerometer, view=View()):
        self.velocity = Vector2D()
        self.accelerometer = accelerometer
        self.view = view

    def read_accelerometer(self):
        x_mss, y_mss, z_mss = self.accelerometer.acceleration
        # TODO business logic - decide how fast to go

        x_tilt = max(min(x_mss, MAX_SPEED_TILT), -1 * MAX_SPEED_TILT)
        if abs(x_tilt) >= MIN_MOVE_TILT:
            x_tilt_percent_of_max = (x_tilt - MIN_MOVE_TILT) / (MAX_SPEED_TILT - MIN_MOVE_TILT)
            self.velocity.x = round(x_tilt_percent_of_max * 3)
        else:
            self.velocity.x = 0

        y_tilt = max(min(y_mss, MAX_SPEED_TILT), -1 * MAX_SPEED_TILT)
        if abs(y_tilt) >= MIN_MOVE_TILT:
            y_tilt_percent_of_may = (y_tilt - MIN_MOVE_TILT) / (MAX_SPEED_TILT - MIN_MOVE_TILT)
            self.velocity.y = round(y_tilt_percent_of_may * 3)
        else:
            self.velocity.y = 0

    def update_view(self):
        max_offset = self.view.max_offset()
        self.view.offset.x = clamp(self.view.offset.x + self.velocity.x, range(0, max_offset.x))
        self.view.offset.y = clamp(self.view.offset.x + self.velocity.y, range(0, max_offset.y))
