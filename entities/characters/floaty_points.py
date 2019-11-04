import pygame
from .corpse import Corpse
from util import world_to_screen, make_vector
from util import mario_str_to_pixel_value_velocity as mstpvv
from util import mario_str_to_pixel_value_acceleration as mstpva
from ..entity import Entity
from .parameters import CharacterParameters

floaty_font = None
floaty_parameters = CharacterParameters(0., mstpvv('01500'), 0., mstpvv('00950'), 0.)


class FloatyPoints(Corpse):
    DURATION = 0.33

    def __init__(self, level, points):
        if isinstance(points, int):
            points = str(points)

        global floaty_font
        from animation import StaticAnimation

        # lazy load font
        floaty_font = floaty_font or pygame.font.Font("scoring/super_mario_font.ttf", 12)

        frame = floaty_font.render(points, True, pygame.Color('white'))

        animation = StaticAnimation(frame)

        super().__init__(level, animation, floaty_parameters, FloatyPoints.DURATION, True)

    @staticmethod
    def display(level, points, position):
        floaty = FloatyPoints(level, points)
        floaty.movement.velocity = make_vector(0., -floaty_parameters.jump_velocity)

        # if given an entity, start the points out just above the entity
        if isinstance(position, Entity):
            r = position.rect
            fr = floaty.rect
            fr.bottom = r.top
            fr.centerx = r.centerx

            position = make_vector(fr.left, fr.top)

        floaty.position = position
        level.entity_manager.register(floaty)

        return floaty
