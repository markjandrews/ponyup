from ponyup.pbdraw import PowerBallDraw
from ponyup.ozdraw import OzLottoDraw


class Config(object):
    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

configs = {'pb': Config(klass=PowerBallDraw),
           'oz': Config(klass=OzLottoDraw)}
