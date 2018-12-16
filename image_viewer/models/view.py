from image_viewer.models.image import Image
from image_viewer.models.vector_2d import Vector2D


class View:
    def __init__(self, width=8, height=4, image=Image(), offset=Vector2D()):
        self.image = image
        self.width = width
        self.height = height
        self.offset = offset

    def max_offset(self):
        return Vector2D(
            x=self.image.width - self.width,
            y=self.image.height - self.height)

    def render(self, canvas):
        for x in range(0, self.width):
            for y in range(0, self.height):
                canvas.pixels[x, y] = self.image.pixel_data[x + self.offset.x][y + self.offset.y]
