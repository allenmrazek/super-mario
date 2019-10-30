import pygame
from entities.entity_manager import Entity
from util import make_vector, mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from util import world_to_screen
from event import EventHandler
from state import state_stack
import state.level_begin
import state.run_session
import entities.characters.mario
import constants

"""Death animation:

Stay in place 0.25 seconds
Apply upward velocity roughly equivalent to 4 tiles of jump height
pass off bottom of screen
remove effect
respawn mario
"""


class MarioDeath(Entity, EventHandler):
    FREEZE_LENGTH = 0.25  # in seconds
    VELOCITY = mstpvv('04000')
    GRAVITY = mstpva('00200')

    def __init__(self, level, position):
        self.animation = level.asset_manager.character_atlas.load_static("mario_dead")

        super().__init__(self.animation.get_rect())

        self.level = level
        self.position = position

        self._elapsed = 0.
        self._applied_jump = False
        self._velocity = make_vector(0, 0)
        self._finished = False

        # play death music
        pygame.mixer_music.load('sounds/music/smb_mariodie.wav')
        pygame.mixer_music.set_endevent(pygame.USEREVENT)

        pygame.mixer_music.play()

        state_stack.top.game_events.register(self)

    def update(self, dt, view_rect):
        self._elapsed += dt

        if not self._applied_jump and self._elapsed > MarioDeath.FREEZE_LENGTH:
            # apply jump
            self._velocity.y = -MarioDeath.VELOCITY
            self._applied_jump = True

        if self._applied_jump:
            self._velocity.y += MarioDeath.GRAVITY * dt

        self.position = self.position + self._velocity * dt

        if self._finished:
            self.level.entity_manager.unregister(self)

            # Decrement live counter
            self.level.stats.lives -= 1

            # if have more lives, display world start again
            if self.level.stats.lives > 0:
                # reset any state mario might have had
                self.level.mario.effects = entities.characters.mario.MarioEffects.Small

                # kludgy :( no time to do it the nice way though
                run_session = state_stack.top

                while run_session is not None and not isinstance(run_session, state.run_session.RunSession):
                    run_session = state_stack.get_next(run_session)

                state_stack.push(state.level_begin.LevelBegin(
                    self.level.asset_manager, self.level, run_session.scoring_labels,
                    self.level.stats))

                # also resetore level state...
                self.level.reset()

    def draw(self, screen, view_rect):
        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

    def handle_event(self, evt, game_events):
        # only event we care about is the end of sound one
        if evt.type == pygame.USEREVENT:
            self._finished = True
            pygame.mixer_music.set_endevent()
            state_stack.top.game_events.unregister(self)

    @property
    def layer(self):
        return constants.Active
