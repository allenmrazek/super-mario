import pygame
from pygame import Vector2
from .game_state import GameState
import config


class PhysicsTest(GameState):
    def __init__(self):
        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.position = Vector2()

    def update(self, input_state, elapsed):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.image, self.rect)

    @property
    def finished(self):
        return False

    def activated(self):
        self.position = config.screen_rect.center
        self.rect.center = self.position
