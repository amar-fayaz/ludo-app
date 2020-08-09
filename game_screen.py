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
from data.config import *

class LudoGameScreen(MDScreen):
    current_roll = NumericProperty(0)
    roll_display = ObjectProperty(None)
    game_board = ObjectProperty(None)

    def roll_die(self):
        self.roll_display.text = str(random.randint(1, 6))

    # ------------------- Handle Key Presses -----------------------------
    def handle_key_downs(self, window, key, *args):
        pass

class GameSquare(MDFloatLayout):
    fill_color = ListProperty(WHITE_COLOR)
    border_color = ListProperty(BLACK_COLOR)

class UnitSquare(GameSquare):
    color = StringProperty("white")
    content = OptionProperty("None", options=["None", "Icon", "Color"])
    unit_dimension = NumericProperty(UNIT_SQUARE_DIMENSION)
    safe_zone = BooleanProperty(False)

    def __init__ (self, option="None", **kwargs):
        super(UnitSquare, self).__init__(**kwargs)
        self.content = option
        if not (option == "None"):
            self.add_widget(Image(
                source="./assets/arrow_left.png",
                size=(self.unit_dimension - 1, self.unit_dimension - 1),
                pos_hint={"center_x": 0.5, "center_y": 0.5}
                ))

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
  

class LudoBoard(GameSquare):
    board_dimension = NumericProperty(BOARD_DIMENSION)
    unit_dimension = NumericProperty(UNIT_SQUARE_DIMENSION)

    bottom_left_base = ObjectProperty(None)
    top_left_base = ObjectProperty(None)
    top_right_base = ObjectProperty(None)
    bottom_right_base = ObjectProperty(None)

    winners_podium = ObjectProperty(None)
    
    top_left_path_end = ObjectProperty(None)
    top_right_path_end = ObjectProperty(None)
    bottom_left_path_end = ObjectProperty(None)
    bottom_right_path_end = ObjectProperty(None)

    game_path = ListProperty([])
    bottom_left_home_stretch = ListProperty([])
    top_left_home_stretch = ListProperty([])
    top_right_home_stretch = ListProperty([])
    bottom_right_home_stretch = ListProperty([])
    home_stretch = ReferenceListProperty(bottom_left_home_stretch, top_left_home_stretch, \
                                        top_right_home_stretch, bottom_right_home_stretch)

    def __init__(self, **kwargs):
        super(LudoBoard, self).__init__(**kwargs)
        Clock.schedule_once(self.create_unit_squares)
        #self.bind(pos=self.create_unit_squares)

    def create_unit_squares(self, *args):
        self.create_game_path()
        self.create_home_stretch()
        for path in self.game_path:
            self.add_widget(path)   

        for stretch in self.home_stretch:
            for square in stretch:
                self.add_widget(square) 


    def add_to_game_path(self, unit_square):
        self.game_path.append(unit_square)

    def create_game_path(self):
        # --------- bottom left area --------------
        for i in range(0, 6):        
            current_square = UnitSquare(
                pos = (self.x + 6* self.unit_dimension,
                 self.y + i * self.unit_dimension),
                color = self.bottom_left_base.color if i == 1 else "white"
            )
            self.add_to_game_path(current_square)

        for i in range(0, 6):
            current_square = UnitSquare(
                pos = (self.x + 5* self.unit_dimension - i * self.unit_dimension,
                 self.y + 6 * self.unit_dimension),
            )
            self.add_to_game_path(current_square)

        #path_end for top left
        self.top_left_path_end = UnitSquare(
            pos = (self.x, self.y + 7 * self.unit_dimension)
        )

        self.add_to_game_path(self.top_left_path_end)

        # -------------- top left area ----------------------
        for i in range(0, 6):
            current_square = UnitSquare(
                pos = (self.x + i * self.unit_dimension,
                 self.y + 8 * self.unit_dimension),
                color = self.top_left_base.color if i == 1 else "white"
            )
            self.add_to_game_path(current_square)

        for i in range(0, 6):
            current_square = UnitSquare(
                pos = (self.x + 6 * self.unit_dimension,
                 self.y + 9 * self.unit_dimension + i * self.unit_dimension),
            )
            self.add_to_game_path(current_square)

        # path end for top right
        self.top_right_path_end = UnitSquare(
            pos = (self.x + 7 * self.unit_dimension, self.y + 14 * self.unit_dimension)
        )

        self.add_to_game_path(self.top_right_path_end)

        # ------------------ top right area -------------------------
        for i in range(0, 6):
            current_square = UnitSquare(
                pos = (self.x + 8 * self.unit_dimension,
                 self.y + 14 * self.unit_dimension - i * self.unit_dimension),
                color = self.top_right_base.color if i == 1 else "white"
            )
            self.add_to_game_path(current_square)

        for i in range(0, 6):
            current_square = UnitSquare(
                pos = (self.x + 9 * self.unit_dimension + i * self.unit_dimension,
                 self.y + 8 * self.unit_dimension),
            )
            self.add_to_game_path(current_square)

        # path end for bottom right
        self.bottom_right_path_end = UnitSquare(
            pos = (self.x + 14 * self.unit_dimension, self.y + 7 * self.unit_dimension)
        )
        self.add_to_game_path(self.bottom_right_path_end)


        # ------------------botom right area --------------------------
        for i in range(0, 6):
            current_square = UnitSquare(
                pos = (self.x + 14 * self.unit_dimension - i * self.unit_dimension,
                 self.y + 6 * self.unit_dimension),
                color = self.bottom_right_base.color if i == 1 else "white"
            )
            self.add_to_game_path(current_square)

        for i in range(0, 6):
            current_square = UnitSquare(
                pos = (self.x + 8 * self.unit_dimension ,
                 self.y + 5 * self.unit_dimension - i * self.unit_dimension),
            )
            self.add_to_game_path(current_square)

        #path end for bottom left
        self.bottom_left_path_end = UnitSquare(
            pos = (self.x + 7 * self.unit_dimension, self. y)
        )
        self.add_to_game_path(self.bottom_left_path_end)

    def create_home_stretch(self):
        # Bottom Left Player
        for i in range(0, 5):
            self.bottom_left_home_stretch.append(UnitSquare(
                pos = (self.x + 7 * self.unit_dimension, self.y + self.unit_dimension + i * self.unit_dimension),
                color = self.bottom_left_base.color
            ))

        # Top Left Player
        for i in range(0, 5):
            self.top_left_home_stretch.append(UnitSquare(
                pos = (self.x + (1+i) * self.unit_dimension, self.y + 7 * self.unit_dimension),
                color = self.top_left_base.color
            ))

        # Top Right Player
        for i in range(0, 5):
            self.top_right_home_stretch.append(UnitSquare(
                pos = (self.x + 7 * self.unit_dimension, self.y + (13 - i) * self.unit_dimension),
                color = self.top_right_base.color
            ))

        # Bottom Right Player
        for i in range(0, 5):
            self.bottom_right_home_stretch.append(UnitSquare(
                pos = (self.x + (13- i) * self.unit_dimension, self.y + 7 * self.unit_dimension),
                color = self.bottom_right_base.color
            ))


        

