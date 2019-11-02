from .util import create_static_with_flipped, create_animation_with_flipped
import config


"""Mario has so much associated with him, it's best to keep it all in one place where there is as little noise
as possible from loading other things"""


def load_mario(atlas, small, large):
    # stationary mario
    create_static_with_flipped(atlas, "mario_stand_right", "mario_stand_left")
    create_static_with_flipped(atlas, "mario_fire_stand_right", "mario_fire_stand_left")
    create_static_with_flipped(atlas, "super_mario_stand_right", "super_mario_stand_left")
    create_static_with_flipped(atlas, "super_mario_fire_stand_right", "super_mario_fire_stand_left")

    # running mario (left and right)
    create_animation_with_flipped(atlas, "mario_run_right", "mario_run_left", small, 0.2)
    create_animation_with_flipped(atlas, "mario_fire_run_right", "mario_fire_run_left", small, 0.2)
    create_animation_with_flipped(atlas, "super_mario_run_right", "super_mario_run_left", large, 0.2)
    create_animation_with_flipped(atlas, "super_mario_fire_run_right", "super_mario_fire_run_left", large, 0.2)

    # walking mario (left and right)
    # same frames as running, just slower

    # normal walking mario
    atlas.initialize_animation_from_frames("mario_walk_right", atlas.load_animation("mario_run_right").frames, 0.4)
    atlas.initialize_animation_from_frames("mario_walk_left", atlas.load_animation("mario_run_left").frames, 0.4)

    # fire walking mario
    atlas.initialize_animation_from_frames("mario_fire_walk_right",
                                           atlas.load_animation("mario_fire_run_right").frames, 0.4)
    atlas.initialize_animation_from_frames("mario_fire_walk_left",
                                           atlas.load_animation("mario_fire_run_left").frames, 0.4)

    # normal walking super mario
    atlas.initialize_animation_from_frames("super_mario_walk_right",
                                           atlas.load_animation("super_mario_run_right").frames, 0.4)
    atlas.initialize_animation_from_frames("super_mario_walk_left",
                                           atlas.load_animation("super_mario_run_left").frames, 0.4)

    atlas.initialize_animation_from_frames("super_mario_fire_walk_right",
                                           atlas.load_animation("super_mario_fire_run_right").frames, 0.4)
    atlas.initialize_animation_from_frames("super_mario_fire_walk_left",
                                           atlas.load_animation("super_mario_fire_run_left").frames, 0.4)

    # jumping mario (left and right)
    create_static_with_flipped(atlas, "mario_jump_right", "mario_jump_left")
    create_static_with_flipped(atlas, "mario_fire_jump_right", "mario_fire_jump_left")
    create_static_with_flipped(atlas, "super_mario_jump_right", "super_mario_jump_left")
    create_static_with_flipped(atlas, "super_mario_fire_jump_right", "super_mario_fire_jump_left")

    # skidding mario (left and right)
    create_static_with_flipped(atlas, "mario_skid_left", "mario_skid_right")
    create_static_with_flipped(atlas, "mario_fire_skid_left", "mario_fire_skid_right")
    create_static_with_flipped(atlas, "super_mario_skid_left", "super_mario_skid_right")
    create_static_with_flipped(atlas, "super_mario_fire_skid_left", "super_mario_fire_skid_right")

    # death
    atlas.initialize_static("mario_dead", config.transparent_color)
    atlas.initialize_static("mario_fire_dead", config.transparent_color)
    # todo: super mario dead?

    # crouching
    create_static_with_flipped(atlas, "super_mario_crouch_right", "super_mario_crouch_left")
    create_static_with_flipped(atlas, "super_mario_fire_crouch_right", "super_mario_fire_crouch_left")

    # transformations
    create_static_with_flipped(atlas, "super_mario_transform_right", "super_mario_transform_left")
    create_static_with_flipped(atlas, "super_mario_fire_transform_right", "super_mario_fire_transform_left")

    # pole movement
    atlas.initialize_static("mario_pole_right", config.transparent_color)
    atlas.initialize_static("fire_mario_pole_right", config.transparent_color)
    atlas.initialize_static("super_mario_pole_right", config.transparent_color)
    atlas.initialize_static("super_mario_fire_pole_right", config.transparent_color)
