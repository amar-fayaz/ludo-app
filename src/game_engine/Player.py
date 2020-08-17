from ..data.config import PLAYER_PIN_DIMENSION, PLAYER_OPACITY_DELTA
from .PathUnit import PathUnit
from kivy.clock import Clock
from operator import add

class Player():
    def __init__(self, starting_index):
        self.PlayerBaseModel = None
        self.Pin1 = PlayingPin(starting_index)
        self.Pin2 = PlayingPin(starting_index)
        self.Pin3 = PlayingPin(starting_index)
        self.Pin4 = PlayingPin(starting_index)
        self.PlayerPins = [self.Pin1, self.Pin2, self.Pin3, self.Pin4]
        self.Pin_start_pos = starting_index
        self.HomeStretch = []
        self.PlayerColor = None
        self.PodiumTransform = None

        self._opacity_delta = - PLAYER_OPACITY_DELTA

    def process_dice_roll(self, roll_value):
        eligible_pins = self.get_eligible_pins(roll_value)
        if eligible_pins:
            for pin in eligible_pins:
                pin.enable_pin()
            return True
        else:
            return False

    def get_eligible_pins(self, roll_value):
        return [pin for pin in self.PlayerPins if pin.eligible_to_move(roll_value)]

    def set_base_model(self, base_model_list):
        self.PlayerBaseModel = base_model_list[0]
        for pin_model, pin in zip(self.PlayerBaseModel.pins, self.PlayerPins):
            pin.set_pin_model(pin_model)
        self.PlayerColor = self.PlayerBaseModel.color
        self.set_home_stretch(base_model_list[1])
    
    def set_home_stretch(self, home_strech_model):
        for square in home_strech_model:
            self.HomeStretch.append(PathUnit(square))
        
    def set_podium_transform(self, podium_transform):
        self.PodiumTransform = podium_transform
        for pin in self.PlayerPins:
            pin.set_podium_transform(podium_transform)

    def move_pin(self, pin_model, roll_value):
        for pin in self.PlayerPins:
            pin.disable_pin()
        activated_pin = next(pin for pin in self.PlayerPins if pin.PinModel == pin_model)
        if activated_pin == None:
            raise ValueError("Cannot find the corresponding Pin object")
        activated_pin.move_pin(roll_value)
        return activated_pin

    def highlight_player_square(self):
        self.PlayerBaseModel.outer_square.fill_color[3] += self._opacity_delta
        if self.PlayerBaseModel.outer_square.fill_color[3] <= 0.6 or self.PlayerBaseModel.outer_square.fill_color[3] >= 1.0:
            self._opacity_delta = - self._opacity_delta

    def set_player_square_full_opacity(self):
        self.PlayerBaseModel.outer_square.fill_color[3] = 1.0
        self._opacity_delta = - PLAYER_OPACITY_DELTA


class PlayingPin():
    def __init__(self, pin_start_index):
        self.PinModel = None
        self.home_base_pos = None
        self.current_pos = None
        self.pin_progress = -1
        self.color = None
        self.start_index = pin_start_index
        self.pin_parent_model = None
        self.home_pin_model = None
        self.road_pin_model = None
        self.podium_transform = None

        self._opacity_delta = - PLAYER_OPACITY_DELTA

    def get_path_index(self, roll_value):
        if self.pin_progress == -1 and roll_value == 6:
            return self.start_index
        if self.pin_progress >= 0 and self.pin_progress + self.roll_value <= 50:
            return (self.pin_progress + self.start_index) % 52

    def get_current_path_index(self):
        return self.pin_progress + self.start_index

    def set_pin_model(self, pin_model):
        if self.PinModel == None:
            self.PinModel = pin_model
            self.pin_parent_model = pin_model.parent
            self.home_pin_model = pin_model
            self.color = pin_model.color
        else:
            raise ValueError("Pin Model already set.")

    def set_podium_transform(self, podium_transform):
        self.podium_transform = podium_transform

    def can_enter_home_stretch(self):
        return self.pin_progress > 50

    def pin_in_base(self):
        return self.pin_progress == -1

    def pin_reached_podium(self):
        return self.pin_progress == 56

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

    def disable_pin(self):
        self.PinModel.disabled = True
        Clock.unschedule(self.highlight_pin)
        self.reset_opacity()

    def enable_pin(self):
        self.PinModel.disabled = False
        Clock.schedule_interval(self.highlight_pin, 1/20.)
        
    def highlight_pin(self, dt):
        self.PinModel.opacity += self._opacity_delta
        if self.PinModel.opacity <= 0.6 or self.PinModel.opacity >= 1.0:
            self._opacity_delta = - self._opacity_delta

    def reset_opacity(self):
        self.PinModel.opacity = 1.0
        self._opacity_delta = - PLAYER_OPACITY_DELTA

    def switch_pin_model_to_playing(self):
        self.road_pin_model = self.PinModel.create_playing_pin(PLAYER_PIN_DIMENSION, self.PinModel.center)
        self.PinModel.hide_widget()
        self.PinModel = self.road_pin_model

    def switch_pin_model_to_base(self):
        self.home_pin_model.show_widget()
        self.PinModel.remove_widget_from_parent()
        self.PinModel = self.home_pin_model

    def return_to_base_operation(self):
        self.return_to_base()
        self.switch_pin_model_to_base()

    def get_podium_location(self, podium_center):
        return tuple(map(add, podium_center, self.podium_transform))

    def move_pin(self, roll_value):
        if self.eligible_to_move(roll_value):
            if self.pin_in_base() and roll_value == 6:
                self.switch_pin_model_to_playing()
                self.pin_progress = 0
            else:
                self.pin_progress += roll_value

    def move_pin_visual_to_square(self, square_model_coordinate):
        self.PinModel.center = square_model_coordinate