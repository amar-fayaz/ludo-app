from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.spinner import MDSpinner

class JoinGameForm(MDBoxLayout):
    username_form = ObjectProperty(None)
    host_ip_form = ObjectProperty(None)
    loading_spinner = ObjectProperty(None)

    def store_user_data(self, user_data_object): 
        if self.validate_inputs():
            user_data_object.set_username(self.username_form.text)
            user_data_object.set_host_ip(self.host_ip_form.text)      
            return True
        return False

    def validate_inputs(self):
        print("Fired")
        self.loading_spinner.active = True
        return True  

    