import os
import pygame
from . import SpriteAtlas
from animation import Animation
from entities.gui.drawing import generated_selected_version_circle, generated_selected_version_darken
import config


def get_atlas_path(atlas_name):
    return os.path.join("images", f"atlas_{atlas_name}.png")


def _load_all_as_static(atlas_name, rescale=True):
    path = get_atlas_path(atlas_name)

    if not os.path.exists(path):
        return SpriteAtlas(tf_use_rescale_factor=False)

    atlas = SpriteAtlas(path, rescale)
    kwargs = {"color_key": config.transparent_color}

    for name in atlas.sprite_names:
        atlas.initialize_static(name, **kwargs)

    return atlas


def load_entity_atlas():
    atlas = SpriteAtlas(get_atlas_path("mario"))

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
    atlas = SpriteAtlas(get_atlas_path("gui"), tf_use_rescale_factor=False, convert=False)
    kwargs = {"color_key": config.transparent_color}

    def load_slice(name, hl_name, dims, **kw):
        atlas.initialize_slice(name, dims, **kw)
        sliced = atlas.load_sliced(name)

        hl = generated_selected_version_darken(sliced.base_surface, 0.5)

        if sliced.base_surface.get_colorkey() is not None:
            hl = hl.convert()
            hl.set_colorkey(sliced.base_surface.get_colorkey())

        atlas.initialize_slice_from_surface(hl_name, hl, dims)

    load_slice("bkg_square", "bkg_square_hl", (16, 16), **kwargs)
    load_slice("bkg_rounded", "bkg_rounded_hl", (32, 32), **kwargs)
    load_slice("bkg_very_rounded", "bkg_very_rounded_hl", (32, 32), **kwargs)
    load_slice("control_small", "control_small_hl", (7, 7), **kwargs)
    load_slice("control_small_block", "control_small_block_hl", (7, 7), **kwargs)
    load_slice("control_small_block2", "control_small_block2_hl", (7, 7), **kwargs)

    atlas.initialize_static("option_button", **kwargs)
    atlas.initialize_static("option_button_checked_heavy", **kwargs)
    atlas.initialize_static("option_button_checked_light", **kwargs)

    # tools (no colorkey => use per-pixel alpha)

    def load_tool_static(name, hl_name):
        atlas.initialize_static(name)
        atlas.initialize_static_from_surface(hl_name, generated_selected_version_circle(atlas.load_static(name).image,
                                                                                 pygame.Color('yellow')))

    load_tool_static("pencil", "pencil_hl")
    load_tool_static("paint", "paint_hl")
    load_tool_static("grid", "grid_hl")
    load_tool_static("dropper", "dropper_hl")

    return atlas


def load_solid_block_atlas():
    return _load_all_as_static("solid_blocks")


def load_background_block_atlas():
    return _load_all_as_static("background_blocks")


def load_interactive_block_atlas():
    return _load_all_as_static("interactive_blocks")

    # todo: actually load animations here


def load_misc_atlas():
    atlas = SpriteAtlas(get_atlas_path("misc"), tf_use_rescale_factor=True)
    kwargs = {"color_key": config.transparent_color}

    atlas.initialize_static("misc_gray_bricks", **kwargs)
    atlas.initialize_static("green_square")

    return atlas


def load_atlases():
    entity_atlas = load_entity_atlas()
    gui_atlas = load_gui_atlas()
    solid_block_atlas = load_solid_block_atlas()
    background_block_atlas = load_background_block_atlas()
    interactive_block_atlas = load_interactive_block_atlas()
    misc_atlas = load_misc_atlas()

    return entity_atlas + gui_atlas + solid_block_atlas + background_block_atlas + interactive_block_atlas + misc_atlas
