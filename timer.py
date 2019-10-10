import pygame


class Timer:
    def __init__(self):
        self._last_tick = pygame.time.get_ticks()
        self._elapsed = 0.0
        self._paused = False

    def update(self):
        tick = pygame.time.get_ticks()
        elapsed_ms = tick - self._last_tick
        self._last_tick = tick

        self._elapsed = elapsed_ms / 1000.0 if not self._paused else 0.0

    def pause(self, tf):
        self._paused = tf

        if self._paused:
            self._elapsed = 0.0

    @property
    def elapsed(self):
        return self._elapsed

    def reset(self):
        self._last_tick = pygame.time.get_ticks()
        self._elapsed = 0.0


game_timer = Timer()
