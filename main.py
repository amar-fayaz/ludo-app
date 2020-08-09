from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics','resizable', 0)
# Config.set('graphics', 'width', '600')
# Config.set('graphics', 'height', '1200')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty

from user_data import UserData


class LudoScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(LudoScreenManager, self).__init__(**kwargs)
        self.user_data = UserData()
        Window.bind(on_keyboard=self.current_screen.handle_key_downs)


class LudoApp(MDApp):
    game = ObjectProperty(None)

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.theme_style = "Dark"
        return LudoScreenManager()

if __name__ == "__main__":
    LudoApp().run()