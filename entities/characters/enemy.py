from abc import ABC, abstractmethod
from typing import NamedTuple
from .level_entity import LevelEntity


class Enemy(LevelEntity, ABC):
    def __init__(self, level, position, rect):
        super().__init__(rect)

        assert level is not None

        self.position = position
        self.level = level

    @property
    def layer(self):
        import entities.entity
        return entities.entity.Layer.Enemy

    @abstractmethod
    def update(self, dt, view_rect):
        pass

    @abstractmethod
    def draw(self, screen, view_rect):
        pass

    @abstractmethod
    def die(self):
        pass

    @abstractmethod
    def destroy(self):
        pass


class EnemyParameters(NamedTuple):
    max_horizontal_velocity: float
    max_vertical_velocity: float
    jump_velocity: float
    squash_bounce_velocity: float  # velocity applied to mario when he squashes this enemy (if he can)
    gravity: float

    @staticmethod
    def create(hmax, vmax, jump, squash, gravity):
        return EnemyParameters(max_horizontal_velocity=hmax,
                               max_vertical_velocity=vmax,
                               jump_velocity=jump,
                               squash_bounce_velocity=squash,
                               gravity=gravity)
