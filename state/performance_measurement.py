from typing import NamedTuple
import pygame
from .game_state import GameState
from .game_state import GameStateStack
from entities.gui.element import Anchor
from entities.gui.text import Text
from entities.entity import Layer
from entities.entity_manager import EntityManager
from util import make_vector
import config


class _Measurement(NamedTuple):
    min: int
    avg: float
    max: int
    max_overall: int


class PerformanceMeasurement(GameState):
    def __init__(self, state_stack, game_events, target_state: GameState):
        super().__init__(game_events)

        assert target_state is not None

        self.target_state = target_state
        self.state_stack = state_stack

        self.entities = EntityManager([Layer.Interface], [Layer.Interface])

        text_position = make_vector(config.screen_rect.right, config.screen_rect.top)

        font = pygame.font.SysFont(None, 20)

        self.frame_rate = Text(text_position, "Frame Rate", anchor=Anchor.TOP_RIGHT, font=font)

        text_position.y += self.frame_rate.height
        self.draw_stats = Text(text_position, anchor=Anchor.TOP_RIGHT, text="???", font=font)

        text_position.y += self.frame_rate.height
        self.update_rate = Text(text_position, anchor=Anchor.TOP_RIGHT, text="???", font=font)

        text_position.y += self.frame_rate.height
        self.update_stats = Text(text_position, anchor=Anchor.TOP_RIGHT, text="???", font=font)

        self.entities.register([self.frame_rate, self.draw_stats, self.update_rate, self.update_stats])

        self.last_performance_update = 0

        self.update_performance = _Measurement(0, 0, 0, 0)
        self.update_call_count = 0
        self.update_total_ticks = 0

        self.draw_performance = _Measurement(0, 0, 0, 0)
        self.draw_call_count = 0
        self.draw_total_ticks = 0

    def update(self, dt):
        start_tick = pygame.time.get_ticks()
        self.target_state.update(dt)

        elapsed_ticks = pygame.time.get_ticks() - start_tick

        self.update_call_count += 1
        self.update_total_ticks += elapsed_ticks

        self.entities.update(dt, pygame.Rect(0, 0, 0, 0))

        self.update_performance = _Measurement(
            min(self.update_performance.min, elapsed_ticks),
            self.update_performance.avg,
            max(self.update_performance.max, elapsed_ticks),
            max(self.update_performance.max_overall, self.update_performance.max))

        current_tick = pygame.time.get_ticks()

        if current_tick - self.last_performance_update > 1000:
            delta_seconds = (current_tick - self.last_performance_update) / 1000.0

            # these two are interested in tracking min, avg, and max elapsed ticks for update and draw
            self._do_update_info_text()
            self._do_draw_info_text()

            # this tracks frames per second that are actually rendered
            self._do_frame_rate(delta_seconds)

            # this tracks updates per second. This does not necessarily equal frame rate
            self._do_update_rate(delta_seconds)

            self.update_call_count, self.draw_call_count = 0, 0
            self.update_total_ticks, self.draw_total_ticks = 0, 0
            self.last_performance_update = current_tick

    def draw(self, screen):
        start_ticks = pygame.time.get_ticks()
        self.target_state.draw(screen)

        elapsed = pygame.time.get_ticks() - start_ticks
        self.draw_call_count += 1
        self.draw_total_ticks += elapsed

        self.entities.draw(screen, pygame.Rect(0, 0, 0, 0))
        self.draw_performance = _Measurement(
            min(self.draw_performance.min, elapsed),
            self.draw_performance.avg,
            max(self.draw_performance.max, elapsed),
            max(self.draw_performance.max_overall, self.draw_performance.max)
        )

    def activated(self):
        self.target_state.activated()

    def deactivated(self):
        self.target_state.deactivated()

    @property
    def finished(self):
        return self.target_state.finished

    @staticmethod
    def measure(state_stack: GameStateStack, target_state: GameState):
        pm = PerformanceMeasurement(state_stack, target_state.game_events, target_state)
        state_stack.push(pm)

    def _do_update_info_text(self):
        # calc avg
        avg = (self.update_performance.min + self.update_performance.max) * 0.5
        self.update_stats.text = f"U: {self.update_performance.min}, {avg:.2f}," \
                                 f" {self.update_performance.max}, {self.update_performance.max_overall}"
        self.update_performance = \
            _Measurement(0, avg, 0, max(self.update_performance.max_overall, self.update_performance.max))

    def _do_draw_info_text(self):
        avg = (self.draw_performance.min + self.draw_performance.max) * 0.5
        self.draw_stats.text = f"D: {self.draw_performance.min}, {avg:.2f}," \
                               f" {self.draw_performance.max}, {self.draw_performance.max_overall}"
        self.draw_performance = \
            _Measurement(0, avg, 0, max(self.draw_performance.max_overall, self.draw_performance.max))

    def _do_frame_rate(self, delta_seconds):
        if delta_seconds > 0:
            avg_fps = float(self.draw_call_count) / delta_seconds
            self.frame_rate.text = f"FPS: {avg_fps:.2f}"
        else:
            self.frame_rate.text = "FPS: ???"

    def _do_update_rate(self, delta_seconds):
        if delta_seconds > 0:
            avg_updates = float(self.update_call_count) / delta_seconds
            self.update_rate.text = f"UPS: {avg_updates:.2f}"
        else:
            self.update_rate.text = "UPS: ???"
