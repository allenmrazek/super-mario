import os
import pygame
from state.game_state import GameStateStack
from state.physics_test import PhysicsTest
from state.input_state import InputState

import config
from timer import game_timer


def run():
    # initialize PyGame
    pygame.init()
    screen = pygame.display.set_mode(config.screen_size)
    pygame.display.set_caption("Super Mario")

    # initialize states
    input_state = InputState()
    state_stack = GameStateStack(PhysicsTest())
    game_timer.reset()

    while state_stack.top is not None and not input_state.quit:
        input_state.do_events()
        game_timer.update()
        state_stack.update(input_state, game_timer.elapsed)

        state_stack.draw(screen)
        pygame.display.flip()

    exit(0)


run()