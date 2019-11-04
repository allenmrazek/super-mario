from abc import ABC, abstractmethod
from entities.entity import Entity
from util import world_to_screen


class Projectile(Entity, ABC):
    def __init__(self, animation, level, parameters, hitbox_offset, hitbox_size, movement_mask, harm_mask):
        self.animation = animation

        super().__init__(self.animation.rect)

        from .behaviors import SimpleMovement, Interactive

        self.movement = SimpleMovement(
            self, level.collider_manager, parameters, movement_mask, self.on_movement_collision)

        # not DamageMario because projectiles by themselves won't necessarily harm mario (ex: mario fireballs)
        self.harm = Interactive(level, self, hitbox_offset, hitbox_size, self.on_hit)
        self.harm.hitbox.mask = harm_mask

    def update(self, dt, view_rect):
        self.movement.update(dt)
        self.harm.update(dt)
        self.animation.update(dt)

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))
        self.movement.draw(screen, view_rect)

    @abstractmethod
    def on_movement_collision(self, collision):
        # hit something in movement mask
        pass

    @abstractmethod
    def on_hit(self, collision):
        # hit something in harm mask
        pass
