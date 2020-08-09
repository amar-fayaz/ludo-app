
class LudoGame():
    def __init__(self):
        self.Player1 = None
        self.Player2 = None
        self.Player3 = None
        self.Player4 = None
        self.Players = [self.Player1, self.Player2, \
                        self.Player3, self.Player4]
        self.current_player = Player1
        self.WhitePaths = []

    def change_player(self):
        self.current_player =  self.Players[(self.Players.index(self.current_player) + 1) % len(self.Players)]

    
    def process_dice_roll(self, roll_value):
        self.current_player.process_dice_roll(roll_value)

    def move_player_pin(self, roll_value):
        self.current_player.move_pin(roll_value)