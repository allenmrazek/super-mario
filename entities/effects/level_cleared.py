from entities.characters.mario import MarioEffectStar, MarioEffectFire, MarioEffectSuper, MarioEffectSmall
from state.game_state import GameState
from event.game_events import GameEvents
import pygame
from util import make_vector
from util import world_to_screen
import entities.characters.triggers.flag
import entities.characters.mario

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

        self.game_events.register(self)

        # locate the pole
        self.pole = self.level.entity_manager.search_by_type(entities.characters.triggers.flag.Flag)[0]

        # hide mario
        self.mario = self.level.mario
        self.mario_input = self.mario.movement.input_state
        self.mario.enabled = False

        # put a doppelganger where he would be on the pole
        self.doppler = self._create_doppleganger(self.mario)
        self.doppler.position = make_vector(self.pole.position.x - self.doppler.rect.width // 3,
                                            self.level.mario.position.y)

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

                # drop mario and make him move right
                self.mario.position = make_vector(self.pole.position.x, self.doppler.position.y)
                self.mario.reset()
                self.mario.enabled = True
                self.mario.movement.input_state = _FakeInput()

                # now wait for fake mario to reach castle
                # a trigger should be set up to hide him or move into a pipe

            self.mario.update(dt, self.level.view_rect)
            self.level.update_triggers_only(dt)

    def draw(self, screen):
        self.game_state.draw(screen)

        if not self.waiting:
            screen.blit(self.doppler.image, world_to_screen(self.doppler.position, self.level.view_rect))
        else:
            if self.mario.enabled:
                self.mario.draw(screen, self.level.view_rect)

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

    @property
    def finished(self):
        return self._finished

    def deactivated(self):
        pygame.mixer_music.set_endevent()
        self.mario.movement.input_state = self.mario_input  # restore mario's input handler
        self.mario.movement.input_state.reset()
        self.level.set_cleared()
