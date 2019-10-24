from .entity import Layer
from .drawable import Drawable
from .collider import Collider


class Block(Drawable):
    def __init__(self, position, animation, cmanager):
        assert cmanager is not None

        super().__init__(position, animation)

        self.collider = Collider.from_entity(self, cmanager, 0)
        cmanager.register(self.collider)

    @property
    def collision_mask(self):
        return 0

    @property
    def layer(self):
        return Layer.Block

    # need to override position to propagate any changes to block's collider
    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, new_pos):
        super(Block, self.__class__).position.fset(self, new_pos)

        # todo: better solution to resolve circular properties?
        if hasattr(self, "collider"):
            self.collider.position = new_pos
