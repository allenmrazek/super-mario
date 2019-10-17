from abc import ABC, abstractmethod
from pygame.sprite import Rect
from enum import IntEnum
from util import copy_vector
from util import make_vector

class Layer(IntEnum):
    Background = 1 << 0
    Block = 1 << 1
    Mario = 1 << 2
    Active = 1 << 3


class Entity(ABC):
    def __init__(self, rect: Rect):
        super().__init__()
        self.rect = rect.copy()
        self._position = make_vector(rect.x, rect.y)  # rect only int values

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @property
    def layer(self):
        return Layer.Background

    @property
    def position(self):
        return copy_vector(self._position)

    @position.setter
    def position(self, pos):
        self._position = copy_vector(pos)


class EntityManager:
    def __init__(self, layers: dict, ordering: list):
        assert layers is not None and len(layers.keys()) > 0
        assert ordering is not None and len(ordering) > 0

        self.layers = layers
        self.ordering = ordering

    @staticmethod
    def create_default():
        # create a default entity manager. This should be sufficient in most cases
        layers = {
            Layer.Background: set(),
            Layer.Block: set(),
            Layer.Mario: set(),
            Layer.Active: set()}

        ordering = [Layer.Background, Layer.Block, Layer.Mario, Layer.Active]

        return EntityManager(layers, ordering)

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