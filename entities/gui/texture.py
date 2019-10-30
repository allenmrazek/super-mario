import pygame
from .element import Element
from .element import Anchor
from .drawing import smart_draw


class Texture(Element):
    def __init__(self, background, position, anchor=Anchor.TOP_LEFT):
        assert background is not None

        if isinstance(background, str):
            background = pygame.image.load(background)

        super().__init__(position, initial_rect=background.get_rect(), anchor=anchor)
        self.background = background

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        smart_draw(screen, self.background, self.rect)
