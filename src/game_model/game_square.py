from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ListProperty

from ..data.config import *

class GameSquare(MDFloatLayout):
    fill_color = ListProperty(WHITE_COLOR)
    border_color = ListProperty(BLACK_COLOR)
