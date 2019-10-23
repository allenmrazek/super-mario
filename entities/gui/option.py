from copy import copy
from . import Button, SlicedImage, Text, Anchor, Texture
import config
from util import make_vector, copy_vector


class Option(Button):
    def __init__(self, position, size, background, font, text,
                 selected_image, unselected_image, is_selected=True, anchor=Anchor.TOP_LEFT,
                 text_color=config.default_text_color, mouseover_image=None):
        super().__init__(position=position,
                         size=size, background=background, text="", font=font, anchor=anchor,
                         mouseover_image=mouseover_image)

        assert selected_image and unselected_image

        # create textures
        # position them on left side, in center
        relative = make_vector(0, size[1] // 2)

        self._texture_on = Texture(selected_image, relative)
        self._texture_off = Texture(unselected_image, relative)

        relative.y -= max(self._texture_off.height, self._texture_on.height) // 2
        self._texture_on.relative_position = copy_vector(relative)
        self._texture_off.relative_position = copy_vector(relative)

        self.add_child(self._texture_on)
        self.add_child(self._texture_off)

        self.selected = is_selected

        # create text
        # position to right side of textures
        relative.x = max(self._texture_on.get_absolute_rect().right + 10,
                         self._texture_off.get_absolute_rect().right + 10)
        relative.y = size[1] // 2 - font.get_height() // 2

        self.text = Text(relative, text, font, text_color=text_color)

        self.add_child(self.text)

        self.layout()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, val):
        self._texture_off.enabled = not val
        self._texture_on.enabled = val
        self._selected = val
        # todo: invoke callback?

    def clicked(self):
        print("option clicked!")
        self.selected = not self.selected


class OptionGroup:
    """This class makes sure only one option in a set of options is selected at a time"""
    def __init__(self, tf_require_selected=True, *option_buttons):
        self.option_buttons = []
        self.require_selected = tf_require_selected  # if true, ensure there is always at least one selection
        for btn in option_buttons:
            self.add(btn)

    def _make_callback(self, button_self):
        """Goal: right after the original click does whatever it does, we get a chance. Do this transparently"""
        original_click = button_self.clicked

        def merged_callback():
            # if we require at least one selection, don't allow a button to become unselected due to a click
            if not self.require_selected or not button_self.selected:
                original_click()
                self.on_member_clicked(button_self)

        button_self.clicked = merged_callback

    def add(self, option_button):
        assert isinstance(option_button, Option)

        self.option_buttons.append(option_button)
        self._make_callback(option_button)

    def on_member_clicked(self, which):
        if which.selected:
            # unset all other options
            for btn in self.option_buttons:
                if btn is not which:
                    btn.selected = False
