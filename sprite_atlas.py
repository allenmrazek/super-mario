import os
import copy
import pygame
from animation import Animation
from animation import StaticAnimation
import config


class SpriteAtlasException(Exception):
    def __init__(self, name):
        super().__init__()
        self.name = name


class SpriteNotFoundException(SpriteAtlasException):
    def __init__(self, sprite_name):
        super().__init__(sprite_name)


class InvalidDimensionsException(SpriteAtlasException):
    def __init__(self, name, rect, wh):
        super().__init__(name)
        self.rect = rect
        self.dimensions = wh


class SpriteAtlas:
    def __init__(self, atlas_path=""):
        if len(atlas_path) > 0:
            # locate atlas descriptor
            basename = os.path.splitext(atlas_path)[0]
            atlas_descriptor = basename + '.txt'

            if not os.path.exists(atlas_descriptor) or not os.path.exists(atlas_path):
                raise FileNotFoundError

            self.atlas = pygame.image.load(atlas_path)

            if not self.atlas:
                raise RuntimeError

            file = open(atlas_descriptor, 'r')

            if not file:
                raise RuntimeError

            # use the descriptor file to load subsurfaces
            self._sprite_rects = {}

            for line in file:
                # of the form: name = left top width height
                name, rect_str = [s.strip() for s in line.split('=')]
                rect = self._get_rect_from_str(rect_str)

                # add sprite to dictionary
                self._sprite_rects[name] = rect
        else:
            self.__sprite_rects = {}

        self.animations = {}
        self.statics = {}  # statics aren't initialized to anything by default so user can specify color key if wanted

    @property
    def sprite_names(self):
        return list(self._sprite_rects.keys())

    def initialize_animation(self, name, frame_width, frame_height, duration, color_key=None):
        if name in self.animations:
            return self.animations[name]

        # grab rect for this name
        if name not in self._sprite_rects:
            raise SpriteNotFoundException(name)

        rect = self._sprite_rects[name]

        frame_height = frame_height or frame_width

        if rect.width % frame_width != 0 or rect.height % frame_height != 0:
            raise InvalidDimensionsException(name, rect, (frame_width, frame_height))

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
        rect = self._fetch(name, self._sprite_rects)

        if override_width or override_height:
            rect = rect.copy()  # don't affect original dimensions

        rect.width = override_width or rect.width
        rect.height = override_height or rect.height

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

    def load_static(self, name):
        return copy.copy(self._fetch(name, self.statics))

    def load_animation(self, name):
        return copy.copy(self._fetch(name, self.animations))

    @staticmethod
    def _fetch(name, location):
        if name not in location:
            print("could not find sprite '{}' in atlas".format(name))
            raise SpriteNotFoundException(name)
        return location[name]

    @staticmethod
    def _get_rect_from_str(rect_str):
        r = pygame.Rect(0, 0, 0, 0)

        r.left, r.top, r.width, r.height = [int(x) for x in rect_str.split(' ')]

        return r

    @staticmethod
    def initialize_from_dir(path):
        assert os.path.exists(path)
        assert os.path.isdir(path)

        raise NotImplementedError


def load():
    atlas = SpriteAtlas(os.path.join('images', 'atlas.png'))

    # stationary
    atlas.initialize_static("mario_stand_right", config.transparent_color)
    atlas.initialize_static_from_surface("mario_stand_left",
                                         pygame.transform.flip
                                         (atlas.load_static("mario_stand_right").frames[0], True, False))

    # running (left and right)
    atlas.initialize_animation("mario_run_right", 16, 16, 0.2, config.transparent_color)

    run_right = atlas.load_animation("mario_run_right")  # type: Animation
    left_run_frames = [pygame.transform.flip(f, True, False) for f in run_right.frames]
    atlas.initialize_animation_from_frames("mario_run_left", left_run_frames, run_right.duration)

    # walking (left and right)
    # same frames as running, just slower
    atlas.initialize_animation_from_frames("mario_walk_right", run_right.frames, 0.3)
    atlas.initialize_animation_from_frames("mario_walk_left", left_run_frames, 0.3)

    # jumping (left and right)
    atlas.initialize_static("mario_jump_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "mario_jump_left", pygame.transform.flip(atlas.load_static("mario_jump_right").frames[0], True, False))

    # skidding (left and right)
    atlas.initialize_static("mario_skid_left", config.transparent_color)

    atlas.initialize_static_from_surface(
        "mario_skid_right", pygame.transform.flip(atlas.load_static("mario_skid_left").frames[0], True, False))



    return atlas

# atlas.initialize_static("ship", color_key=config.transparent_color, override_width=48)  # used for explosion
# atlas.initialize_static("player_bullet", color_key=config.transparent_color, generate_mask=True)
# atlas.initialize_static("bunker", color_key=config.transparent_color, generate_mask=True)
# atlas.initialize_static("selector", color_key=config.transparent_color)
# atlas.initialize_static("ship_no_engines", color_key=config.transparent_color)
#
# atlas.initialize_animation("ship", 48, 32, 0.25, color_key=config.transparent_color)
#
# # init alien sprites
# for alien in config.alien_stats:
#     atlas.initialize_animation(alien.sprite_name, 32, 32, 1, color_key=config.transparent_color)
# atlas.initialize_animation("ufo", 64, 64, 1, color_key=config.transparent_color)
#
# # alien bullet frames
# frames = generate_alien_bullet_frames(config.default_alien_bullet.size, config.default_alien_bullet.color)
# atlas.initialize_animation_from_frames("alien_bullet", frames, 0.5, generate_masks=True)
#
# # explosion frames for ship
# frames = generate_explosion_frames(atlas.load_static("ship").image, 16, .5, 1.25, 15.5, 4.0)
# atlas.initialize_animation_from_frames("ship_explosion", frames, .5)
#
# # explosion frames for aliens
# for key in [k for k in atlas.animations.keys() if k.startswith("alien")]:
#     frames = generate_explosion_frames(atlas.load_animation(key).image, 4, 1, 2, 8)
#     atlas.initialize_animation_from_frames(key + "_explosion", frames, .25)
