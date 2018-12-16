from pyne.expectations import expect
from pyne.matchers import Matcher
from pyne.pyne_test_collector import it, describe, before_each
from pyne.pyne_tester import pyne

from image_viewer.accelerometer_controls import AccelerometerControls
from image_viewer.models.image import Image
from image_viewer.models.vector_2d import Vector2D
from image_viewer.models.view import View


def at_least(number):
    return Matcher("at_least", lambda subject, _: subject >= number, number)


def at_most(number):
    return Matcher("at_least", lambda subject, _: subject <= number, number)


class FakeAccelerometer(object):
    def __init__(self):
        self._acceleration = (0, 0, 1)

    def acceleration(self):
        """The x, y, z acceleration values returned in a 3-tuple in m / s ^ 2."""
        # x, y, z = unpack('<hhh', self._read_register(_REG_DATAX0, 6))
        # x = x * _ADXL345_MG2G_MULTIPLIER * _STANDARD_GRAVITY
        # y = y * _ADXL345_MG2G_MULTIPLIER * _STANDARD_GRAVITY
        # z = z * _ADXL345_MG2G_MULTIPLIER * _STANDARD_GRAVITY
        return self._acceleration


@pyne
def accelerometer_controls_test():
    @before_each
    def _(self):
        self.image = Image(width=16, height=16)
        self.view = View(offset=Vector2D(x=0, y=0), image=self.image)
        self.accelerometer = FakeAccelerometer()
        self.controls = AccelerometerControls(accelerometer=self.accelerometer,
                                              view=self.view)

    @describe("#read_accelerometer")
    def _():
        @describe("when the x acceleration is 5m/s^2")
        def _():
            @it("sets the x velocity to 3")
            def _(self):
                self.accelerometer.acceleration = (5, 0, 0)
                self.controls.read_accelerometer()
                expect(self.controls.velocity.x).to_be(3)

    @describe("#update_view")
    def _():
        @describe("when the controls are moving")
        def _():
            @before_each
            def _(self):
                self.controls.velocity = Vector2D(2, 2)

            @it("increments the view offset")
            def _(self):
                self.controls.update_view()
                expect(self.view.offset.x).to_be(at_least(1))
                expect(self.view.offset.y).to_be(at_least(1))

            @describe("when the view is near the edge of the image")
            def _():
                @before_each
                def _(self):
                    self.image.width = 10
                    self.image.height = 10
                    self.view.height = 2
                    self.view.width = 2
                    self.view.offset = Vector2D(x=1, y=2)

                @it("keeps the view within the bounds of the image")
                def _(self):
                    self.controls.velocity = Vector2D(100, 100)
                    self.controls.update_view()

                    expect(self.view.offset.x + self.view.width).to_be(self.image.width)
                    expect(self.view.offset.y + self.view.height).to_be(self.image.height)

                    self.controls.velocity = Vector2D(-100, -100)
                    self.controls.update_view()

                    expect(self.view.offset.x).to_be(0)
                    expect(self.view.offset.y).to_be(0)
