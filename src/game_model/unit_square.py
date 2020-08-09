
from kivy.properties import NumericProperty, BooleanProperty, \
                            OptionProperty, StringProperty


from .game_square import GameSquare
from ..data.config import *

class UnitSquare(GameSquare):
    color = StringProperty("white")
    content = OptionProperty("None", options=["None", "Icon", "Color"])
    unit_dimension = NumericProperty(UNIT_SQUARE_DIMENSION)
    safe_zone = BooleanProperty(False)

    def __init__ (self, option="None", **kwargs):
        super(UnitSquare, self).__init__(**kwargs)
        self.content = option
        # if not (option == "None"):
        #     self.add_widget(Image(
        #         source="./assets/arrow_left.png",
        #         size=(self.unit_dimension - 1, self.unit_dimension - 1),
        #         pos_hint={"center_x": 0.5, "center_y": 0.5}
        #         ))