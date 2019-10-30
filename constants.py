COIN_POINT_VALUE = 200
TIME_PER_LEVEL = 400
BRICK_VALUE = 50

Background = 1 << 0  # behind blocks
Block = 1 << 1  # layer blocks are drawn on
Spawner = 1 << 2  # spawners go here
Trigger = 1 << 3  # take a guess
Mario = 1 << 4  # take a guess
Enemy = 1 << 5  # take another guess
Active = 1 << 6  # "active" things: think fireballs and projectiles; mario death animations
Interface = 1 << 7  # interface stuff here
Overlay = 1 << 8  # a final layer that absolutely will overlay everything. Use sparingly

LayerList = [Background, Block, Spawner, Trigger, Mario, Enemy, Active, Interface, Overlay]


def layer_to_name(layer):
    names = {Background: "Background",
             Block: "Block",
             Spawner: "Spawner",
             Trigger: "Trigger",
             Mario: "Mario",
             Enemy: "Enemy",
             Active: "Active",
             Interface: "Interface",
             Overlay: "Overlay"}

    if layer not in names:
        raise NotImplementedError

    return names[layer]


def name_to_layer(layer_name):
    layers = {"Background": Background,
              "Block": Block,
              "Spawner": Spawner,
              "Trigger": Trigger,
              "Mario": Mario,
              "Enemy": Enemy,
              "Active": Active,
              "Interface": Interface,
              "Overlay": Overlay}

    if layer_name not in layers:
        raise NotImplementedError

    return layers[layer_name]
