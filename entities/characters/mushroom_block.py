from .level_entity import LevelEntity
from util import make_vector
from util import world_to_screen
from entities.entity import Entity
import config
import entities.collider
from .spawn_block import SpawnBlock
import entities.characters.mushroom
import constants


class _RisingMushroom(Entity):
    def __init__(self, level):
        pickup_atlas = level.asset_manager.pickup_atlas
        self.animation = pickup_atlas.load_static("mushroom_red")

        super().__init__(self.animation.rect)

        # calculate velocity such that we rise one block at the exact time the powerup sound would end
        # we won't just spawn there though, in case there are other blocks that would stop the mushroom from moving
        appears = level.asset_manager.sounds['powerup_appears']

        self.velocity = make_vector(0, -16 * config.rescale_factor / appears.get_length())
        self.collider = entities.collider.Collider.from_entity(self, level.collider_manager, constants.Block)
        self.level = level

    def update(self, dt, view_rect):
        self.animation.update(dt)
        self.position = self.position + self.velocity * dt

        # rise until we're clear of blocks
        self.collider.position = self.position

        if not self.collider.test(self.position):
            # not hitting anything -> ready to spawn
            mushroom = entities.characters.mushroom.Mushroom(self.level, self.position)
            self.level.entity_manager.register(mushroom)

            self.destroy()

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

    def destroy(self):
        self.level.entity_manager.unregister(self)

    @property
    def layer(self):
        return constants.Background


class MushroomBlock(SpawnBlock):
    def __init__(self, level):
        super().__init__(level)
        patlas = self.level.asset_manager.pickup_atlas

        self.mushroom = patlas.load_static("mushroom_red")

    def smashed(self):
        # spawn a mushroom "ghost", which appears from behind the blocks and rises up. Won't be interactive until
        # it's clear of any collisionis
        self.level.asset_manager.sounds['powerup_appears'].play()
        self._smashed = True
        self.animation = self.empty

        rising_mushroom = _RisingMushroom(self.level, self.position)

        self.level.entity_manager.register(rising_mushroom)

    def create_preview(self):
        block = super().create_preview()
        block.blit(self.mushroom.image, (0, 0))

        return block

    def destroy(self):
        super().destroy()


LevelEntity.create_generic_factory(MushroomBlock)
