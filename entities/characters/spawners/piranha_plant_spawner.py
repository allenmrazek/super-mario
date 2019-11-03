from entities.characters.level_entity import LevelEntity
from entities.characters.piranha_plant import PiranhaPlant
from util import world_to_screen
import constants


class PiranhaPlantSpawner(LevelEntity):
    """Exists only to spawn a piranha plant in the level"""

    def __init__(self, level):
        self.mouth = level.asset_manager.character_atlas.load_animation("piranha_plant")
        self.level = level

        super().__init__(self.mouth.get_rect())

        self._spawned = False

    def update(self, dt, view_rect):
        if not self._spawned:
            plant = PiranhaPlant(self.level, self.rect)
            plant.position = self.position
            self.level.entity_manager.register(plant)

            self.destroy()

            self._spawned = True

    def draw(self, screen, view_rect):
        screen.blit(self.mouth.image, world_to_screen(self.position, view_rect))

    def create_preview(self):
        return self.mouth.image.copy()

    @property
    def layer(self):
        return constants.Spawner

    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, val):
        super(LevelEntity, self.__class__).position.fset(self, val)
        self.mouth.position = val

    def destroy(self):
        self.level.entity_manager.unregister(self)


LevelEntity.create_generic_factory(PiranhaPlantSpawner)