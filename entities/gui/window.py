import pygame
from .frame import Frame
from .element import Anchor
from .sliced_image import SlicedImage
from util import copy_vector


class Window(Frame):
    """A window is essentially just a rect on the screen, with a color, sliced, or surface background. It
    sets a clipping rect for the screen which prevents children from drawing anything outside of it"""
    def __init__(self, window_position, size, background, anchor=Anchor.TOP_LEFT, draggable=True):
        super().__init__(window_position, size, anchor)

        assert background is not None
        assert isinstance(background, pygame.Surface) or isinstance(background, pygame.Color) \
            or isinstance(background, tuple) or isinstance(background, SlicedImage)

        self.element_position = copy_vector(window_position)
        self.background = background
        self.draggable = draggable

        # event-related state
        self._is_dragging = False
        self._start_drag = pygame.Vector2()

    def draw(self, screen: pygame.Surface):
        # pygame seems to just set coordinates to 0 if rect is outside of screen and you try and blit it?
        # so ensure only visible portion of window onscreen is drawn
        r = screen.get_rect().clip(self.rect)

        if isinstance(self.background, pygame.Surface):
            screen.blit(self.background, r)
        elif isinstance(self.background, SlicedImage):
            raise NotImplementedError
        else:
            screen.fill(self.background, r)

        # don't let children draw outside of bounds
        clipping_rect = screen.get_clip()
        screen.set_clip(r)

        # draw children
        super().draw(screen)

        # restore screen as we found it
        screen.set_clip(clipping_rect)

    def handle_event(self, evt, game_events):
        # let children have a shot at the event first
        super().handle_event(evt, game_events)

        # handle own events
        if self._is_dragging or (not evt.consumed and self.draggable):
            # left-down inside window -> start a drag (assuming no children handled it)
            if evt.type == pygame.MOUSEBUTTONDOWN and self.get_absolute_rect().collidepoint(*evt.pos):
                if self.parent is not None:
                    self.parent.bring_to_front(self)

                self.consume(evt)  # always consume mousedown in a window
                self._is_dragging = True

            elif evt.type == pygame.MOUSEBUTTONUP:
                self._is_dragging = False

                # don't consume this event: could have occurred over another element which is interested in
                # mouseup events...

            elif evt.type == pygame.MOUSEMOTION:
                if self._is_dragging:
                    self.consume(evt)
                    rel = evt.rel

                    self.relative_position += rel
                    self.layout()
            else:
                self._is_dragging = False
