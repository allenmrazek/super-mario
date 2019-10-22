from typing import NamedTuple
import pygame
from .element import Element
from .element import Anchor
from event.game_events import EventHandler
from util import copy_vector
from util import make_vector


class WindowParameters(NamedTuple):
    bar_color: pygame.Color
    text_color: pygame.Color
    font: pygame.font.SysFont
    height: int
    title: str


class _TitleBar(Element):
    def __init__(self, params):
        super().__init__(make_vector(0, 0), anchor=Anchor.TOP_LEFT)
        self.surface = params.font.render(params.title, True, params.text_color)
        self.bar_color = params.bar_color
        self.text_color = params.text_color
        self.font = params.font
        self.height = params.height if params.height > 0 else self.surface.get_height()

        self.layout()

    def draw(self, screen):
        # draw title bar
        r = self.get_absolute_rect()
        current_clip = screen.get_clip()
        screen.set_clip(r)
        screen.set_clip(None)

        screen.fill(self.bar_color, r)
        screen.blit(self.surface, r)

        screen.set_clip(current_clip)

    def update(self, dt):
        pass

    def handle_event(self, evt, game_events):
        pass  # todo

    def layout(self):
        self.width = self.parent.width if self.parent is not None else self.width

        # todo: relative position of buttons?
        super().layout()


class Window(Element, EventHandler):
    def __init__(self, window_position, rect, background, anchor=Anchor.CENTER, params=None):
        super().__init__(window_position, anchor, rect)

        assert background is not None
        assert isinstance(background, pygame.Surface) or isinstance(background, pygame.Color) \
            or isinstance(background, tuple)

        self.element_position = copy_vector(window_position)
        self.background = background
        self.titlebar = _TitleBar(params) if params is not None else None

        if self.titlebar is not None:
            self.add_child(self.titlebar)

        self.layout()

        # event-related state
        self._is_dragging = False
        self._start_drag = pygame.Vector2()

    def draw(self, screen: pygame.Surface):
        r = screen.get_rect().clip(self.rect)

        if isinstance(self.background, pygame.Surface):
            screen.blit(self.background, r)
        else:
            screen.fill(self.background, r)

        screen.set_clip(r)

        # handle title bar
        if self.titlebar is not None:
            self.titlebar.draw(screen)

        # draw children
        super().draw(screen)

        screen.set_clip(None)

    def update(self, dt):
        pass

    def handle_event(self, evt, game_events):
        # let children have a shot at the event first
        super().handle_event(evt, game_events)

        # handle own events
        if not evt.consumed:
            if evt.type == pygame.MOUSEBUTTONDOWN:
                # todo: bring to front?

                self.consume(evt)  # always consume mousedown in a window
                self._is_dragging = True

            elif evt.type == pygame.MOUSEBUTTONUP:
                self.consume(evt)
                self._is_dragging = False
            elif evt.type == pygame.MOUSEMOTION:
                if self._is_dragging:
                    self.consume(evt)
                    rel = evt.rel

                    self.relative_position += rel
                    self.layout()
