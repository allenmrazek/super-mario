from abc import abstractmethod
from typing import NamedTuple
import warnings
from entities.entity import Entity
from util import make_vector


class LevelEntity(Entity):
    """This type of Entity is serialized by the level editor. Anything that can be placed on the map which isn't
    a tile should have this as a parent, plus a registered factory function"""
    Factories = {}

    def __init__(self,  rect):
        super().__init__(rect)
        self.name = self.__class__.__name__

    @abstractmethod
    def update(self, dt, view_rect):
        pass

    @abstractmethod
    def draw(self, screen, view_rect):
        pass

    @abstractmethod
    def destroy(self):
        """Called when entity is about to be removed from a level (not necessarily due to death: for instance,
        entities in the editor can be destroyed frequently"""
        pass

    @abstractmethod
    def create_preview(self):
        pass

    def serialize(self):
        return {'name': self.__class__.__name__, 'position': (self.position.x, self.position.y)}

    def deserialize(self, values):
        assert values['name'] == self.name

        self.position = make_vector(*tuple(values['position']))

    @staticmethod
    def build(level, entity_values, kind=None):
        assert entity_values is not None or kind is not None

        entity_kind = entity_values['name'] if kind is None else kind

        if entity_kind not in LevelEntity.Factories:
            warnings.warn(f"No factory found for {entity_kind}! Will be ignored and lost")
            return None

        factory = LevelEntity.Factories[entity_kind]

        return factory(level, entity_values)

    @staticmethod
    def register_factory(cls, factory):
        assert cls is not None
        assert factory is not None

        name = cls.__name__

        if name in LevelEntity.Factories.keys():
            warnings.warn(f"'name' already had a registered factory. It will be replaced")

        LevelEntity.Factories[name] = factory


class MovementParameters(NamedTuple):
    max_horizontal_velocity: float
    max_vertical_velocity: float
    jump_velocity: float
    squash_bounce_velocity: float  # velocity applied to mario when he squashes this thing (if he can)
    gravity: float

    @staticmethod
    def create(hmax, vmax, jump, squash, gravity):
        return MovementParameters(max_horizontal_velocity=hmax,
                               max_vertical_velocity=vmax,
                               jump_velocity=jump,
                               squash_bounce_velocity=squash,
                               gravity=gravity)