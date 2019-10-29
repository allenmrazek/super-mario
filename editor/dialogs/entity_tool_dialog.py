from enum import Flag, Enum
from .tool_dialog import ToolDialog
from util import bind_callback_parameters


class ActiveEntityTool(Enum):
    PLACE = 0
    SELECT = 1
    DELETE = 2


class GridAlignment(Flag):
    NONE = 0
    LEFT = 1 << 0
    BOTTOM = 1 << 1
    GRID = LEFT | BOTTOM


class EntityToolDialog(ToolDialog):
    def __init__(self, gui_atlas):
        super().__init__(gui_atlas, "Entity Tools")

        self.active_tool = ActiveEntityTool.PLACE

        self.add_tool("pencil", "pencil_hl", bind_callback_parameters(self._set_tool, ActiveEntityTool.PLACE))
        self.add_tool("select", "select_hl", bind_callback_parameters(self._set_tool, ActiveEntityTool.SELECT))
        self.add_tool("delete", "delete_hl", bind_callback_parameters(self._set_tool, ActiveEntityTool.DELETE))

        # extend toolbar for additional options
        self.flags = GridAlignment.GRID
        self._grid_tools = []

        r = self.rect
        r.height = 160
        self.rect = r

        left_tool = self.create_tool(self._grid_tools, "left_hl", "grid", self.font,
                                     bind_callback_parameters(self._set_grid_flag, GridAlignment.LEFT),
                                     bind_callback_parameters(self._unset_grid_flag, GridAlignment.LEFT), 64)

        bottom_tool = self.create_tool(self._grid_tools, "bottom_hl", "grid", self.font,
                                       bind_callback_parameters(self._set_grid_flag, GridAlignment.BOTTOM),
                                       bind_callback_parameters(self._unset_grid_flag, GridAlignment.BOTTOM), 64)

        left_tool.selected = bottom_tool.selected = True  # makes sense to start with grid enabled

    def _set_tool(self, which):
        self.active_tool = which

    @property
    def align_bottom(self):
        return self.flags & GridAlignment.BOTTOM

    @property
    def align_left(self):
        return self.flags & GridAlignment.LEFT

    def _set_grid_flag(self, which):
        self.flags |= which

    def _unset_grid_flag(self, which):
        self.flags = self.flags & (~which)
