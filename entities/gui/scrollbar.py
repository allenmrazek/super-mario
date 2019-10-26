from enum import Enum
import pygame
from pygame import Rect
from . import Button, Window, Anchor, Element
from . import smart_draw
from util import make_vector


class ScrollbarType(Enum):
    VERTICAL = 0,
    HORIZONTAL = 1


class _SliderButton(Button):
    def __init__(self, relative_position, size, owner, background, mouseover_image):
        font = pygame.font.SysFont(None, 12)  # not used, dummy value

        super().__init__(relative_position, size, background, font,
                         anchor=Anchor.CENTER, mouseover_image=mouseover_image)

        self.scrollbar = owner

        # state
        self._is_dragging = False

    def handle_event(self, evt, game_events):
        if evt.type == pygame.MOUSEBUTTONDOWN:
            within_button = self.rect.collidepoint(evt.pos)

            if within_button:
                self.consume(evt)

            self._is_dragging = within_button
        elif evt.type == pygame.MOUSEMOTION and self._is_dragging:
            self.scrollbar.on_slider_moved(evt.pos)
            self.consume(evt)
        elif evt.type == pygame.MOUSEBUTTONUP:
            self._is_dragging = False

        super().handle_event(evt, game_events)


class Scrollbar(Element):
    VERTICAL_WIDTH = 16
    HORIZONTAL_HEIGHT = 16

    def __init__(self, relative_position, sb_type, width_or_height, sb_background,
                 sb_button_background, sb_max_value, sb_min_value=0, sb_button_mouseover=None,
                 on_value_changed_callback=None):
        # todo: to implement anchor, some assumptions in positioning code need fixing. low priority for now

        if sb_type == ScrollbarType.VERTICAL:
            initial_rect = Rect(*relative_position, Scrollbar.VERTICAL_WIDTH, width_or_height)
        else:
            initial_rect = Rect(*relative_position, width_or_height, Scrollbar.HORIZONTAL_HEIGHT)

        super().__init__(relative_position, initial_rect)

        assert sb_min_value <= sb_max_value

        self.sb_type = sb_type
        self.background = sb_background
        self.sb_button = sb_button_background
        self.max_value = sb_max_value
        self.min_value = sb_min_value
        self.on_value_changed = None

        # create slider button
        self.slider = _SliderButton(make_vector(self.width // 2, self.height // 2), None, self, sb_button_background, sb_button_mouseover)
        self.add_child(self.slider)

        self.layout()

        self.value = sb_min_value
        self.on_value_changed = on_value_changed_callback

    def draw(self, screen, view_rect):
        smart_draw(screen, self.background, self.get_absolute_rect())
        super().draw(screen, view_rect)

    def update(self, dt, view_rect):
        pass

    def on_slider_moved(self, absolute):
        if self.sb_type == ScrollbarType.VERTICAL:
            # try to align thumb button with y mouse coordinates
            thumb_pos = pygame.Vector2(*self.slider.rect.center)
            thumb_pos.y = absolute[1]

            relative = thumb_pos - pygame.Vector2(*self.rect.center)

            if relative.y < 0:
                relative.y = 0
            elif relative.y > self.height:
                relative.y = self.height

            # compute ratio of sb movement on bar
            ratio = relative.y / self.height

            self.value = ratio * (self.max_value - self.min_value) + self.min_value

        elif self.sb_type == ScrollbarType.HORIZONTAL:
            # try to align thumb button with x mouse coordinates
            thumb_pos = pygame.Vector2(*self.slider.rect.center)
            thumb_pos.x = absolute[0]

            relative = thumb_pos - pygame.Vector2(*self.rect.center)

            if relative.x < 0:
                relative.x = 0
            elif relative.x > self.width:
                relative.x = self.width

            # compute ratio of sb movement on bar
            ratio = relative.x / self.width

            self.value = ratio * (self.max_value - self.min_value) + self.min_value

    @property
    def value(self):
        return self.current_value

    @value.setter
    def value(self, new_value):
        self.current_value = min(max(new_value, self.min_value), self.max_value)

        # position slider for new value
        # map value into 0...1 range
        delta = self.max_value - self.min_value

        if delta > 0:
            ratio = (self.current_value - self.min_value) / (self.max_value - self.min_value)
        else:
            ratio = 0.

        if self.sb_type == ScrollbarType.HORIZONTAL:
            self.slider.relative_position.x = self.width * ratio
        else:
            self.slider.relative_position.y = self.height * ratio

        self.layout()

        if self.on_value_changed is not None:
            self.on_value_changed(self.current_value)
