import os
import pygame
from assets.sprite_atlas import SpriteAtlas
import config


def get_atlas_path(atlas_name):
    return os.path.join("images", f"atlas_{atlas_name}.png")


def load_all_as_static(atlas_name, rescale=True):
    path = get_atlas_path(atlas_name)

    if not os.path.exists(path):
        return SpriteAtlas(tf_use_rescale_factor=False)

    atlas = SpriteAtlas(path, rescale)
    kwargs = {"color_key": config.transparent_color}

    for name in atlas.sprite_names:
        atlas.initialize_static(name, **kwargs)

    return atlas


def create_static_with_flipped(atlas, name, flipped_name, trans_color=config.transparent_color):
    atlas.initialize_static(name, trans_color)
    atlas.initialize_static_from_surface(flipped_name,
                                         pygame.transform.flip(
                                             atlas.load_static(name).frames[0], True, False)
                                         )


def create_animation_with_flipped(atlas, name, flipped_name, size, duration, trans_color=config.transparent_color):
    atlas.initialize_animation(name, *size, duration, trans_color)

    flipped_frames = [pygame.transform.flip(f, True, False) for f in atlas.load_animation(name).frames]
    atlas.initialize_animation_from_frames(flipped_name, flipped_frames, duration)
