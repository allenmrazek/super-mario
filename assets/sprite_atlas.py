import os
import copy
import pygame
from animation import Animation
from animation import StaticAnimation
from entities.gui.sliced_image import SlicedImage
import config

# if rescale is not a factor of 2, sprites will have fuzzy edges that will look terrible with color keying
assert config.rescale_factor % 2 == 0, "factor must be a multiple of 2"
assert isinstance(config.rescale_factor, int), "factor must be an int value"


class SpriteAtlasError(Exception):
    def __init__(self, name):
        super().__init__()
        self.name = name


class SpriteNotFoundError(SpriteAtlasError):
    def __init__(self, sprite_name):
        super().__init__(sprite_name)


class InvalidDimensionsError(SpriteAtlasError):
    def __init__(self, name, rect, wh):
        super().__init__(name)
        self.rect = rect
        self.dimensions = wh


class SpriteAtlas:
    """An atlas is a grouped set of surfaces. By itself, it doesn't do much
    more than read the main surface into memory along with a txt file that describes
    the surfaces contained within the atlas. This information can be used to create
    specific Animation instances for later use by calling appropriate methods on the atlas"""
    def __init__(self, atlas_path=None, tf_use_rescale_factor=True, convert=True):
        # use the descriptor file to load subsurfaces
        self.sprite_rects = {}

        if atlas_path is not None and len(atlas_path) > 0:
            # locate atlas descriptor
            basename = os.path.splitext(atlas_path)[0]
            atlas_descriptor = basename + '.txt'

            if not os.path.exists(atlas_descriptor) or not os.path.exists(atlas_path):
                raise FileNotFoundError(atlas_descriptor)

            self.atlas = pygame.image.load(atlas_path)

            if not self.atlas:
                raise FileNotFoundError(atlas_path)

            if tf_use_rescale_factor:
                # apply rescaling
                # rescale without resampling
                scaled_size = (self.atlas.get_width() * config.rescale_factor,
                               self.atlas.get_height() * config.rescale_factor)

                self.atlas = self.atlas \
                    if config.rescale_factor == 1 else pygame.transform.scale(self.atlas, scaled_size)

                self.rescale_factor = config.rescale_factor
            else:
                self.rescale_factor = 1

            file = open(atlas_descriptor, 'r')

            if not file:
                raise FileNotFoundError(atlas_descriptor)

            for line in file:
                # of the form: name = left top width height
                name, rect_str = [s.strip() for s in line.split('=')]
                rect = self._get_rect_from_str(rect_str)

                # apply rescale factor
                rect.x *= self.rescale_factor
                rect.y *= self.rescale_factor
                rect.width *= self.rescale_factor
                rect.height *= self.rescale_factor

                # add sprite to dictionary
                self.sprite_rects[name] = rect
        else:
            self.__sprite_rects = {}
            self.atlas = None

        self.animations = {}
        self.statics = {}  # statics aren't initialized to anything by default so user can specify color key if wanted
        self.sliced = {}

        if convert and self.atlas is not None:
            self.atlas = self.atlas.convert()

    @property
    def sprite_names(self):
        return list(self.sprite_rects.keys())

    def initialize_animation(self, name, frame_width, frame_height, duration, color_key=None):
        if name in self.animations:
            return self.animations[name]

        # grab rect for this name
        if name not in self.sprite_rects:
            raise SpriteNotFoundError(name)

        rect = self.sprite_rects[name]

        frame_height = frame_height or frame_width

        if rect.width % frame_width != 0 or rect.height % frame_height != 0:
            raise InvalidDimensionsError(name, rect, (frame_width, frame_height))

        frames = [self.atlas.subsurface(
            pygame.Rect(x, y, frame_width, frame_height))
            for y in range(rect.y, rect.y + rect.height, frame_height)
            for x in range(rect.x, rect.x + rect.width, frame_width)]

        if color_key is not None:
            # cannot use per-pixel alpha values in this case
            converted = [s.convert() for s in frames]
            frames = converted

            for f in frames:
                f.set_colorkey(color_key)

        animation = Animation(frames, duration)

        self.animations[name] = animation

    def initialize_static(self, name, color_key=None, override_width=None, override_height=None):
        rect = self._fetch(name, self.sprite_rects)

        if override_width or override_height:
            rect = rect.copy()  # don't affect original dimensions

        rect.width = override_width or rect.width
        rect.height = override_height or rect.height

        assert 0 <= rect.width <= self.atlas.get_width(), "width out of range"
        assert 0 <= rect.height <= self.atlas.get_height(), "height out of range"

        assert 0 <= rect.x <= self.atlas.get_width() - rect.width, "x position out of range"
        assert 0 <= rect.y <= self.atlas.get_height() - rect.height, "y position out of range"

        surf = self.atlas.subsurface(rect)

        if color_key is not None:
            surf = surf.convert()
            surf.set_colorkey(color_key)

        self.statics[name] = StaticAnimation(surf)

    def initialize_static_from_surface(self, name, surf):
        self.statics[name] = StaticAnimation(surf)

    def initialize_animation_from_frames(self, name, frames, duration):
        assert len(frames) > 0

        self.animations[name] = Animation(frames, duration)

    def initialize_slice_from_surface(self, name, surf, dims):
        self.sliced[name] = SlicedImage(surf, dims)

    def initialize_slice(self, name, slice_size, color_key=None):
        assert len(slice_size) == 2

        if name not in self.sprite_rects:
            raise SpriteNotFoundError(name)

        # todo: check for double-initialization?

        rect = self.sprite_rects[name]
        slice_img = self.atlas.subsurface(rect)

        # this surface must be at LEAST 24 bit or else scaling will fail
        if slice_img.get_bitsize() < 24:
            slice_img = slice_img.convert(24)

        if color_key is not None:
            slice_img = slice_img.convert()
            assert slice_img.get_bitsize() >= 24  # just to catch unexpected edge cases

            slice_img.set_colorkey(color_key)

        self.sliced[name] = SlicedImage(slice_img, slice_size)

    def load_static(self, name):
        return copy.copy(self._fetch(name, self.statics))

    def load_animation(self, name):
        return copy.copy(self._fetch(name, self.animations))

    def load_sliced(self, name):
        return copy.copy(self._fetch(name, self.sliced))

    def __add__(self, other):
        assert other is not self, "adding atlas to itself makes no sense"

        # create a new atlas that combines the two previous atlas
        # in this special case, we want shallow copies because it's likely the two atlases to be added
        # are about to be thrown away

        def get_names(an_atlas):
            sprite_names = set()

            for li in [an_atlas.sliced, an_atlas.statics, an_atlas.animations, an_atlas.sprite_rects]:
                for key_name in li.keys():
                    sprite_names.add(key_name)

            return sprite_names

        # check for duplicate names and warn if any are found, because it may cause the atlas to choose
        # the wrong sprites
        intersections = get_names(self).intersection(get_names(other))

        for inter in intersections:
            print(f"Warning! Two sprites named '{inter}' in atlases to be combined; consider renaming one of the sprites")

        new_atlas = SpriteAtlas()

        for new_d, our_d, other_d in [(new_atlas.sprite_rects, self.sprite_rects, other.sprite_rects),
                  (new_atlas.statics, self.statics, other.statics),
                  (new_atlas.animations, self.animations, other.animations),
                  (new_atlas.sliced, self.sliced, other.sliced)]:
            new_d.update(our_d)
            new_d.update(other_d)

        return new_atlas

    def scale(self, new_size):
        if new_size is not tuple:
            new_size = (new_size, new_size)

        self.atlas = pygame.transform.scale(self.atlas, new_size)

        # modify all sprite rects
        old_rects = self.sprite_rects
        self.sprite_rects = {}

        # rather than come up with fancy logic to re-create all the sprites, or just to resize them (since that
        # will result in doubling memory use), just assume this will be an operation that happens before any
        # initializing of sprites and warn if it doesn't
        if len(self.statics) > 0 or len(self.animations) > 0 or len(self.sliced) > 0:
            print("Warning! Scaling an atlas will result in all initialized sprites being lost")

        self.statics = {}
        self.animations = {}
        self.sliced = {}

        for name, rect in old_rects:
            nr = pygame.Rect(rect.x * new_size[0], rect.y * new_size[1],
                             rect.width * new_size[0], rect.height * new_size[1])
            self.sprite_rects[name] = nr

    @staticmethod
    def _fetch(name, location):
        name = name.strip()

        if name not in location:
            print("could not find sprite '{}' in atlas".format(name))
            raise SpriteNotFoundError(name)
        return location[name]

    @staticmethod
    def _get_rect_from_str(rect_str):
        r = pygame.Rect(0, 0, 0, 0)

        r.left, r.top, r.width, r.height = [int(x) for x in rect_str.split(' ')]

        return r
