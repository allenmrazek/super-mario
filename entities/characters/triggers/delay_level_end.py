from ..level_entity import LevelEntity
import constants
from util import world_to_screen


class DelayLevelEnd(LevelEntity):
    DELAY = 6.

    def __init__(self, level, duration=None):
        self.animation = level.asset_manager.gui_atlas.load_static("level_end_trigger")

        super().__init__(self.animation.get_rect())

        self.level = level
        self.duration = duration or DelayLevelEnd.DELAY

    def update(self, dt, view_rect):
        self.duration -= dt

        if self.duration < 0.:
            self.level.set_cleared()

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

    def destroy(self):
        super().destroy()
        self.level.entity_manager.unregister(self)

    def create_preview(self):
        return self.animation.image.copy()

    @property
    def layer(self):
        return constants.Trigger


LevelEntity.create_generic_factory(DelayLevelEnd)
