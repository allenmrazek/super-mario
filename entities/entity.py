from abc import ABC, abstractmethod
from pygame import Surface
from pygame import Color
from pygame.sprite import Sprite
from pygame.sprite import Rect
from enum import IntEnum
import config


class Layer(IntEnum):
    Background = 1 << 0
    Block = 1 << 1
    Mario = 1 << 2
    Active = 1 << 3


blank_image = None


class Entity(ABC, Sprite):
    def __init__(self, rect: Rect):
        super().__init__()
        self.rect = rect.copy()

        global blank_image

        if blank_image is not None:
            blank_image = Surface((1, 1)).convert()
            blank_image.fill(config.transparent_color)
            blank_image.set_colorkey(config.transparent_color)

        self.image = blank_image

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @property
    def layer(self):
        return Layer.Background


class EntityManager:
    def __init__(self):
        self.layers = {
            Layer.Background: set(),
            Layer.Block: set(),
            Layer.Mario: set(),
            Layer.Active: set()}

        self.ordering = [Layer.Background, Layer.Block, Layer.Mario, Layer.Active]

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
        # todo: update only screen and a quarter
        def update_entity(entity):
            entity.update(dt)

        self._do_on_each_layer(update_entity)

    def draw(self, screen):
        # todo: draw only screen and a quarter
        def draw_entity(entity):
            entity.draw(screen)

        self._do_on_each_layer(draw_entity)

    def _do_on_each_layer(self, fn):
        for layer in self.ordering:
            for entity in self.layers[layer]:
                fn(entity)