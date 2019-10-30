from entities.entity import Entity, Layer
from entities.characters.behaviors import Interactive, SimpleMovement
from entities.characters.level_entity import MovementParameters
from util import world_to_screen, mario_str_to_pixel_value_acceleration as mstpva
from ..effects import MarioTransformSuper
from scoring import labels

mushroom_movement = MovementParameters(50, 50, 0., 0., mstpva('04000'))


class Mushroom(Entity):
    def __init__(self, level, position):
        self.animation = level.asset_manager.pickup_atlas.load_static("mushroom_red")

        super().__init__(self.animation.image.get_rect())

        self.level = level
        self.pickup = Interactive(level, self, (0, 0), (16, 16), self.on_collected)
        self.movement = SimpleMovement(self, level.collider_manager, mushroom_movement)
        self.movement.movement_collider.mask = Layer.Block  # exclude enemies

        self.position = position

    def update(self, dt, view_rect):
        self.movement.update(dt)
        self.pickup.update(dt)

    def draw(self, screen, view_rect):
        super().draw(screen, view_rect)

        screen.blit(self.animation.image, world_to_screen(self.position, view_rect))

        self.movement.draw(screen, view_rect)
        self.pickup.draw(screen, view_rect)

    def on_collected(self, collision):
        self.level.entity_manager.unregister(self)
        labels.Labels.points += 1000

        print("mushroom collected!")

        MarioTransformSuper.apply_transform(self.level, self.level.mario)
