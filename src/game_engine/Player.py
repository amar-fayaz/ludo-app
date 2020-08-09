class Player():
    def __init__(self, starting_index):
        self.PlayerBaseModel = None
        self.Pin1 = PlayingPin()
        self.Pin2 = PlayingPin()
        self.Pin3 = PlayingPin()
        self.Pin4 = PlayingPin()
        self.PlayerPins = [self.Pin1, self.Pin2, self.Pin3, self.Pin4]
        self.Pin_start_pos = None
        self.HomeStretch = []
        self.PlayerColor = None

    def process_dice_roll(self, roll_value):
        eligible_pins = [pin for pin in self.PlayerPins if pin.eligible_to_move(roll_value)]

    def set_base_model(self, base_model_list):
        self.PlayerBaseModel = base_model_list[0]
        for pin_model, pin in zip(self.PlayerBaseModel.pins, self.PlayerPins):
            pin.set_pin_model(pin_model)
        self.HomeStretch = base_model_list[1]
        self.PlayerColor = self.PlayerBaseModel.color


class PlayingPin():
    def __init__(self, pin_model=None):
        self.PinModel = pin_model
        self.home_base_pos = None
        self.current_pos = None
        self.pin_progress = -1

    def set_pin_model(self, pin_model):
        if self.PinModel == None:
            self.PinModel = pin_model
        else:
            raise ValueError("Pin Model already set.")

    def can_enter_home_stretch(self, new_step):
        return self.pin_progress + new_step > 50

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