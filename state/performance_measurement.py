from typing import NamedTuple
import pygame
from .game_state import GameState
from .game_state import GameStateStack
from entities.text import Text, TextAnchor
from entities.entity import EntityManager, Layer
from util import make_vector
import config


class _Measurement(NamedTuple):
    min: int
    avg: float
    max: int


class PerformanceMeasurement(GameState):
    def __init__(self, input_state, target_state: GameState):
        super().__init__(input_state)

        assert target_state is not None

        self.target_state = target_state
        self.entities = EntityManager({Layer.Overlay: set()}, [Layer.Overlay])

        text_position = make_vector(config.screen_rect.right, config.screen_rect.top)

        self.frame_rate = Text(text_position, "Frame Rate", anchor=TextAnchor.TOP_RIGHT)

        text_position.y += self.frame_rate.height
        self.update_rate = Text(text_position, anchor=TextAnchor.TOP_RIGHT)

        text_position.y += self.frame_rate.height
        self.update_stats = Text(text_position, anchor=TextAnchor.TOP_RIGHT)

        text_position.y += self.frame_rate.height
        self.draw_stats = Text(text_position, anchor=TextAnchor.TOP_RIGHT)

        self.last_performance_update = 0

        self.update_performance = _Measurement(0, 0, 0)
        self.update_call_count = 0
        self.update_total_ticks = 0

        self.draw_performance = _Measurement(0, 0, 0)
        self.draw_call_count = 0
        self.draw_total_ticks = 0

        self.entities.register(self.frame_rate)

    def update(self, dt):
        start_tick = pygame.time.get_ticks()
        self.target_state.update(dt)

        elapsed_ticks = pygame.time.get_ticks() - start_tick

        self.update_call_count += 1
        self.update_total_ticks += elapsed_ticks

        self.entities.update(dt)
        self._update_frame_rate()

        self.update_performance = _Measurement(
            min(self.update_performance.min, elapsed_ticks),
            self.update_performance.avg,
            max(self.update_performance.max, elapsed_ticks))

        if pygame.time.get_ticks() - self.last_performance_update > 1000:
            self.last_performance_update = pygame.time.get_ticks()
            self._update_update_text()
            self._update_draw_text()
            self._update_frame_rate()
            self.update_call_count, self.draw_call_count = 0, 0
            self.update_total_ticks, self.draw_total_ticks = 0, 0

    def draw(self, screen):
        start_ticks = pygame.time.get_ticks()
        self.target_state.draw(screen)

        elapsed = pygame.time.get_ticks() - start_ticks
        self.draw_call_count += 1
        self.draw_total_ticks += elapsed

        self.entities.draw(screen)
        self.draw_performance = _Measurement(
            min(self.draw_performance.min, elapsed),
            self.draw_performance.avg,
            max(self.draw_performance.max, elapsed)
        )

    @property
    def finished(self):
        return self.target_state.finished

    @staticmethod
    def measure(state_stack: GameStateStack, target_state: GameState):
        pm = PerformanceMeasurement(target_state.input_state, target_state)
        state_stack.push(pm)

    def _update_update_text(self):
        pass

    def _update_draw_text(self):
        pass

    def _update_frame_rate(self):
        avg_fps = 60. / float(self.draw_call_count) if self.draw_call_count > 0 else 0.
        self.frame_rate.text = f"FPS: {avg_fps:.2f}"

    def _update_update_rate(self):
        avg_updates = 60. / float(self.update_call_count) if self.update_call_count > 0 else 0.
        self.update_rate.text = f"UPS: {avg_updates:.2f}"
