block_size = 16  # 16 pixels on a side


def mario_str_to_pixel_value(str_mario_value):
    """Given a classic mario velocity string, convert into a magnitude suitable for the game"""

    if str_mario_value[0:2].lower() == "0x":
        str_mario_value = str_mario_value[2:]

    block_value = int(str_mario_value[:1], 16)
    pixel_value = int(str_mario_value[1:2], 16)
    subpixel_value = int(str_mario_value[2:3], 16)
    subsubpixel_value = int(str_mario_value[3:4], 16)
    subsubsubpixel_value = int(str_mario_value[4:5], 16)

    return block_value * block_size + pixel_value + subpixel_value / 16. + subsubpixel_value / (16. * 16.) + \
        subsubsubpixel_value / (16. * 16. * 16.)