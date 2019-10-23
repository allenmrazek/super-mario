import os
import pygame
from . import SpriteAtlas
from animation import Animation
import config


def _get_atlas_path(atlas_name):
    return os.path.join("images", f"{atlas_name}.png")


def load_entity_atlas():
    atlas = SpriteAtlas(_get_atlas_path("atlas_entities"))

    # stationary
    atlas.initialize_static("mario_stand_right", config.transparent_color)
    atlas.initialize_static_from_surface("mario_stand_left",
                                         pygame.transform.flip
                                         (atlas.load_static("mario_stand_right").frames[0], True, False))

    # running (left and right)
    atlas.initialize_animation("mario_run_right",
                               16 * config.rescale_factor,
                               16 * config.rescale_factor,
                               0.2, config.transparent_color)

    run_right = atlas.load_animation("mario_run_right")  # type: Animation
    left_run_frames = [pygame.transform.flip(f, True, False) for f in run_right.frames]
    atlas.initialize_animation_from_frames("mario_run_left", left_run_frames, run_right.duration)

    # walking (left and right)
    # same frames as running, just slower
    atlas.initialize_animation_from_frames("mario_walk_right", run_right.frames, 0.4)
    atlas.initialize_animation_from_frames("mario_walk_left", left_run_frames, 0.4)

    # jumping (left and right)
    atlas.initialize_static("mario_jump_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "mario_jump_left", pygame.transform.flip(atlas.load_static("mario_jump_right").frames[0], True, False))

    # skidding (left and right)
    atlas.initialize_static("mario_skid_left", config.transparent_color)

    atlas.initialize_static_from_surface(
        "mario_skid_right", pygame.transform.flip(atlas.load_static("mario_skid_left").frames[0], True, False))

    return atlas


def load_gui_atlas():
    atlas = SpriteAtlas(_get_atlas_path("atlas_gui"), tf_use_rescale_factor=False)
    kwargs = {"color_key": config.transparent_color}

    atlas.initialize_slice("bkg_square", (16, 16), **kwargs)
    atlas.initialize_slice("bkg_rounded", (32, 32), **kwargs)
    atlas.initialize_slice("bkg_very_rounded", (32, 32), **kwargs)
    atlas.initialize_slice("control_small", (7, 7), **kwargs)

    atlas.initialize_static("option_button", **kwargs)
    atlas.initialize_static("option_button_checked_heavy", **kwargs)
    atlas.initialize_static("option_button_checked_light", **kwargs)

    return atlas


def load_atlases():
    entity_atlas = load_entity_atlas()
    gui_atlas = load_gui_atlas()

    return entity_atlas + gui_atlas
