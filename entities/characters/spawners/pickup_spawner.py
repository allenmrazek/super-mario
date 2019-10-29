from ..level_entity import LevelEntity
from util import world_to_screen
from entities.entity import Layer
from entities.characters.mushroom import Mushroom
from util import world_to_screen, make_vector
import config


# just used as convenient testing mechanism
class PickupSpawner(LevelEntity):
    def __init__(self, level):
        self.level = level

        self.image = level.asset_manager.pickup_atlas.load_static("mushroom_red").image

        super().__init__(self.image.get_rect())

    def update(self, dt, view_rect):
        mushroom = Mushroom(self.level, self.position)

        self.level.entity_manager.register(mushroom)
        self.level.entity_manager.unregister(self)

    def draw(self, screen, view_rect):
        # needed to see it in editor
        screen.blit(self.image, world_to_screen(self.position, view_rect))

    @property
    def layer(self):
        return Layer.Spawner

    def create_preview(self):
        return self.image

    def destroy(self):
        self.level.entity_manager.unregister(self)

    @staticmethod
    def factory(level, values):
        spawn = PickupSpawner(level)

        if values is not None:
            spawn.deserialize(values)

        return spawn


LevelEntity.register_factory(PickupSpawner, PickupSpawner.factory)
