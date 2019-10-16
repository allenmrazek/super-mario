from pygame import Vector2
from .game_state import GameState
from entities.block import Block
from entities.entity import EntityManager
from entities.collider import ColliderManager
from entities.test_entities import BouncingBall
from tileset import TileSet
import config
from util import make_vector


class TestBlockPhysics(GameState):
    def __init__(self, input_state):
        super().__init__(input_state)

        self.colliders = ColliderManager()
        self.entity_mgr = EntityManager()

        # load tileset
        tileset = TileSet("NES - Super Mario Bros - Tileset.png", 16)

        # create row of blocks along bottom of screen
        y_pos = config.screen_rect.height - tileset.dimensions[1]

        blocks = [Block(make_vector(x_pos, y_pos), tileset, 1, self.colliders)
                  for x_pos in range(0, config.screen_rect.height, tileset.dimensions[0])]

        y_pos = 0

        blocks.extend([Block(make_vector(x_pos, y_pos), tileset, 1, self.colliders)
                       for x_pos in range(0, config.screen_rect.height, tileset.dimensions[0])])

        for block in blocks:
            self.entity_mgr.register(block)

        # create a bouncing ball
        bb = BouncingBall(self.colliders, config.screen_rect.center, make_vector(0., 175.))
        self.entity_mgr.register(bb)

    def update(self, dt):
        self.entity_mgr.update(dt)

    def draw(self, screen):
        screen.fill((120, 120, 120))
        self.entity_mgr.draw(screen)

    @property
    def finished(self):
        return False
