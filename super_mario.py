import os
import pygame
from event.game_events import EventHandler
from state.game_state import state_stack
from state import MainMenu
import config
from timer import game_timer
from assets import AssetManager


class _QuitListener(EventHandler):
    def handle_event(self, evt, game_events):
        if evt.type == pygame.QUIT or\
                (not self.is_consumed(evt) and evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE):
            exit(0)


def run():
    # initialize PyGame
    if pygame.mixer:
        pygame.mixer.pre_init(22050, -16, 2, 1024)

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    screen = pygame.display.set_mode(config.screen_size)
    pygame.display.set_caption("Super Mario")
    assets = AssetManager()

    state_stack.push(MainMenu(assets))

    game_timer.reset()

    # timer initialize
    accumulator = 0.0

    #Level.take_snapshot(assets, EntityManager.create_editor(), 'levels/level11.level', 'captured.png')

    while state_stack.top is not None:
        state_stack.top.do_events()
        game_timer.update()

        # todo: fixed time step, or max time step?
        accumulator += game_timer.elapsed
        accumulator = min(0.20, accumulator)
        while accumulator > config.PHYSICS_DT:
            state_stack.update(config.PHYSICS_DT)
            accumulator -= config.PHYSICS_DT

        state_stack.draw(screen)
        pygame.display.flip()

    exit(0)


run()
