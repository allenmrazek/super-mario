from pygame import Rect, Surface
from .element import Element
from entities.gui import Button, Window
from util import make_vector
from entities.gui.drawing import smart_draw
from util import copy_vector


class ScrollableContents(Element):
    def __init__(self, relative_pos, visible_size, content):
        super().__init__(relative_pos, initial_rect=Rect(0, 0, *visible_size))

        assert isinstance(content, Surface)

        self.content_rect = Rect(0, 0, *content.get_rect().size)
        self.scroll_pos = make_vector(0, 0)
        self.content = content
        self.set_scroll(self.scroll_pos)

    def set_scroll(self, pos):
        hscroll = max(0, self.content_rect.width - self.width)
        vscroll = max(0, self.content_rect.height - self.height)

        self.scroll_pos = min(hscroll, pos[0]),\
                          min(vscroll, pos[1])

        # compute visible area of content given this scroll position
        self.content_rect.x, self.content_rect.y = self.scroll_pos

    def get_scroll(self):
        return copy_vector(self.scroll_pos)

    def draw(self, screen):
        existing_cr = screen.get_clip()

        screen_rect = self.get_absolute_rect()
        screen.set_clip(screen_rect)

        super().draw(screen)

        smart_draw(screen, self.content, screen_rect.topleft, self.content_rect)

        screen.set_clip(existing_cr)
