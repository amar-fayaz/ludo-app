from .Player import Player
from .PathUnit import PathUnit
from kivy.clock import Clock

class LudoGame():
    def __init__(self, game_board):
        # Player Starting Indexes are
        starting_indexes = [1, 14, 27, 40]
        self.safe_zones = starting_indexes + [9, 22, 35, 48]
        self.GameBoard = game_board
        self.Player1 = Player(starting_indexes[0])
        self.Player2 = Player(starting_indexes[1])
        self.Player3 = Player(starting_indexes[2])
        self.Player4 = Player(starting_indexes[3])
        self.Players = [self.Player1, self.Player2, \
                        self.Player3, self.Player4]
        self.current_player = self.Player1
        self.current_roll = -1
        self.roll_button_model = None
        self.WhitePaths = []

    def set_white_game_paths(self, white_path_array):
        for path in white_path_array:
            self.WhitePaths.append(PathUnit(path))
        
        for index in self.safe_zones:
            self.WhitePaths[index].safe_zone = True        

    def assign_base_to_player(self, player_home_list):
        for player, home in zip(self.Players, player_home_list):
            player.set_base_model(home)
        Clock.schedule_interval(self.highlight_player_square, 1/20.)

    def assign_roll_button_model(self, button_model):
        self.roll_button_model = button_model
    
    def highlight_player_square(self, dt):
        self.current_player.highlight_player_square()

    def change_player(self):
        prev_player = self.current_player
        self.current_player = self.Players[(self.Players.index(self.current_player) + 1) % len(self.Players)]
        prev_player.set_player_square_full_opacity()
    
    def process_dice_roll(self, roll_value):
        self.current_roll = roll_value
        if self.current_player.process_dice_roll(roll_value):
            self.roll_button_model.disabled = True
            if len(self.current_player.get_eligible_pins(roll_value)) == 1:
                self.process_pin_click(self.current_player.get_eligible_pins(roll_value)[0].PinModel)
        else:
            self.change_player()

    def process_pin_click(self, clicked_pin_model):
        moved_pin = self.current_player.move_pin(clicked_pin_model, self.current_roll)
        self.update_game(moved_pin)
        
    def move_pin_action(self, moved_pin):
        if not moved_pin.can_enter_home_stretch():
            path_unit_to_move_into = self.WhitePaths[moved_pin.get_current_path_index() % len(self.WhitePaths)]
            moved_pin.move_pin_visual_to_square(path_unit_to_move_into.PathSquareModel.center)
            enemy_pins_in_same_square = path_unit_to_move_into.add_pin(moved_pin)
            
            if enemy_pins_in_same_square and path_unit_to_move_into.is_not_safe():
                return True

    def update_game(self, moved_pin):
        cut_operated = self.move_pin_action(moved_pin)
        if not(self.current_roll == 6 or cut_operated or moved_pin.pin_in_podium()):
            self.change_player()
        self.roll_button_model.disabled = False