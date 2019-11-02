from abc import abstractmethod
from typing import NamedTuple
from warnings import warn
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

    @staticmethod
    def create_generic_factory(cls):

        def _factory(level, serialized_values):
            try:
                thing = cls(level)

                deserialize = getattr(thing, "deserialize", None)

                if serialized_values is not None and deserialize is not None:
                    thing.deserialize(serialized_values)

                return thing
            except TypeError:
                print("GenericFactory: failed to create {}".format(cls.__name__))
                warn("GenericFactory failed to create a LevelEntity")
                raise

        name = cls.__name__

        assert name not in LevelEntity.Factories

        LevelEntity.Factories[name] = _factory
        return _factory


