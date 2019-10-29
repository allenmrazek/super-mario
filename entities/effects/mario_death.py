import pygame
from entities.entity_manager import Entity
from util import make_vector, mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from util import world_to_screen
from event import EventHandler
from state import state_stack
from entities.entity import Layer


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
            self.level.spawn_mario()

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
        return Layer.Active

