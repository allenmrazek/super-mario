import math
import pygame
from util import distance_squared
from util import copy_vector


class _JumpTrajectory:
    DRAW_COLOR = pygame.Color('green')
    MIN_SEGMENT_LENGTH = 3

    def __init__(self, mario):
        self.points = []
        self.max_velocity = pygame.Vector2()
        self.initial_velocity_x = math.fabs(mario.velocity.x)
        self.debug_image = pygame.font.SysFont(None, 18).render('', True, (255, 0, 0))
        self.rect = self.debug_image.get_rect()

    def add(self, pt):
        # don't add this point unless it will help visualize our line with at least [min segment length] more pixels
        if (len(self.points) > 0 and
                distance_squared(*self.points[-1:], pt) > self.MIN_SEGMENT_LENGTH * self.MIN_SEGMENT_LENGTH) \
                or len(self.points) == 0:
            new_point = pygame.Vector2()
            new_point.x, new_point.y = pt.x, pt.y

            self.points.append(new_point)

            if len(self.points) == 1:
                self.rect.center = self.points[0]

    def update(self, current_speed):
        self.max_velocity.x = self.max_velocity.x if math.fabs(current_speed.x) < self.max_velocity.x \
            else math.fabs(current_speed.x)
        self.max_velocity.y = self.max_velocity.y if math.fabs(current_speed.y) < self.max_velocity.y \
            else math.fabs(current_speed.y)

        if len(self.points) > 0:
            self.rect.center = min(self.points, key=lambda pos: pos.y)
            self.debug_image = pygame.font.SysFont(None, 18).render(f'{self.max_velocity.x:0.0f},'
                                                                    f'{self.max_velocity.y:0.0f},'
                                                                    f'{self.initial_velocity_x:0.0f}',
                                                                    True, (255, 0, 0))

    def draw(self, screen):
        if len(self.points) > 1:
            pygame.draw.lines(screen, self.DRAW_COLOR, False, self.points)
            screen.blit(self.debug_image, self.rect)


class JumpTrajectoryVisualizer:
    TRAJECTORY_COUNT_MAX = 3

    def __init__(self):
        self.trajectories = []
        self.current_trajectory = None
        self.last_known_position = None

    def update(self, mario):
        if self.last_known_position is None:
            self.last_known_position = copy_vector(mario.position)

        if self.current_trajectory is None and mario.is_airborne:
            self.current_trajectory = _JumpTrajectory(mario)

            self.trajectories.append(self.current_trajectory)
            self.trajectories = self.trajectories[-self.TRAJECTORY_COUNT_MAX:]
            self.current_trajectory.add(self.last_known_position)

        elif not mario.is_airborne:
            if self.current_trajectory is not None:
                self.current_trajectory.add(mario.position)

            self.current_trajectory = None

        if self.current_trajectory is not None:
            self.current_trajectory.add(mario.position)
            self.current_trajectory.update(mario.velocity)

        self.last_known_position = copy_vector(mario.position)

    def draw(self, screen):
        for traj in self.trajectories:
            traj.draw(screen)
