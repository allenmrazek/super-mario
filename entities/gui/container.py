from pygame import Rect
from .frame import Frame, Anchor
from util import make_vector, copy_vector


class Container(Frame):
    """Rather similar to a Frame, except it can apply an offset to the drawing positions of
    all children """
    def __init__(self, relative_position, rect, anchor=Anchor.TOP_LEFT):
        super().__init__(relative_position, rect, anchor)

        self._offset = make_vector(0, 0)
        self.hidden_rect = rect

    def get_absolute_position(self):
        return super().get_absolute_position() - self._offset

    def draw(self, screen, view_rect):
        # set correct clipping rect
        existing_cr = screen.get_clip()
        cr = Rect(*(super().get_absolute_position()), self.width, self.height)

        screen.set_clip(cr)
        self.hidden_rect = cr
        super().draw(screen, view_rect)

        screen.set_clip(existing_cr)

    @property
    def offset(self):
        return copy_vector(self._offset)

    @offset.setter
    def offset(self, val):
        self._offset = make_vector(*val)
        self.layout()

    @property
    def x(self):
        return self._offset.x

    @x.setter
    def x(self, val):
        self._offset.x = val
        self.layout()

    @property
    def y(self):
        return self._offset.y

    @y.setter
    def y(self, val):
        self._offset.y = val
        self.layout()

    # todo: get_absolute_rect?
