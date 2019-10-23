import os
import pygame
from atlas import load_atlases
from event.game_events import GameEvents, EventHandler
from state.game_state import GameStateStack
from state.editor_state import EditorState
import config
from timer import game_timer
from state.test_gui import TestGui
from state.test_level import TestLevel


class _QuitListener(EventHandler):
    def handle_event(self, evt, game_events):
        if evt.type == pygame.QUIT or (evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE):
            exit(0)


def run():
    # initialize PyGame
    if pygame.mixer:
        pygame.mixer.pre_init(22050, -16, 2, 1024)

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    screen = pygame.display.set_mode(config.screen_size)
    pygame.display.set_caption("Super Mario")
    atlas = load_atlases()

    # initialize states
    game_events = GameEvents()
    game_events.register(_QuitListener())

    state_stack = GameStateStack()

    # PerformanceMeasurement.measure(state_stack, TestMarioPhysics(game_events, atlas))
    # state_stack.push(TestGui(game_events, atlas))
    #state_stack.push(EditorState(game_events, atlas))
    state_stack.push(TestLevel(game_events, atlas))

    game_timer.reset()

    # timer initialize
    accumulator = 0.0

    while state_stack.top is not None:
        game_events.do_events()
        game_timer.update()

        # todo: fixed timestep, or max timestep?
        accumulator += game_timer.elapsed

        while accumulator > config.PHYSICS_DT:
            state_stack.update(config.PHYSICS_DT)
            accumulator -= config.PHYSICS_DT

        state_stack.draw(screen)
        pygame.display.flip()

    exit(0)


run()
