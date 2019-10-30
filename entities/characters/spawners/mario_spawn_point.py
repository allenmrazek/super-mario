from ..level_entity import LevelEntity
from util import world_to_screen
import constants

class MarioSpawnPoint(LevelEntity):
    def __init__(self, level):
        self.level = level
        character_atlas = level.asset_manager.character_atlas
        self.image = character_atlas.load_static("mario_stand_right").image

        super().__init__(self.image.get_rect())

    def update(self, dt, view_rect):
        pass

    def draw(self, screen, view_rect):
        screen.blit(self.image, world_to_screen(self.position, view_rect))

    @property
    def layer(self):
        return constants.Spawner

    def create_preview(self):
        return self.image

    def destroy(self):
        super().destroy()

        self.level.entity_manager.unregister(self)

    @staticmethod
    def factory(level, values):
        spawn = MarioSpawnPoint(level)

        if values is not None:
            spawn.deserialize(values)

        return spawn


LevelEntity.register_factory(MarioSpawnPoint, MarioSpawnPoint.factory)
