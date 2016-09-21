
class WorldObject:

    def __init__(self, init_pos=(0, 0)):
        self._pos = init_pos

    def get_pos(self):
        return self._pos

    def set_pos(self, x, y):
        self._pos = (x, y)

    def set_pos_x(self, x):
        self.set_pos(x, self._pos[1])

    def set_pos_y(self, y):
        self.set_pos(self._pos[0], y)
