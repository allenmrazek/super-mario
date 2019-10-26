from abc import ABC, abstractmethod
from typing import Sized
from pygame.sprite import Rect
from enum import IntFlag
from util import copy_vector
from util import make_vector


class Layer(IntFlag):
    Background = 1 << 0
    Block = 1 << 1
    Mario = 1 << 2
    Active = 1 << 3
    Interface = 1 << 4
    Overlay = 1 << 5

    @staticmethod
    def count():
        return len(Layer)


class Entity(ABC):
    def __init__(self, rect: Rect):
        super().__init__()

        # reminder to self: we don't just expose this publically because we want them
        # synchronized; specifically, that position can be tracked in floating points
        # (since rects are int-only)
        self._rect = rect.copy()
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
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, val):
        self._rect = val

    @property
    def position(self):
        return copy_vector(self._position)

    @position.setter
    def position(self, pos):
        self._position = copy_vector(pos)
        self._rect.x, self._rect.y = pos

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, w):
        self._rect.width = w

    @property
    def height(self):
        return self._rect.height

    @height.setter
    def height(self, h):
        self._rect.height = h


class EntityManager:
    def __init__(self, layer_ordering: list):
        assert layer_ordering is not None and len(layer_ordering) > 0

        self.ordering = layer_ordering
        self.layers = dict(zip(layer_ordering, [list() for _ in range(len(layer_ordering))]))

    @staticmethod
    def create_default():
        # create a default entity manager. This should be sufficient in most cases
        ordering = [Layer.Background, Layer.Block, Layer.Mario, Layer.Active, Layer.Overlay]

        return EntityManager(ordering)

    def register(self, *args):
        try:
            iterator = iter(*args)

            for item in iterator:
                self._register_internal(item)

        except TypeError:
            for item in args:
                if isinstance(item, Entity):
                    self._register_internal(*args)
                else:
                    self.register(item)

    def _register_internal(self, entity):
        assert entity.layer in self.layers.keys()
        self.layers[entity.layer].append(entity)

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
                if hasattr(entity, "enabled"):
                    if entity.enabled:
                        fn(entity)

                else:
                    fn(entity)
