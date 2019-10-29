import os
import pygame
from event.game_events import GameEvents, EventHandler
from state.game_state import state_stack
from state import PerformanceMeasurement
from editor.editor_state import EditorState
from state import TestLevel
from assets.level import Level
import config
from timer import game_timer
from assets import AssetManager
from entities.gui.modal import ModalTextInput
from scoring import labels
from entities import entity_manager


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

    # initialize states
    game_events = GameEvents()
    #default_game_events.register(_QuitListener())


    #PerformanceMeasurement.measure(state_stack, TestMarioPhysics(game_events, atlas))
    #state_stack.push()
    PerformanceMeasurement.measure(state_stack, EditorState(None, assets))
    #state_stack.push(TestLevel(game_events, assets, Level(assets, entity_manager)))
    #PerformanceMeasurement.measure(state_stack, TestLevel(game_events, assets, Level(assets, entity_manager)))

    game_timer.reset()

    # timer initialize
    accumulator = 0.0

    # Labels for overhead information
    labels_ = labels.Labels(screen)
    labels_.prep_labels()
    labels_.prep_points()


    while state_stack.top is not None:
    #while True:
        state_stack.top.do_events()
        game_timer.update()

        # todo: fixed time step, or max time step?
        accumulator += game_timer.elapsed
        updated = False  # no interpolation, so don't waste time drawing screen if it didn't change anyways

        while accumulator > config.PHYSICS_DT:
            updated = True
            state_stack.update(config.PHYSICS_DT)
            accumulator -= config.PHYSICS_DT

        if updated:
            state_stack.draw(screen)
            labels_.show_labels()
            pygame.display.flip()

    exit(0)


run()
