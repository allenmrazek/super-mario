from pygame import Rect, Surface
from .element import Element
from entities.gui import Button, Window
from util import make_vector
from entities.gui.drawing import smart_draw


# todo: scrollable contents (this isn't complete)
class ScrollableContents(Element):
    def __init__(self, relative_pos, visible_size, scrollable_size, content):
        super().__init__(relative_pos)

        assert scrollable_size[0] >= visible_size[0]
        assert scrollable_size[1] >= visible_size[1]

        self.visible_rect = Rect(*relative_pos, *visible_size)
        self.content_rect = Rect(*relative_pos, *scrollable_size)
        self.scroll_pos = make_vector(0, 0)
        self.content_surface = content
        self.visible_surface = Surface(visible_size)

    def set_scroll(self, pos):
        self.scroll_pos = (min(pos[0], self.content_rect.width - self.visible_rect.width),
                           min(pos[1], self.content_rect.height - self.visible_rect.height))

        # update content
        dest = self.visible_rect.copy()
        dest.x, dest.y = 0, 0

        src = self.visible_rect.copy()
        src.x, src.y = self.scroll_pos[0], self.scroll_pos[1]
        src.width -= self.scroll_pos[0]
        src.height -= self.scroll_pos[1]

        smart_draw(self.visible_surface, self.content_surface, dest, src)
