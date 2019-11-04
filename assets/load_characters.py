from .util import create_animation_with_flipped
from .sprite_atlas import SpriteAtlas
import config


def load_characters(atlas: SpriteAtlas, small, large):
    # goomba enemy
    atlas.initialize_animation("goomba", *small, .25, config.transparent_color)
    atlas.initialize_static("goomba_squashed", config.transparent_color)

    # goomba (uw)
    atlas.initialize_animation("goomba_uw", *small, 0.25, config.transparent_color)
    atlas.initialize_static("goomba_uw_squashed", config.transparent_color)

    # koopa (green)
    koopa_size = (16 * config.rescale_factor, 24 * config.rescale_factor)

    create_animation_with_flipped(atlas, "koopa_green_right", "koopa_green_left", koopa_size, 0.33)
    atlas.initialize_static("shell_green", config.transparent_color, *small)
    atlas.initialize_animation("shell_green", *small, 0.25, config.transparent_color)
    atlas.initialize_static("shell_green_dead", config.transparent_color, *small)

    # koopa (red)
    create_animation_with_flipped(atlas, "koopa_red_right", "koopa_red_left", koopa_size, 0.33)
    atlas.initialize_static("shell_red", config.transparent_color, *small)
    atlas.initialize_animation("shell_red", *small, 0.25, config.transparent_color)
    atlas.initialize_static("shell_red_dead", config.transparent_color, *small)

    # koopa (uw)
    create_animation_with_flipped(atlas, "koopa_uw_right", "koopa_uw_left", koopa_size, 0.33)
    atlas.initialize_static("shell_uw", config.transparent_color, *small)
    atlas.initialize_animation("shell_uw", *small, 0.25, config.transparent_color)
    atlas.initialize_static("shell_uw_dead", config.transparent_color, *small)

    # koopa (red, winged)
    create_animation_with_flipped(atlas, "koopa_red_winged_right", "koopa_red_winged_left", koopa_size, 0.33)

    # piranha plant
    plant_size = (16 * config.rescale_factor, 24 * config.rescale_factor)
    atlas.initialize_animation("piranha_plant", *plant_size, 0.25, config.transparent_color)

    # bowser
    bowser_size = (32 * config.rescale_factor, 32 * config.rescale_factor)

    atlas.initialize_animation("bowser_left_mouth_closed", *bowser_size, 0.50, config.transparent_color)
    atlas.initialize_animation("bowser_left_mouth_open", *bowser_size, 0.50, config.transparent_color)
