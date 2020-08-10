from .Player import Player
from .PathUnit import PathUnit

class LudoGame():
    def __init__(self):
        # Player Starting Indexes are
        starting_indexes = [1, 14, 27, 40]
        self.safe_zones = starting_indexes + [9, 22, 35, 48]
        self.Player1 = Player(starting_indexes[0])
        self.Player2 = Player(starting_indexes[1])
        self.Player3 = Player(starting_indexes[2])
        self.Player4 = Player(starting_indexes[3])
        self.Players = [self.Player1, self.Player2, \
                        self.Player3, self.Player4]
        self.current_player = self.Player1
        self.current_roll = -1
        self.WhitePaths = []

    def set_white_game_paths(self, white_path_array):
        for path in white_path_array:
            self.WhitePaths.append(PathUnit(path))
        
        for index in self.safe_zones:
            self.WhitePaths[index].safe_zone = True        

    def assign_base_to_player(self, player_home_list):
        for player, home in zip(self.Players, player_home_list):
            player.set_base_model(home)

    def change_player(self):
        self.current_player =  self.Players[(self.Players.index(self.current_player) + 1) % len(self.Players)]
    
    def process_dice_roll(self, roll_value):
        self.current_roll = roll_value
        return self.current_player.process_dice_roll(roll_value)

    def move_player_pin(self, roll_value):
        self.current_player.move_pin(roll_value)