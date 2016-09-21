from world_object import WorldObject
import math
import pygame


class Ball(WorldObject):

    def __init__(self, surface, window, init_pos=(0, 0), init_velocity_vector=(1, 1), radius=1, color=(255, 255, 255)):
        super().__init__(init_pos)
        self._v = init_velocity_vector
        self._radius = radius
        self._speed = math.sqrt(self._v[0]*self._v[0]+self._v[1]*self._v[1])
        self._surface = surface
        self._color = color
        self._win = window

    def collided_on_wall(self):
        self._v = (self._v[0], -self._v[1])

    def is_on_lower_x_bound(self):
        return self._pos[0] - self._radius < self._win[0]

    def is_on_upper_x_bound(self):
        return self._pos[0] + self._radius > self._win[0] + self._win[2]

    def _collided_on_paddle(self, paddle):
        theta = 180 * (self._pos[1] - paddle.get_pos()[1]) / paddle.get_height()
        a = 9.672824e-9
        b = 4.693818
        theta += math.copysign(a * math.pow(math.fabs(theta), b), -theta)
        if self._pos[0] < paddle.get_pos()[0]:
            theta += 180
        theta = math.radians(theta)
        self._v = (math.copysign(self._speed, math.cos(theta)), self._speed * math.tan(theta))

    def get_rect(self):
        return (self._pos[0] - self._radius, self._pos[1] - self._radius) + (2 * self._radius, 2 * self._radius)

    def update(self, paddles):
        if self._pos[1] - self._radius <= self._win[1] or self._pos[1] + self._radius >= self._win[1] + self._win[3]:
            self.collided_on_wall()
        else:
            for p in paddles:
                if self._is_colliding_on_paddle(p):
                    self._collided_on_paddle(p)
                    break

        self.set_pos(self._pos[0] + self._v[0], self._pos[1] + self._v[1])

    def _is_colliding_on_paddle(self, paddle):
        return paddle.is_rect_colliding_with_me(self.get_rect())

    def draw(self):
        pygame.draw.circle(self._surface, self._color, self._int_pos(), self._radius)

    def _int_pos(self):
        return int(self._pos[0]), int(self._pos[1])

    def get_velocity(self):
        return self._v