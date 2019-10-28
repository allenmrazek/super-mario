from abc import abstractmethod
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
        """Called by editor to create a preview image for this entity, which appears in the entity picker dialog"""
        pass
    
    def serialize(self):
        return {'name': self.__class__.__name__, 'position': self.position}

    def deserialize(self, values):
        assert values['name'] == self.name

        self.position = make_vector(*tuple(values['position']))

    @staticmethod
    def build(level, entity_values):
        entity_kind = entity_values['name']

        if entity_kind not in LevelEntity.Factories:
            warnings.warn(f"No factory found for {entity_kind}! Will be ignored and lost")
            return None

        factory = LevelEntity.Factories[entity_kind]

        return factory(level, entity_values)

    @staticmethod
    def register_factory(cls, factory):
        name = cls.__name__

        if name in LevelEntity.Factories.keys():
            warnings.warn(f"'name' already had a registered factory. It will be replaced")

        LevelEntity.Factories[name] = factory
