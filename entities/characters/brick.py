from entities.characters.corpse import Corpse
from .level_entity import LevelEntity
from util import make_vector
from util import world_to_screen, get_aligned_foot_position
from .behaviors import Smashable
import constants


class Brick(LevelEntity):
    POINT_VALUE = 50

    def __init__(self, level, position):
        self.level = level
        self.image = level.asset_manager.interactive_atlas.load_static("brick").image
        self.destroyed = level.asset_manager.interactive_atlas.load_static("brick_debris")

        super().__init__(self.image.get_rect())

        self.position = position

        # note: Smashable assumes we're passing in UNSCALED values, so don't use our own rect size
        self.smashable = Smashable(level, self, self._on_smashed)

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.smashable.update(dt)

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.image, world_to_screen(self.position, view_rect))
        self.smashable.draw(screen, view_rect)

    def _on_smashed(self):
        mario = self.level.mario

        if mario.is_super:
            # destroy this brick
            self.die()
            self.level.stats.score += Brick.POINT_VALUE
        else:
            # mario can't break it, small movement instead
            self.level.asset_manager.sounds['bump'].play()

    def die(self):
        self.destroy()

        corpse = Corpse.\
            create_ghost_corpse_from_entity(self,
                                            self.level.asset_manager.interactive_atlas.load_static("brick_debris"),
                                            self.level, 0.1)

        self.level.asset_manager.sounds['breakblock'].play()

        corpse.position = get_aligned_foot_position(self.rect, corpse.rect)

        self.level.entity_manager.register(corpse)

    def destroy(self):
        self.smashable.destroy()
        self.level.entity_manager.unregister(self)

    def create_preview(self):
        return self.image.copy()

    @property
    def layer(self):
        return constants.Block


def make_brick(level, values):
    brick = Brick(level, make_vector(0, 0))

    if values is not None:
        brick.deserialize(values)

    return brick


LevelEntity.register_factory(Brick, make_brick)
