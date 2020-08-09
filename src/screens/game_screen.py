from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import NumericProperty, ListProperty, \
                            ObjectProperty, ReferenceListProperty, \
                            OptionProperty, BooleanProperty, \
                            StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image

from kivymd.uix.textfield import MDTextField

from kivymd.uix.button import MDRoundImageButton

import random
from ..data.config import *

class LudoGameScreen(MDScreen):
    current_roll = NumericProperty(0)
    roll_display = ObjectProperty(None)
    game_board = ObjectProperty(None)

    def roll_die(self):
        self.roll_display.text = str(random.randint(1, 6))

    # ------------------- Handle Key Presses -----------------------------
    def handle_key_downs(self, window, key, *args):
        pass
