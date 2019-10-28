import os
import pygame
import warnings
from pygame.mixer import Sound
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


def load_character_atlas():
    atlas = SpriteAtlas(get_atlas_path("characters"))

    small_frame_width, small_frame_height = [16 * config.rescale_factor] * 2
    large_frame_width, large_frame_height = small_frame_width, 2 * small_frame_height

    # stationary mario
    atlas.initialize_static("mario_stand_right", config.transparent_color)
    atlas.initialize_static_from_surface("mario_stand_left",
                                         pygame.transform.flip
                                         (atlas.load_static("mario_stand_right").frames[0], True, False))

    atlas.initialize_static("mario_fire_stand_right", config.transparent_color)
    atlas.initialize_static_from_surface("mario_fire_stand_left",
                                         pygame.transform.flip
                                         (atlas.load_static("mario_fire_stand_right").frames[0], True, False))

    atlas.initialize_static("super_mario_stand_right", config.transparent_color)
    atlas.initialize_static_from_surface("super_mario_stand_left", pygame.transform.flip
                                         (atlas.load_static("super_mario_stand_right").frames[0], True, False))

    atlas.initialize_static("super_mario_fire_stand_right", config.transparent_color)
    atlas.initialize_static_from_surface("super_mario_fire_stand_left", pygame.transform.flip
                                         (atlas.load_static("super_mario_fire_stand_right").frames[0], True, False))

    # running mario (left and right)
    atlas.initialize_animation("mario_run_right",
                               small_frame_width,
                               small_frame_height,
                               0.2, config.transparent_color)

    mario_run_right = atlas.load_animation("mario_run_right")  # type: Animation
    mario_left_run_frames = [pygame.transform.flip(f, True, False) for f in mario_run_right.frames]
    atlas.initialize_animation_from_frames("mario_run_left", mario_left_run_frames, mario_run_right.duration)

    atlas.initialize_animation("mario_fire_run_right",
                               small_frame_width,
                               small_frame_height,
                               0.2, config.transparent_color)

    mario_fire_run_right = atlas.load_animation("mario_fire_run_right")  # type: Animation
    mario_fire_left_run_frames = [pygame.transform.flip(f, True, False) for f in mario_fire_run_right.frames]
    atlas.initialize_animation_from_frames("mario_fire_run_left", mario_fire_left_run_frames, mario_fire_run_right.duration)

    atlas.initialize_animation("super_mario_run_right",
                               large_frame_width,
                               large_frame_height,
                               0.2, config.transparent_color)

    super_mario_run_right = atlas.load_animation("super_mario_run_right")  # type: Animation
    super_mario_left_run_frames = [pygame.transform.flip(f, True, False) for f in super_mario_run_right.frames]
    atlas.initialize_animation_from_frames("super_mario_run_left", super_mario_left_run_frames, super_mario_run_right.duration)

    atlas.initialize_animation("super_mario_fire_run_right",
                               large_frame_width,
                               large_frame_height,
                               0.2, config.transparent_color)

    super_mario_fire_run_right = atlas.load_animation("super_mario_fire_run_right")  # type: Animation
    super_mario_fire_left_run_frames = [pygame.transform.flip(f, True, False) for f in super_mario_fire_run_right.frames]
    atlas.initialize_animation_from_frames("super_mario_fire_run_left", super_mario_fire_left_run_frames, super_mario_fire_run_right.duration)

    # walking mario (left and right)
    # same frames as running, just slower
    atlas.initialize_animation_from_frames("mario_walk_right", mario_run_right.frames, 0.4)
    atlas.initialize_animation_from_frames("mario_walk_left", mario_left_run_frames, 0.4)

    atlas.initialize_animation_from_frames("mario_fire_walk_right", mario_fire_run_right.frames, 0.4)
    atlas.initialize_animation_from_frames("mario_fire_walk_left", mario_fire_left_run_frames, 0.4)

    atlas.initialize_animation_from_frames("super_mario_walk_right", super_mario_run_right.frames, 0.4)
    atlas.initialize_animation_from_frames("super_mario_walk_left", super_mario_left_run_frames, 0.4)

    atlas.initialize_animation_from_frames("super_mario_fire_walk_right", super_mario_fire_run_right.frames, 0.4)
    atlas.initialize_animation_from_frames("super_mario_fire_walk_left", super_mario_fire_left_run_frames, 0.4)

    # jumping mario (left and right)
    atlas.initialize_static("mario_jump_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "mario_jump_left", pygame.transform.flip(atlas.load_static("mario_jump_right").frames[0], True, False))

    atlas.initialize_static("mario_fire_jump_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "mario_fire_jump_left", pygame.transform.flip(atlas.load_static("mario_fire_jump_right").frames[0], True, False))

    atlas.initialize_static("super_mario_jump_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "super_mario_jump_left", pygame.transform.flip(atlas.load_static("super_mario_jump_right").frames[0], True, False))

    atlas.initialize_static("super_mario_fire_jump_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "super_mario_fire_jump_left", pygame.transform.flip(atlas.load_static("super_mario_fire_jump_right").frames[0], True, False))

    # skidding mario (left and right)
    atlas.initialize_static("mario_skid_left", config.transparent_color)
    atlas.initialize_static_from_surface(
        "mario_skid_right", pygame.transform.flip(atlas.load_static("mario_skid_left").frames[0], True, False))

    atlas.initialize_static("mario_fire_skid_left", config.transparent_color)
    atlas.initialize_static_from_surface(
        "mario_fire_skid_right", pygame.transform.flip(atlas.load_static("mario_fire_skid_left").frames[0], True, False))

    atlas.initialize_static("super_mario_skid_left", config.transparent_color)
    atlas.initialize_static_from_surface(
        "super_mario_skid_right", pygame.transform.flip(atlas.load_static("super_mario_skid_left").frames[0], True, False))

    atlas.initialize_static("super_mario_fire_skid_left", config.transparent_color)
    atlas.initialize_static_from_surface(
        "super_mario_fire_skid_right", pygame.transform.flip(atlas.load_static("super_mario_fire_skid_left").frames[0], True, False))

    # death
    atlas.initialize_static("mario_dead", config.transparent_color)
    atlas.initialize_static("mario_fire_dead", config.transparent_color)

    # crouching
    atlas.initialize_static("super_mario_crouch_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "super_mario_crouch_left", pygame.transform.flip(atlas.load_static("super_mario_crouch_right").frames[0], True, False))

    atlas.initialize_static("super_mario_fire_crouch_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "super_mario_fire_crouch_left", pygame.transform.flip(atlas.load_static("super_mario_fire_crouch_right").frames[0], True, False))

    # transformations
    atlas.initialize_static("super_mario_transform_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "super_mario_transform_left", pygame.transform.flip(atlas.load_static("super_mario_transform_right").frames[0], True, False))

    atlas.initialize_static("super_mario_fire_transform_right", config.transparent_color)
    atlas.initialize_static_from_surface(
        "super_mario_fire_transform_left", pygame.transform.flip(atlas.load_static("super_mario_fire_transform_right").frames[0], True, False))

    # goomba enemy
    atlas.initialize_animation("goomba", small_frame_width, small_frame_height, .25, config.transparent_color)
    atlas.initialize_static("goomba_squashed", config.transparent_color)

    return atlas


def load_gui_atlas():
    atlas = SpriteAtlas(get_atlas_path("gui"), tf_use_rescale_factor=False, convert=False)
    kwargs = {"color_key": config.transparent_color}

    def load_slice(name, darken_name, dims, **kw):
        atlas.initialize_slice(name, dims, **kw)
        sliced = atlas.load_sliced(name)

        if darken_name is not None:
            darkened = generated_selected_version_darken(sliced.base_surface, 0.5)

            if sliced.base_surface.get_colorkey() is not None:
                darkened = darkened.convert()
                darkened.set_colorkey(sliced.base_surface.get_colorkey())

            atlas.initialize_slice_from_surface(darken_name, darkened, dims)

    load_slice("bkg_square", "bkg_square_dk", (16, 16), **kwargs)
    load_slice("bkg_rounded", "bkg_rounded_dk", (32, 32), **kwargs)
    load_slice("bkg_very_rounded", "bkg_very_rounded_dk", (32, 32), **kwargs)
    load_slice("button_bkg_dark", None, (7, 7), **kwargs)
    load_slice("button_bkg_light", None, (7, 7), **kwargs)
    load_slice("button_bkg_white", "button_bkg_white_dk", (7, 7), **kwargs)
    load_slice("window_bkg_large", None, (34, 34), **kwargs)
    load_slice("frame1", "frame1_dk", (43, 43), **kwargs)
    load_slice("tb_frame", "tb_frame_dk", (5, 5), **kwargs)
    load_slice("control_small", "control_small_dk", (7, 7), **kwargs)
    load_slice("control_small_block", "control_small_block_dk", (7, 7), **kwargs)
    load_slice("control_small_block2", "control_small_block2_dk", (7, 7), **kwargs)
    load_slice("sb_thumb_h", "sb_thumb_h_dk", (4, 4), **kwargs)
    load_slice("sb_thumb_v", "sb_thumb_v_dk", (4, 4), **kwargs)
    load_slice("slider_bkg_h", None, (7, 7), **kwargs)
    load_slice("slider_bkg_v", None, (7, 7), **kwargs)
    load_slice("sb_thumb_light", None, (7, 7), **kwargs)
    load_slice("option_button", "option_button_hl", (4, 4))

    atlas.initialize_static("option_button", **kwargs)
    atlas.initialize_static("option_button_checked_heavy", **kwargs)
    atlas.initialize_static("option_button_checked_light", **kwargs)
    atlas.initialize_static("slider_thumb_h", **kwargs)
    atlas.initialize_static("slider_thumb_h_light", **kwargs)
    atlas.initialize_static("slider_thumb_v", **kwargs)
    atlas.initialize_static("slider_thumb_v_light", **kwargs)
    atlas.initialize_static("slider_bkg_h", **kwargs)
    atlas.initialize_static("slider_bkg_v", **kwargs)
    atlas.initialize_static("sb_thumb", **kwargs)
    atlas.initialize_static("sb_thumb_light", **kwargs)

    # tools (no colorkey => use per-pixel alpha)

    def load_tool_static(name, hl_name):
        atlas.initialize_static(name)
        atlas.initialize_static_from_surface(hl_name, generated_selected_version_circle(atlas.load_static(name).image,
                                                                                        pygame.Color('yellow')))

    load_tool_static("pencil", "pencil_hl")
    load_tool_static("paint", "paint_hl")
    load_tool_static("grid", "grid_hl")
    load_tool_static("dropper", "dropper_hl")
    load_tool_static("select", "select_hl")
    load_tool_static("delete", "delete_hl")
    load_tool_static("left", "left_hl")
    load_tool_static("bottom", "bottom_hl")

    return atlas


def load_tile_atlas(tf_rescale=True):
    return _load_all_as_static("tiles", rescale=tf_rescale)


def load_misc_atlas():
    atlas = SpriteAtlas(get_atlas_path("misc"), tf_use_rescale_factor=True)
    kwargs = {"color_key": config.transparent_color}

    atlas.initialize_static("misc_gray_bricks", **kwargs)
    atlas.initialize_static("green_square")

    return atlas


def load_pickup_atlas():
    atlas = SpriteAtlas(get_atlas_path("pickups"), tf_use_rescale_factor=True)
    kwargs = {"color_key": config.transparent_color}

    atlas.initialize_static("mushroom_red", **kwargs)

    return atlas


def load_sound_fx():
    sounds = {}

    def load_sound(name):
        path = os.path.join('sounds', 'sfx', name)

        if not os.path.exists(path):
            warnings.warn(f'could not load {path} -- does not exist')
        else:
            try:
                return Sound(path)
            except pygame.error:
                warnings.warn(f'Unable to load {Sound}')

    sounds['powerup'] = load_sound('smb_powerup.wav')
    sounds['stomp'] = load_sound('smb_stomp.wav')
    sounds['smb_life'] = load_sound('smb_1-up.wav')
    sounds['kick'] = load_sound('smb_kick.wav')
    sounds['pause'] = load_sound('smb_pause.wav')

    return sounds
