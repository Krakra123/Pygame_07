class GameVariable(object):

    WITDH, HEIGHT = 1400, 600

    _current_fps = 0
    @property
    def current_fps(self):
        return type(self)._current_fps
    @current_fps.setter
    def current_fps(self, val):
        type(self)._current_fps = val

    _ingame_time = 0
    @property
    def ingame_time(self):
        return type(self)._ingame_time
    @ingame_time.setter
    def ingame_time(self, val):
        type(self)._ingame_time = val

    PIXEL_PER_DISTANCE = 60

    GRAVITY = -9.8
    ground_level = 450

    game_speed = 15