from paddle import Paddle
from random import Random


class ComputerPaddle(Paddle):

    def __init__(self, surface, name, y_bounds, init_pos=(0, 0), speed=1, rect_dims=(2, 10), color=(0, 0, 0)):
        super().__init__(surface, name, y_bounds, init_pos=init_pos, speed=speed, rect_dims=rect_dims, color=color)
        self._y_target = (self._y_bounds[0] + self._y_bounds[1]) / 2

    def update_computer(self, game_ball, prev_ball_velocity):

        b_v = game_ball.get_velocity()
        b_pos = game_ball.get_pos()
        my_pos = self._pos

        ball_changed_direction = b_v[0] * prev_ball_velocity[0] < 0 or b_v[1] * prev_ball_velocity[1] < 0

        if ball_changed_direction:
            c0 = self._y_bounds[0]
            c1 = self._y_bounds[1]
            k = my_pos[0]
            y_int = (self._y_bounds[0] + self._y_bounds[1]) / 2

            if my_pos[0] < b_pos[0]:
                if b_v[0] < 0:
                    c = c0 if b_v[1] < 0 else c1
                    y_int = ComputerPaddle._get_y_intersection(b_pos, b_v, k)
                    if not c0 <= y_int <= c1:
                        x_int = ComputerPaddle._get_x_intersection(b_pos, b_v, c)
                        while x_int > k:
                            b_pos = (x_int, c)
                            b_v = (b_v[0], -b_v[1])
                            c = c0 if b_v[1] < 0 else c1
                            x_int = ComputerPaddle._get_x_intersection(b_pos, b_v, c)
                        y_int = ComputerPaddle._get_y_intersection(b_pos, b_v, k)
            else:
                if b_v[0] > 0:
                    c = c0 if b_v[1] < 0 else c1
                    y_int = ComputerPaddle._get_y_intersection(b_pos, b_v, k)

                    if not c0 <= y_int <= c1:
                        x_int = ComputerPaddle._get_x_intersection(b_pos, b_v, c)
                        while x_int < k:
                            b_pos = (x_int, c)
                            b_v = (b_v[0], -b_v[1])
                            c = c0 if b_v[1] < 0 else c1
                            x_int = ComputerPaddle._get_x_intersection(b_pos, b_v, c)
                        y_int = ComputerPaddle._get_y_intersection(b_pos, b_v, k)
            y_int += Random().randint(-self.get_height() // 4, self.get_height() // 4)
            self._move_towards(y_int)
            self._y_target = y_int
        if my_pos[1] - self._speed <= self._y_target <= my_pos[1] + self._speed:
            self.released_up()
            self.released_down()
        self.update()

    def _move_towards(self, y):
        if y > self._pos[1]:
            self.pressed_down()
        elif y < self._pos[1]:
            self.pressed_up()

    @staticmethod
    def _get_x_intersection(r0, v, y):
        t = (y - r0[1]) / v[1]
        return r0[0] + t * v[0]

    @staticmethod
    def _get_y_intersection(r0, v, x):
        t = (x - r0[0]) / v[0]
        return r0[1] + t * v[1]
