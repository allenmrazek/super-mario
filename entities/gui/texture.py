import pygame
from .element import Element
from .element import Anchor


class Texture(Element):
    def __init__(self, surface, position, anchor=Anchor.TOP_LEFT):
        assert surface is not None

        if isinstance(surface, str):
            surface = pygame.image.load(surface)

        super().__init__(position, initial_rect=surface.get_rect(), anchor=anchor)
        self.surface = surface

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
