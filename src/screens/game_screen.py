from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
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
from ..game_engine.LudoGame import LudoGame

class LudoGameScreen(MDScreen):
    current_roll = NumericProperty(0)
    roll_display = ObjectProperty(None)
    game_board = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LudoGameScreen, self).__init__(**kwargs)
        app_instance = MDApp.get_running_app()
        app_instance.game = LudoGame()
        Clock.schedule_once(self.post_init_steps)

    def post_init_steps(self, *args):
        app_instance = MDApp.get_running_app()
        app_instance.game.assign_base_to_player(self.game_board.player_homes)

    def roll_die(self):
        self.roll_display.text = str(random.randint(1, 6))

    # ------------------- Handle Key Presses -----------------------------
    def handle_key_downs(self, window, key, *args):
        pass
