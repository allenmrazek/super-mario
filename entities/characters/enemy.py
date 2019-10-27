from abc import ABC, abstractmethod
from entities import Entity, Layer


class Enemy(Entity, ABC):
    def __init__(self, level, position, rect):
        super().__init__(rect)

        assert level is not None

        self.position = position
        self.level = level

    @property
    def layer(self):
        return Layer.Enemy

    @abstractmethod
    def update(self, dt, view_rect):
        pass

    @abstractmethod
    def draw(self, screen, view_rect):
        pass

    @abstractmethod
    def die(self):
        pass
