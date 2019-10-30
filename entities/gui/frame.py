from .element import Element, Anchor
from pygame import Rect


class Frame(Element):
    """Frame's main purpose is to group orderable children (think windows which can overlap). It has no visual
    aspect on the screen itself"""
    def __init__(self, window_position, size, anchor=Anchor.TOP_LEFT):
        super().__init__(window_position, Rect(window_position[0], window_position[1], *size), anchor)
