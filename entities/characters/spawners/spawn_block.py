from abc import abstractmethod
from ..level_entity import LevelEntity
from util import world_to_screen
from ..behaviors.smashable import Smashable
import constants


class SpawnBlock(LevelEntity):
    def __init__(self, level):
        self.level = level
        iatlas = level.asset_manager.interactive_atlas

        self.animation = iatlas.load_animation("coin_block_ow")
        self.empty = iatlas.load_static("coin_block_empty_ow")

        super().__init__(self.empty.get_rect())

        # note: Smashable assumes we're passing in UNSCALED values, so don't use our own rect size
        self.smashable = Smashable(level, self, self._on_smashed)
        self._smashed = False

    def _on_smashed(self):
        if not self._smashed:
            self.smashed()
        # otherwise, already smashed this block

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.smashable.update(dt)
        self.animation.update(dt)

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))
        self.smashable.draw(screen, view_rect)

    @abstractmethod
    def smashed(self):
        pass

    def destroy(self):
        self.level.entity_manager.unregister(self)
        self.smashable.destroy()

    @abstractmethod
    def create_preview(self):
        return self.animation.image.copy()

    @property
    def layer(self):
        return constants.Block
