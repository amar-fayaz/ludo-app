from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField

import time

from ..join_game import JoinGameForm

class HomeScreen(Screen):
    exit_confirmation = None
    join_confirmation = None
    join_form = None

    # ----------------- Exit Confirmation Related Stuff ---------------

    def create_exit_confirmation_dialog(self):
        exit_button = MDRaisedButton(
            text="Quit", 
            on_release=App.get_running_app().stop)
        dismiss_button = MDFlatButton(
            text="Cancel", 
            on_release=self.dismiss_exit_confirmation)
        self.exit_confirmation = MDDialog(
            title="Quit?", 
            text="Are you sure you want to quit?",
            buttons=[dismiss_button, exit_button],
            size_hint=[0.7, 1])

    def show_exit_confirmation(self):
        if not self.exit_confirmation:
            self.create_exit_confirmation_dialog()
        self.exit_confirmation.open()

    def dismiss_exit_confirmation(self, *args):
        self.exit_confirmation.dismiss()   

    # ------------------ Joining Info Related Stuff ---------------------

    def create_join_dialog(self):
        self.join_form = JoinGameForm()
        join_button = MDRaisedButton(
            text="Join", 
            on_release=self.change_screen)
        dismiss_button = MDFlatButton(
            text="Cancel", 
            on_release=self.dismiss_join_confirmation)
        self.join_confirmation = MDDialog(
            title="Connect",
            type="custom",
            content_cls=self.join_form,
            buttons=[dismiss_button, join_button],
            size_hint=[0.7, 1])
    
    def show_join_confirmation(self):
        if not self.join_confirmation:
            self.create_join_dialog()
        self.join_confirmation.open()

    def dismiss_join_confirmation(self, *args):
        self.join_confirmation.dismiss()   


    # ------------------- Page Change Logic -----------------------------

    def change_screen(self, *args):
        if self.join_form.store_user_data(self.manager.user_data):
            print ("loading_screen")

    # ------------------- Handle Key Presses -----------------------------
    def handle_key_downs(self, window, key, *args):
        if key == 27:
            self.show_exit_confirmation()         