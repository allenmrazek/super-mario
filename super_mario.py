import os
import pygame
from state.game_state import GameStateStack
from state.input_state import InputState
from state.test_mario_physics import TestMarioPhysics
import config
from timer import game_timer


def run():
    # initialize PyGame
    pygame.init()
    screen = pygame.display.set_mode(config.screen_size)
    pygame.display.set_caption("Super Mario")

    # initialize states
    input_state = InputState()
    state_stack = GameStateStack(TestMarioPhysics(input_state))
    game_timer.reset()

    # timer initialize
    accumulator = 0.0

    while state_stack.top is not None and not input_state.quit:
        input_state.do_events()
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