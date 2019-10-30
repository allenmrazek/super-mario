import pygame
from entities.entity_manager import Entity
from util import make_vector, mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from util import world_to_screen
from entities.characters.mario import MarioEffects
from state.game_state import GameState, state_stack
from animation import Animation, OneShotAnimation
from util import world_to_screen
from event.game_events import GameEvents, EventHandler
import config
import pygame
from entities.entity_manager import Entity
from util import make_vector, mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from util import world_to_screen
from event import EventHandler
from state import state_stack
from entities.entity import Layer
import entities.characters.triggers.flag
import entities.characters.mario
import event.player_input

"""
Jumps on pole, left side
flag slides down
Mario switches side
gets off pole, walks into castle
"""


class _FakeInput:
    def __init__(self):
        self.right = True
        self.left, self.up, self.down, self.fire, self.jump, self.dash = False, False, False, False, False, False


class LevelCleared(GameState):
    FLAG_SLIDE_TIME = .75  # in seconds

    def __init__(self, level, game_state):
        super().__init__(GameEvents())

        self.level = level
        self.game_state = game_state

        self._elapsed = 0.
        self._applied_jump = False
        self._velocity = make_vector(0, 0)
        self._finished = False

        # play clear music
        pygame.mixer_music.load('sounds/music/smb_stage_clear.wav')
        pygame.mixer_music.set_endevent(pygame.USEREVENT)

        pygame.mixer_music.play()

        #state_stack.top.game_events.register(self)
        self.game_events.register(self)

        # locate the pole
        self.pole = self.level.entity_manager.search_by_type(entities.characters.triggers.flag.Flag)[0]

        # hide mario
        self.level.mario.enabled = False

        # create another mario that we'll control ourselves
        self.fake_input = event.player_input.PlayerInputHandler()
        self.fake_mario = entities.characters.mario.Mario(_FakeInput(), self.level)
        self.fake_mario.effects = self.level.mario.effects
        self.fake_mario.enabled = False

        # put a doppelganger where he would be on the pole
        self.doppler = self._create_doppleganger(self.fake_mario)
        self.doppler.position = make_vector(self.pole.position.x - self.doppler.rect.width // 3, self.level.mario.position.y)

        # keep track of state
        self.waiting = False

    def update(self, dt):
        self._elapsed += dt

        if self._elapsed < LevelCleared.FLAG_SLIDE_TIME:
            flag_ratio = self._elapsed / LevelCleared.FLAG_SLIDE_TIME
            self.pole.set_flag_position(flag_ratio)
        else:
            if not self.waiting:
                self.waiting = True

                self.pole.set_flag_position(1.0)

                # activate fake mario, drop him from the pole and make him move right
                self.fake_input.right = True
                self.fake_mario.position = make_vector(self.pole.position.x, self.doppler.position.y)
                self.fake_mario.enabled = True

                # now wait for fake mario to reach castle
                # todo

            self.fake_mario.update(dt, self.level.view_rect)

    def draw(self, screen):
        self.game_state.draw(screen)

        if not self.waiting:
            screen.blit(self.doppler.image, world_to_screen(self.doppler.position, self.level.view_rect))
        else:
            self.fake_mario.draw(screen, self.level.view_rect)

    def _create_doppleganger(self, fake):
        ca = self.level.asset_manager.character_atlas

        if fake.effects & MarioEffects.Super:
            # super variant
            if fake.effects & MarioEffects.Fire:
                return ca.load_static("super_mario_fire_pole_right")
            elif fake.effects & MarioEffects.Star:
                raise NotImplementedError
            else:  # just super mario
                return ca.load_static("super_mario_pole_right")
        else:
            # small variants
            if fake.effects & MarioEffects.Fire:
                return ca.load_static("mario_fire_pole_right")
            elif fake.effects & MarioEffects.Star:
                raise NotImplementedError
            else:
                return ca.load_static("mario_pole_right")

    def handle_event(self, evt, game_events):
        # only event we care about is the end of sound one
        if evt.type == pygame.USEREVENT:
            self._finished = True
            pygame.mixer_music.set_endevent()
            state_stack.top.game_events.unregister(self)
            self.level.mario.input_state.reset()

    @property
    def finished(self):
        return self._finished

    def deactivated(self):
        self.level.set_cleared()
