from abc import ABC, abstractmethod
from pygame.sprite import Sprite


class Entity(ABC, Sprite):
    def on_collision(self, other_entity):
        pass

    def on_hit_top(self, other_entity):
        pass

    def on_hit_bottom(self, other_entity):
        pass

    def on_hit_left(self, other_entity):
        pass

    def on_hit_right(self, other_entity):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def collision_mask(self):
        # return an int, with bits set to layers to collide with
        pass
