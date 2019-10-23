import os
import pygame
from event import GameEvents
from state import GameState, GameStateStack
from timer import game_timer
from tools.TileExtractor.run_state import RunState
import config

"""Improved version of tileset generator which is used to classify new tiles as they're found"""


def run():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    screen = pygame.display.set_mode(config.screen_size)
    pygame.display.set_caption("Tile Extractor")

    import atlas

    real_get_atlas_path = atlas.get_atlas_path

    def editor_path(atlas_name):
        return os.path.join("../../", real_get_atlas_path(atlas_name))

    atlas.load.get_atlas_path = editor_path

    sprite_atlas = atlas.load_gui_atlas()

    # initialize states
    game_events = GameEvents()

    state_stack = GameStateStack()
    state_stack.push(RunState(game_events, sprite_atlas))

    game_events.register(state_stack.top)
    game_timer.reset()

    accumulator = 0.0

    while state_stack.top is not None:
        game_events.do_events()
        game_timer.update()

        accumulator += game_timer.elapsed

        while accumulator > config.PHYSICS_DT:
            state_stack.update(config.PHYSICS_DT)
            accumulator -= config.PHYSICS_DT

        state_stack.draw(screen)
        pygame.display.flip()

    exit(0)


run()
