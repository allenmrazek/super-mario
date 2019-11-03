import os
import pygame
import warnings
from pygame.mixer import Sound
from . import SpriteAtlas
from entities.gui.drawing import generated_selected_version_circle, generated_selected_version_darken
import config
from .util import get_atlas_path, load_all_as_static
from .load_characters import load_characters
from .load_mario import load_mario


def load_character_atlas():
    atlas = SpriteAtlas(get_atlas_path("characters"))

    small_frame_width, small_frame_height = [config.base_tile_dimensions[0] * config.rescale_factor] * 2
    large_frame_width, large_frame_height = small_frame_width, 2 * small_frame_height

    load_mario(atlas, (small_frame_width, small_frame_height),
               (large_frame_width, large_frame_height))

    load_characters(atlas,
                    (small_frame_width, small_frame_height),
                    (large_frame_width, large_frame_height))

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

    # other things used in editor, here because they shouldn't be scaled like other atlases are
    atlas.initialize_static("level_warp")
    atlas.initialize_static("mm_Smb", **kwargs)
    atlas.initialize_static("menu_mushroom", **kwargs)
    atlas.initialize_static("bulb", **kwargs)

    return atlas


def load_tile_atlas(tf_rescale=True):
    return load_all_as_static("tiles", rescale=tf_rescale)


def load_misc_atlas():
    atlas = SpriteAtlas(get_atlas_path("misc"), tf_use_rescale_factor=True)
    kwargs = {"color_key": config.transparent_color}

    atlas.initialize_static("misc_gray_bricks", **kwargs)
    atlas.initialize_static("green_square")

    return atlas


def load_pickup_atlas():
    atlas = SpriteAtlas(get_atlas_path("pickups"), tf_use_rescale_factor=True)
    kwargs = {"color_key": config.transparent_color}

    fw, fh = 16 * config.rescale_factor, 16 * config.rescale_factor

    atlas.initialize_static("mushroom_red", **kwargs)
    atlas.initialize_animation("fire_flower", fw, fh, 0.25, config.transparent_color)
    atlas.initialize_animation("coin_world", fw, fh, 2., config.transparent_color)
    atlas.initialize_animation("coin_spin", fw, fh, .25, config.transparent_color)

    return atlas


def load_interactive_atlas():
    atlas = SpriteAtlas(get_atlas_path("interactive"), tf_use_rescale_factor=True)
    kwargs = {"color_key": config.transparent_color}

    tinyw, tinyh = 8 * config.rescale_factor, 8 * config.rescale_factor
    tilew, tileh = 16 * config.rescale_factor, 16 * config.rescale_factor

    atlas.initialize_static("brick", **kwargs)
    atlas.initialize_static("brick_debris", **kwargs)

    atlas.initialize_animation("coin_block_ow", tilew, tileh, 1, config.transparent_color)
    atlas.initialize_static("coin_block_empty_ow", **kwargs)
    atlas.initialize_static("flag", **kwargs)
    atlas.initialize_static("flag_pole", **kwargs)
    atlas.initialize_animation("fireball", tinyw, tinyh, 0.33, config.transparent_color)
    atlas.initialize_animation("fireball_explode", tilew, tileh, 0.24, config.transparent_color)

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
    sounds['jump_small'] = load_sound('smb_jump-small.wav')
    sounds['jump_super'] = load_sound('smb_jump-super.wav')
    sounds['pipe'] = load_sound('smb_pipe.wav')
    sounds['downgrade'] = sounds['pipe']
    sounds['breakblock'] = load_sound('smb_breakblock.wav')
    sounds['bump'] = load_sound('smb_bump.wav')
    sounds['coin'] = load_sound('smb_coin.wav')
    sounds['powerup_appears'] = load_sound('smb_powerup_appears.wav')
    sounds['fireball'] = load_sound('smb_fireball.wav')

    return sounds
