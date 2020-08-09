from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRoundImageButton
from kivy.properties import StringProperty

class BasePin(MDRoundImageButton):
    color = StringProperty("white")