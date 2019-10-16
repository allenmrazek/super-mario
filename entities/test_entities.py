import pygame
from .entity import Entity
from .collider import Collider
from .collider import ColliderManager
from .entity import Layer


class BouncingBall(Entity):
    def __init__(self, collider_mgr: ColliderManager, position, velocity):
        super().__init__(pygame.Rect(0, 0, 16, 16))
        self.velocity = velocity
        self.position = position
        self.collider_mgr = collider_mgr
        self.collider = Collider(self, collider_mgr, Layer.Block)
        collider_mgr.register(self.collider)

        # create ball
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 0, 255))
        pygame.draw.circle(self.image, (0, 255, 0), (8, 8), 8)
        self.image = self.image.convert()
        self.image.set_colorkey((255, 0, 255))

    def update(self, dt):
        # adjust position
        new_pos = self.position + self.velocity * dt

        collisions = self.collider.move(new_pos)

        if len(collisions) > 0:
            # reverse velocity instead
            self.velocity.y *= -1
        else:
            self.position = new_pos

    def draw(self, screen):
        self.rect.x, self.rect.y = self.position
        screen.blit(self.image, self.rect)

    @property
    def layer(self):
        return Layer.Active
