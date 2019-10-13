import pygame
from .game_state import GameState
from entities import Mario


class TestMarioPhysics(GameState):
    def __init__(self, input_state, atlas):
        super().__init__(input_state)

        self.mario = Mario(input_state, atlas)
        self.font = pygame.font.SysFont(None, 24)
        self.velocity = self.font.render("Vel: 0", True, (255, 255, 255))
        self.running = self.font.render("Walking", True, (255, 255, 255))
        self.running_rect = self.running.get_rect()
        self.running_rect.top = self.velocity.get_rect().bottom
        self.skidding = self.font.render("not skidding", True, (255, 255, 255))
        self.skidding_rect = self.skidding.get_rect()
        self.skidding_rect.top = self.running_rect.bottom
        self.airborne = self.font.render("ground", True, (255, 255, 255))
        self.airborne_rect = self.airborne.get_rect()
        self.airborne_rect.top = self.skidding_rect.bottom

    def update(self, elapsed):
        self.mario.update(elapsed)

    def draw(self, screen):
        screen.fill((20, 20, 20))
        self.mario.draw(screen)

        self.velocity = self.font.render("Vel: {:.2f}".format(self.mario.velocity.x), True, (255, 255, 255))
        screen.blit(self.velocity, self.velocity.get_rect())

        self.running = self.font.render("run" if self.mario.is_running else "walk", True, (255, 255, 255))
        screen.blit(self.running, self.running_rect)

        self.skidding = self.font.render("skid" if self.mario.skidding else "not skid", True, (255, 255, 255))
        screen.blit(self.skidding, self.skidding_rect)

        self.airborne = self.font.render("air" if self.mario.is_airborne else "ground", True, (255, 255, 255))
        screen.blit(self.airborne, self.airborne_rect)

    @property
    def finished(self):
        return False
