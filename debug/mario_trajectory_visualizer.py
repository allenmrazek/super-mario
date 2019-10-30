import math
import pygame
from util import distance_squared
from util import make_vector
from util import world_to_screen


class _JumpTrajectory:
    DRAW_COLOR = pygame.Color('green')
    MIN_SEGMENT_LENGTH = 3

    def __init__(self, mario):
        self.points = []
        self.max_velocity = pygame.Vector2()
        self.initial_velocity_x = math.fabs(mario.get_velocity().x)
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

    def update(self, current_speed, view_rect):
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

    def draw(self, screen, view_rect):
        if len(self.points) > 1:
            corrected_points = [world_to_screen(x, view_rect) for x in self.points]

            pygame.draw.lines(screen, self.DRAW_COLOR, False, corrected_points)
            screen.blit(self.debug_image, world_to_screen(self.rect.topleft, view_rect))


class JumpTrajectoryVisualizer:
    TRAJECTORY_COUNT_MAX = 3

    def __init__(self):
        self.trajectories = []
        self.current_trajectory = None
        self.last_known_position = None

    def update(self, mario, view_rect):
        if self.last_known_position is None:
            self.last_known_position = self.get_mario_feet_position(mario)

        if self.current_trajectory is None and mario.is_airborne:
            self.current_trajectory = _JumpTrajectory(mario)

            self.trajectories.append(self.current_trajectory)
            self.trajectories = self.trajectories[-self.TRAJECTORY_COUNT_MAX:]
            self.current_trajectory.add(self.last_known_position)

        elif not mario.is_airborne:
            if self.current_trajectory is not None:
                self.current_trajectory.add(self.get_mario_feet_position(mario))

            self.current_trajectory = None

        if self.current_trajectory is not None:
            self.current_trajectory.add(self.get_mario_feet_position(mario))
            self.current_trajectory.update(mario.get_velocity(), view_rect)

        self.last_known_position = self.get_mario_feet_position(mario)

    @staticmethod
    def get_mario_feet_position(mario):
        return mario.get_position() + make_vector(mario.rect.width // 2, mario.rect.height)

    def draw(self, screen, view_rect):
        for traj in self.trajectories:
            traj.draw(screen, view_rect)
