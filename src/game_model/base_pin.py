from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRoundImageButton
from kivy.properties import StringProperty
from kivymd.app import MDApp

class BasePin(MDRoundImageButton):
    color = StringProperty("white")
    pin_type = StringProperty("base")

    def remove_widget_from_parent(self):
        self.parent.remove_widget(self)
    
    def create_playing_pin(self, size, center_pos):
        pin_model = BasePin(color=self.color, center=center_pos, pin_type="playing")#, size=(size,size))
        MDApp.get_running_app().game.GameBoard.add_widget(pin_model)
        return pin_model