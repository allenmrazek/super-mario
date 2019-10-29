from pygame import Rect
from entities.characters import LevelEntity
from ..behaviors import Interactive
from util import world_to_screen
from entities.entity import Layer


class LevelWarp(LevelEntity):
    SIZE = (64, 64)

    def __init__(self, level):
        self.animation = level.asset_manager.gui_atlas.load_static("level_warp")
        self.level = level
        self.next_level_file = "warp1.level"

        super().__init__(Rect(0, 0, *LevelWarp.SIZE))

        self.trigger = Interactive(level, self, (0, 0), LevelWarp.SIZE, self._change_level)
        self._launch = False

    def _change_level(self, collision):
        self.level.load_from_path("levels/" + self.next_level_file)
        self.destroy()

    def update(self, dt, view_rect):
        super().update(dt, view_rect)

        self.trigger.update(dt)

        if self._launch:
            self.level.load_from_path("levels/" + self.next_level_file)
            self.destroy()

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        self.trigger.draw(screen, view_rect)

        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

    def destroy(self):
        self.level.entity_manager.unregister(self)
        self.trigger.destroy()

    def create_preview(self):
        return self.animation.image.copy()

    @property
    def layer(self):
        return Layer.Trigger


def make_level_change(level, values):
    lc = LevelWarp(level)

    if values is not None:
        lc.deserialize(values)

    return lc


LevelEntity.register_factory(LevelWarp, make_level_change)
