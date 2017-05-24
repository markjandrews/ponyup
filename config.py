from ponyup.pbdraw import PowerBallDraw
from ponyup.ozdraw import OzLottoDraw
from ponyup.pbphdraw import PowerBallPHDraw


class Config(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


configs = {'pb': Config(cost_per_game=0.92, klass=PowerBallDraw),
           'pbph': Config(cost_per_game=18.60, klass=PowerBallPHDraw),
           'oz': Config(cost_per_game=1.30, klass=OzLottoDraw)}
