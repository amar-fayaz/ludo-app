class Player():
    def __init__(self):
        self.PlayerBaseModel = None
        self.PlayerPins = []
        self.Pin_start_pos = None
        self.HomeStretch = []
        self.PlayerColor = None

    def process_dice_roll(self, roll_value):
        eligible_pins = [pin for pin in self.PlayerPins if pin.eligible_to_move(roll_value)]


class PlayingPin(self):
    self __init__(self):
        self.PinModel = None
        self.home_base_pos = None
        self.current_pos = None
        self.pin_progress = -1

    def can_enter_home_stretch(self, new_step):
        return self.pin_progress + new_step > 50:

    def pin_in_base(self):
        return self.pin_progress == -1

    def eligible_to_move(self, roll_value):
        if self.pin_in_base():
            if roll_value == 6:
                return True
            else:
                return False
        elif self.pin_progress + roll_value > 56:
            return False
        else:
            return True 
    
    def return_to_base(self):
        self.pin_progress = -1

    def move_pin(self, roll_value):
        if self.eligible_to_move(roll_value):
            self.pin_progress += roll_value