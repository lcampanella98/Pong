from world_object import WorldObject
import pygame
import tools


class Paddle (WorldObject):

    def __init__(self, surface, name, y_bounds, init_pos=(0, 0), speed=1, rect_dims=(2, 10), color=(0, 0, 0)):
        super().__init__(init_pos)
        self._rect_dims = rect_dims
        self._surface = surface
        self._color = color
        self._speed = speed
        self._vy = 0
        self._y_bounds = y_bounds
        self._name = name

    def get_name(self):
        return self._name

    def _move_vertical(self, y_inc):
        self.set_pos_y(self._pos[1] + y_inc)

    def pressed_up(self):
        self._vy = -self._speed

    def pressed_down(self):
        self._vy = self._speed

    def released_up(self):
        if self._vy < 0:
            self._vy = 0

    def released_down(self):
        if self._vy > 0:
            self._vy = 0

    def pressed_slow(self):
        self._vy /= 2
        self._speed /= 2

    def released_slow(self):
        self._vy *= 2
        self._speed *= 2

    def is_rect_colliding_with_me(self, rect):
        return tools.are_rectangles_colliding(self.get_rect(), rect)

    def update(self):
        if self._vy != 0:
            self._move_vertical(self._vy)
        if self.get_top_y() < self._y_bounds[0]:
            self._set_pos_from_top_y(self._y_bounds[0] + 1)
        elif self.get_bottom_y() > self._y_bounds[1]:
            self._set_pos_from_bottom_y(self._y_bounds[1] - 1)

    def get_top_y(self):
        return self._pos[1] - self.get_height() / 2

    def get_bottom_y(self):
        return self._pos[1] + self.get_height() / 2

    def _set_pos_from_top_y(self, top_y):
        self.set_pos_y(top_y + self.get_height() / 2)

    def _set_pos_from_bottom_y(self, bottom_y):
        self.set_pos_y(bottom_y - self.get_height() / 2)

    def draw(self):
        pygame.draw.rect(self._surface, self._color, self.get_rect())

    def get_rect(self):
        return (self._pos[0] - self.get_width() / 2, self._pos[1] - self.get_height() / 2) + self._rect_dims

    def get_width(self):
        return self._rect_dims[0]

    def get_height(self):
        return self._rect_dims[1]
