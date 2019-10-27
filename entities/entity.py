from abc import ABC, abstractmethod
from pygame.sprite import Rect
from enum import IntFlag
from util import copy_vector
from util import make_vector


class Layer(IntFlag):
    Background = 1 << 0     # behind blocks
    Block = 1 << 1          # layer blocks are drawn on
    Mario = 1 << 2          # take a guess
    Enemy = 1 << 3          # take another guess
    Active = 1 << 4         # "active" things: think fireballs and projectiles; mario death animations
    Interface = 1 << 5      # interface stuff here
    Overlay = 1 << 6        # a final layer that absolutely will overlay everything. Use sparingly

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
    def update(self, dt, view_rect):
        pass

    @abstractmethod
    def draw(self, screen, view_rect):
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
        ordering = [Layer.Background, Layer.Block, Layer.Enemy, Layer.Mario, Layer.Active, Layer.Interface, Layer.Overlay]

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

    def update(self, dt, view_rect):
        # todo: update only screen and a quarter
        def update_entity(entity, vr):
            entity.update(dt, vr)

        self._do_on_each_layer(update_entity, view_rect)

    def draw(self, screen, view_rect):
        # todo: draw only screen and a quarter
        def draw_entity(entity, vr):
            entity.draw(screen, vr)

        self._do_on_each_layer(draw_entity, view_rect)

    def _do_on_each_layer(self, fn, view_rect):
        for layer in self.ordering:
            entities = list(self.layers[layer])

            for entity in entities:
                if hasattr(entity, "enabled"):
                    if entity.enabled:
                        fn(entity, view_rect)

                else:
                    fn(entity, view_rect)
