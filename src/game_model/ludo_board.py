from kivy.properties import NumericProperty, ListProperty, \
                            ObjectProperty, ReferenceListProperty
from kivy.clock import Clock

from ..data.config import *
from .game_square import GameSquare
from .unit_square import  UnitSquare

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

    player1_home = ReferenceListProperty(bottom_left_base, bottom_left_home_stretch)
    player2_home = ReferenceListProperty(top_left_base, top_left_home_stretch)
    player3_home = ReferenceListProperty(top_right_base, top_right_home_stretch)
    player4_home = ReferenceListProperty(bottom_right_base, bottom_right_home_stretch)
    player_homes = ReferenceListProperty(player1_home, player2_home, player3_home, player4_home)

    def __init__(self, **kwargs):
        super(LudoBoard, self).__init__(**kwargs)
        Clock.schedule_once(self.post_init_steps)
        #self.bind(pos=self.create_unit_squares)

    def post_init_steps(self, *args):
        self.create_game_path()
        self.create_home_stretch()

        for path in self.game_path:
            self.add_widget(path)   

        for stretch in self.home_stretch:
            for square in stretch:
                self.add_widget(square) 
        self.parent.post_init_steps()

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


        

