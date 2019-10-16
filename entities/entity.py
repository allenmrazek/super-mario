from abc import ABC, abstractmethod
from pygame.sprite import Sprite
from enum import Enum


class CollisionLayer(Enum):
    Nothing = 0
    Mario = 1
    Block = 2


class DrawLayer(Enum):
    Background = 0
    Block = 1
    Mario = 2


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

    @property
    def collision_mask(self):
        # return an int, with bits set to layers to collide with
        return CollisionLayer.Nothing

    @property
    def layer(self):
        return DrawLayer.Background


class EntityManager:
    def __init__(self):
        self.layers = {DrawLayer.Background: set(), DrawLayer.Block: set(), DrawLayer.Mario: set()}
        self.ordering = [DrawLayer.Background, DrawLayer.Block, DrawLayer.Mario]

    def register(self, entity):
        assert isinstance(entity, Entity)
        assert entity.layer in self.layers.keys()

        self.layers[entity.layer].add(entity)

    def unregister(self, entity):
        assert isinstance(entity, Entity)
        assert entity.layer in self.layers.keys()
        assert entity in self.layers[entity.layer]

        self.layers[entity.layer].remove(entity)

    def update(self, dt):
        def update_entity(entity):
            entity.update(dt)

        self._do_on_each_layer(update_entity)

    def draw(self, screen):
        def draw_entity(entity):
            entity.draw(screen)

        self._do_on_each_layer(draw_entity)

    def _do_on_each_layer(self, fn):
        for layer in self.ordering:
            for entity in self.layers[layer]:
                fn(entity)