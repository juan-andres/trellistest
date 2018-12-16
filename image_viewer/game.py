import time

from color_names import BLACK
from image_viewer.accelerometer_controls import AccelerometerControls
from image_viewer.models.view import View


class Game:
    def __init__(self, trellis, accelerometer):
        """initialize a Game instance.
        trellis        -- the TrellisM4Express instance to use as input and screen.
        accel          -- the accelerometer interface object to use as input
        ramp           -- how often (in steps) to increase the speed (default 20)
        challenge_ramp -- how often (in steps) to increase the challenge of the posts
        """
        self.view = View()
        self.controls = AccelerometerControls(accelerometer, self.view)
        self._trellis = trellis
        self._interstitial_delay = 1.0

    def _restart(self):
        """Restart the game."""
        pass

    def _update_game_state(self):
        self.controls.read_accelerometer()
        self.controls.update_view()

    def _render(self):
        """Update the screen."""
        self._trellis.pixels.fill(BLACK)
        self.view.render(self._trellis)
        self._trellis.pixels.show()

    def play(self):
        while True:
            self._update_game_state()
            self._render()
            time.sleep(0.05)
