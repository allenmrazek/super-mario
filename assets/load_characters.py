from .util import create_static_with_flipped, create_animation_with_flipped
from .sprite_atlas import SpriteAtlas
import config


def load_characters(atlas: SpriteAtlas, small, large):
    # goomba enemy
    atlas.initialize_animation("goomba", *small, .25, config.transparent_color)
    atlas.initialize_static("goomba_squashed", config.transparent_color)

    # koopa
    koopa_size = (16 * config.rescale_factor, 24 * config.rescale_factor)
    create_animation_with_flipped(atlas, "koopa_green_right", "koopa_green_left", koopa_size, 0.33)
    atlas.initialize_static("shell_green", config.transparent_color, *small)
    atlas.initialize_animation("shell_green", *small, 0.25, config.transparent_color)
    atlas.initialize_static("shell_green_dead", config.transparent_color, *small)
