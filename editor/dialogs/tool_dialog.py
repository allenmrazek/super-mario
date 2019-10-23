import pygame
from entities.gui import Text, Texture, Window, Dialog, Button, Option, OptionGroup
import config
from util import make_vector


class ToolDialog(Dialog):
    SIZE = (256, 128)

    def __init__(self, atlas):
        font = pygame.font.SysFont("", 24)

        r = config.screen_rect.copy()
        super().__init__(make_vector(r.right - ToolDialog.SIZE[0], r.top),
                         ToolDialog.SIZE, atlas.load_sliced("bkg_rounded"),
                         font=font, title="Tools")

        # todo: tool types

        self.pencil_tool = self.create_tool(atlas, "pencil_hl", "pencil", font)
        self.dropper_tool = self.create_tool(atlas, "dropper_hl", "dropper", font)
        self.paint_tool = self.create_tool(atlas, "paint_hl", "paint", font)
        self.tools = [self.pencil_tool, self.dropper_tool, self.paint_tool]

        for idx, tool in enumerate(self.tools):
            tool.relative_position = make_vector(10 + idx * max(map(lambda t: t.width, self.tools)),
                                                 self.get_title_bar_bottom())
        self.pencil_tool.selected = True

        self._tool_option_group = OptionGroup(True, self.tools)

        self.layout()

    def create_tool(self, atlas, selected_image_name, unselected_image_name, font):
        tool_static = atlas.load_static(unselected_image_name)
        tool_hl_static = atlas.load_static(selected_image_name)

        tool = Option(make_vector(0, self.get_title_bar_bottom()), tool_hl_static.get_rect().size,
                      background=atlas.load_sliced("control_small_block"),
                      font=font,
                      selected_image=tool_hl_static,
                      unselected_image=tool_static,
                      text="")

        self.add_child(tool)

        tool.selected = False
        return tool
