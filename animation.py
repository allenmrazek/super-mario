from pygame.sprite import Sprite


class Animation(Sprite):
    duration: float
    frames: []

    def __init__(self, frames, duration):
        assert len(frames) > 0
        assert duration >= 0

        super().__init__()

        self.frames = frames
        self.frame_count = len(frames)
        self.duration = duration
        self.current_frame_index = 0
        self.accumulator = 0.0
        self.current_frame = frames[0]
        self.width = frames[0].get_width()
        self.height = frames[0].get_height()

        self.rect = self.image.get_rect()

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        assert value >= 0
        self._duration = value
        self._time_per_frame = self.duration / float(self.frame_count)

    def update(self, elapsed):
        self.accumulator += elapsed

        while 0.0 < self._time_per_frame <= self.accumulator:
            self.accumulator -= self._time_per_frame
            self.next_frame()

    @property
    def frame(self):
        return self.current_frame_index

    @frame.setter
    def frame(self, idx):
        assert 0 <= idx < self.frame_count
        self.current_frame_index = idx
        self.current_frame = self.frames[idx]

    def next_frame(self):
        cur = self.frame + 1

        self.frame = cur if cur < self.frame_count else 0

    @property
    def image(self):
        return self.current_frame

    def __copy__(self):
        """Want a shallow copy essentially (to avoid creating duplicate surfaces in memory
            yet also not include references to changing things, like Rect"""
        inst = Animation(self.frames, self.duration)
        inst.rect = self.rect.copy()

        return inst


class StaticAnimation(Animation):
    def __init__(self, frames):
        # quietly convert parameters to lists if needed. This allows this class to be a truly static "animation"
        # (such that frames are manipulated manually) or actually just a one-frame not-actually-animated thing, which
        # can be interchangeably used anywhere Animation is
        if not isinstance(frames, list):
            frames = [frames]

        super().__init__(frames, 0.0)

    def update(self, elapsed):
        pass


class OneShotAnimation(Animation):
    def __init__(self, frames, duration, on_complete_callback=None):
        if not isinstance(frames, list):  # allow single-frame "animations"
            frames = [frames]

        super().__init__(frames, duration=duration)

        self.on_complete = on_complete_callback
        self.finished = False
        self.num_frames = len(frames)

    @staticmethod
    def from_animation(animation, duration=None, on_complete_callback=None):
        return OneShotAnimation(animation.frames, duration or animation.duration, on_complete_callback)

    def update(self, elapsed):
        if self.finished:
            return

        last_accum = self.accumulator
        last_frame = self.current_frame_index

        super().update(elapsed)

        if self.current_frame_index < last_frame or (self.num_frames == 1 and self.accumulator < last_accum):
            # note: we use accumulator above because some "animations" (static, temporary) only have one frame
            if self.on_complete is not None:
                self.on_complete()

            self.finished = True
