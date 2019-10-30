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


class MarioTransformSmall(GameState):
    def __init__(self, level, mario):
        super().__init__(None)

        self.running_game = state_stack.top

        self.level = level
        self.mario = mario

        atlas = level.asset_manager.character_atlas

        facing = 1 if mario.movement.is_facing_right else 0

        little_mario = ["mario_stand_left", "mario_stand_right"][facing]
        middle = ["super_mario_transform_left", "super_mario_transform_right"][facing]
        super_mario = ["super_mario_stand_left", "super_mario_stand_right"][facing]

        little_mario = atlas.load_static(little_mario)
        middle = atlas.load_static(middle)
        super_mario = atlas.load_static(super_mario)

        # tweak little mario frame size to match super mario
        fixed_little = super_mario.image.copy()
        fixed_little.fill(config.transparent_color)
        fixed_little.blit(little_mario.image, (0, little_mario.image.get_height()))
        fixed_little = fixed_little.convert()

        powerup = level.asset_manager.sounds['downgrade']

        self.animation = self.build_animation(powerup.get_length(), fixed_little, middle.image, super_mario.image)
        mario.enabled = False

        self._finished = False

        # since we're positioning by top-left corner and super mario is larger than small mario,
        # we need a corrective offset to apply to mario's position once the effect is over
        self._offset = make_vector(0, little_mario.image.get_height())

        powerup.play()

    def update(self, dt):
        # don't update running game
        self.animation.update(dt)

    def draw(self, screen):
        self.running_game.draw(screen)
        screen.blit(self.animation.image, world_to_screen(self.mario.position, self.level.view_rect))

    def deactivated(self):
        self.mario.effects = MarioEffects.Small  # mario loses all abilities

        # period of invincibility
        self.mario.make_invincible(.75)  # todo: put in a config somewhere

        # the top-left coordinate of mario needs to be moved to account for a smaller sprite
        self.mario.position = self.mario.position + self._offset
        self.mario.enabled = True
        self.mario.input_state.reset()

    def build_animation(self, duration, small, middle, large):
        frames = []
        pieces = [large, middle, small]

        for x in range(0, 9):
            # triple up on frames so we can make the animation appear to move faster just before it finishes
            frames.append(pieces[x % len(pieces)])
            frames.append(pieces[x % len(pieces)])
            frames.append(pieces[x % len(pieces)])

        pieces = [middle, small]

        for x in range(0, 6):
            frames.append(pieces[x % len(pieces)])
            frames.append(pieces[x % len(pieces)])

        frames.append(middle)
        frames.append(small)

        return OneShotAnimation(frames, duration, self._animation_finished)

    def _animation_finished(self):
        self._finished = True

    @property
    def finished(self):
        return self._finished

    @staticmethod
    def apply_transform(level, mario):
        transform = MarioTransformSmall(level, mario)
        state_stack.push(transform)
