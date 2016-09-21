import pygame
from paddle import Paddle
from computer_paddle import ComputerPaddle
from ball import Ball
import math


class Game:

    def __init__(self):
        pygame.init()
        self._win = (1200, 800)
        self._title = 'Pong'

        pygame.display.set_caption(self._title)
        pygame.display.set_mode(self._win)
        self._surface = pygame.display.get_surface()
        self._clock = pygame.time.Clock()

        self._font_sizes = [20, 40, 60]
        self._fps = 140
        self._idle_fps = 10
        self._p1_key_up = pygame.K_w
        self._p1_key_down = pygame.K_s
        self._p1_key_slow = pygame.K_LSHIFT
        self._p2_key_up = pygame.K_UP
        self._p2_key_down = pygame.K_DOWN
        self._p2_key_slow = pygame.K_RCTRL
        self._font_name = 'times'

    def _set_game_state(self, num_humans):
        num_humans %= 3
        paddle_y = self._win[1] / 2
        dist_from_edge = 20
        p1_pos = (dist_from_edge, paddle_y)
        p2_pos = (self._win[0] - dist_from_edge, paddle_y)
        paddle_dims = (10, 70)
        win_rect = (0, 0) + self._win
        self._paddle_speed = 8

        if num_humans == 2:
            self._paddle1 = Paddle(self._surface, 'Player 1',
                                   (0, self._win[1]), p1_pos, self._paddle_speed, paddle_dims)
            self._paddle2 = Paddle(self._surface, 'Player 2',
                                   (0, self._win[1]), p2_pos, self._paddle_speed, paddle_dims)
        elif num_humans == 1:
            self._paddle1 = Paddle(self._surface, 'Player', (0, self._win[1]), p1_pos, self._paddle_speed, paddle_dims)
            self._paddle2 = ComputerPaddle(self._surface, 'CPU',
                                           (0, self._win[1]), p2_pos, self._paddle_speed, paddle_dims)
        elif num_humans == 0:
            self._paddle1 = ComputerPaddle(self._surface, 'CPU 1',
                                           (0, self._win[1]), p1_pos, self._paddle_speed, paddle_dims)
            self._paddle2 = ComputerPaddle(self._surface, 'CPU 2',
                                           (0, self._win[1]), p2_pos, self._paddle_speed, paddle_dims)

        self._ball_speed = 550

        v = self._get_v(self._ball_speed, 180)
        self._background_color = (255, 255, 255)
        b_rad = 3
        self._ball = Ball(self._surface, win_rect, (self._win[0]/2, self._win[1]/2), v, radius=b_rad,
                          color=(255, 0, 0))
        self._world_objects = [self._paddle1, self._paddle2, self._ball]

    def _get_v(self, speed, angle_deg):
        v = speed / self._fps
        return v * math.cos(math.radians(angle_deg)), v * math.sin(math.radians(angle_deg))

    def _game_loop(self):
        run = True
        while run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False
                elif e.type == pygame.KEYDOWN:
                    k = e.key
                    if k == self._p1_key_down:
                        self._paddle1.pressed_down()
                    elif k == self._p1_key_up:
                        self._paddle1.pressed_up()
                    elif k == self._p2_key_down:
                        self._paddle2.pressed_down()
                    elif k == self._p2_key_up:
                        self._paddle2.pressed_up()
                    elif k == self._p1_key_slow:
                        self._paddle1.pressed_slow()
                    elif k == self._p2_key_slow:
                        self._paddle2.pressed_slow()
                elif e.type == pygame.KEYUP:
                    k = e.key
                    if k == self._p1_key_down:
                        self._paddle1.released_down()
                    elif k == self._p1_key_up:
                        self._paddle1.released_up()
                    elif k == self._p2_key_down:
                        self._paddle2.released_down()
                    elif k == self._p2_key_up:
                        self._paddle2.released_up()
                    elif k == self._p1_key_slow:
                        self._paddle1.released_slow()
                    elif k == self._p2_key_slow:
                        self._paddle2.released_slow()

            prev_ball_v = self._ball.get_velocity()
            self._ball.update([self._paddle1, self._paddle2])

            if isinstance(self._paddle1, ComputerPaddle):
                self._paddle1.update_computer(self._ball, prev_ball_v)
            else:
                self._paddle1.update()
            if isinstance(self._paddle2, ComputerPaddle):
                self._paddle2.update_computer(self._ball, prev_ball_v)
            else:
                self._paddle2.update()

            self._surface.lock()
            self._surface.fill(self._background_color)

            for obj in self._world_objects:
                obj.draw()

            self._surface.unlock()
            pygame.display.update()
            self._clock.tick(self._fps)

            if self._ball.is_on_lower_x_bound():
                self._player_win(self._paddle2.get_name())
                run = False
            elif self._ball.is_on_upper_x_bound():
                self._player_win(self._paddle1.get_name())
                run = False

    def _message_to_screen(self, font, msg, color, y_displace=0):
        screen_text = font.render(msg, True, color)
        size = font.size(msg)
        self._surface.unlock()
        self._surface.blit(screen_text, [self._win[0] / 2 - size[0] / 2, self._win[1] / 2 - size[1] / 2 + y_displace])

    def _player_win(self, player_name):
        run = True
        win_msg = player_name + ' won! Press p to play again!'
        win_font = self._get_font(self._font_sizes[1])
        while run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    Game._quit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_p:
                        self.play()
                        run = False
            self._message_to_screen(win_font, win_msg,
                                    (0, 0, 255), -100)
            pygame.display.update()
            self._clock.tick(self._idle_fps)

    def _get_font(self, size):
        return pygame.font.SysFont(self._font_name, size)

    def play(self):
        self._set_game_state(2)
        self._game_loop()
        self._quit()

    @staticmethod
    def _quit():
        pygame.quit()
        quit()
