class Position:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x_pos):
        self._x = x_pos

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y_pos):
        self._y = y_pos
