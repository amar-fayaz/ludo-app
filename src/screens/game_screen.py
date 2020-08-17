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
    roll_button = ObjectProperty(None)
    roll_display = ObjectProperty(None)
    game_board = ObjectProperty(None)
    game_instance = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LudoGameScreen, self).__init__(**kwargs)

    def post_init_steps(self, *args):
        self.game_instance = LudoGame(self.game_board)
        MDApp.get_running_app().game = self.game_instance
        self.game_instance.assign_roll_button_model(self.roll_button)
        self.game_instance.assign_base_to_player(self.game_board.player_homes)
        self.game_instance.set_white_game_paths(self.game_board.game_path)
        self.game_instance.set_winners_podium(self.game_board.winners_podium)

    def roll_die(self):
        roll_value = str(random.randint(1, 6))
        self.roll_display.text = roll_value
        self.game_instance.process_dice_roll(int(roll_value))

    # ------------------- Handle Key Presses -----------------------------
    def handle_key_downs(self, window, key, *args):
        pass
