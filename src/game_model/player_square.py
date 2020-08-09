from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty

from ..data.config import *

class PlayerSquare(MDFloatLayout):
    dimension = PLAYER_BASE_DIMENSION
    player_color = ListProperty(WHITE_COLOR)
    color = StringProperty("white")
    outer_square = ObjectProperty(None)
    inner_square = ObjectProperty(None)
    pin1 = ObjectProperty(None)
    pin2 = ObjectProperty(None)
    pin3 = ObjectProperty(None)
    pin4 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlayerSquare, self).__init__(**kwargs)
  

