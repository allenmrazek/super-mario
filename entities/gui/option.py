from copy import copy
from . import Button, SlicedImage, Text, ElementStyle, Anchor, Texture
import config
from util import make_vector, copy_vector


class Option(Button):
    def __init__(self, position, size, text, option_style: ElementStyle, button_style=None, is_selected=True):
        super().__init__(position=position,
                         size=size,
                         style=button_style or option_style,
                         text="",  # will control own text
                         )

        selected_image = option_style.selected
        unselected_image = option_style.not_selected

        assert selected_image and unselected_image

        # create textures
        # position them on left side, in center
        relative = make_vector(0, size[1] // 2)

        self._texture_on = Texture(selected_image, relative)
        self._texture_off = Texture(unselected_image, relative)

        # self.add_child(self._texture_on)
        # self.add_child(self._texture_off)

        self.selected = is_selected

        # create text
        # position to right side of textures
        relative.x = max(self._texture_on.width, self._texture_off.width)
        relative.y = size[1] // 2 - option_style.font.get_height() // 2

        self.text = Text(relative, text, button_style)

        self.add_child(self.text)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, val):
        self._texture_off.enabled = not val
        self._texture_on.enabled = val
        self._selected = val
        # todo: invoke callback?

    def on_click(self):
        print("option clicked!")
        self.selected = not self.selected

