from util import make_vector
from assets.gui_helper import *


class ToolDialog(Dialog):
    SIZE = (165, 96)

    def __init__(self, gui_atlas, title):
        self.font = pygame.font.SysFont(None, 24)

        r = config.screen_rect.copy()

        super().__init__(make_vector(r.right - ToolDialog.SIZE[0], r.top),
                         ToolDialog.SIZE, gui_atlas.load_sliced("tb_frame"),
                         tb_bkg=gui_atlas.load_sliced("tb_frame"),
                         additional_height=8, text_start_offset=(12, 5),
                         font=self.font, title=title)
        self.gui_atlas = gui_atlas

        self._tools = []
        self._tool_options = OptionGroup()
        self.layout()

    def create_tool(self, tools, selected_image_name, unselected_image_name, font, selected_cb, deselected_cb,
                    y_offset=0):
        tool_static = self.gui_atlas.load_static(unselected_image_name)
        tool_hl_static = self.gui_atlas.load_static(selected_image_name)

        offset_x = tools[len(tools) - 1].relative_position.x + tool_static.get_rect().width\
            if len(tools) > 0 else 10

        tool = Option(make_vector(offset_x, self.get_title_bar_bottom() + y_offset + 5), tool_hl_static.get_rect().size,
                      background=self.gui_atlas.load_sliced("control_small_block"),
                      font=font,
                      selected_image=tool_hl_static,
                      unselected_image=tool_static,
                      text="",
                      on_selected_callback=selected_cb,
                      on_deselected_callback=deselected_cb,
                      is_selected=False)

        self.add_child(tool)
        tools.append(tool)

        return tool

    def add_tool(self, gui_name, hl_gui_name, on_select_callback=None, on_deselect_callback=None):
        tool = self.create_tool(self._tools, hl_gui_name, gui_name, self.font, on_select_callback, on_deselect_callback)

        if len(self._tools) == 1:
            tool.selected = True
        else:
            tool.selected = False

        self._tool_options.add(tool)

        self.layout()
