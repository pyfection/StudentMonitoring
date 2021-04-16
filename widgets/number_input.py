
from kivy.properties import NumericProperty
from kivymd.uix.textfield import MDTextField


class NumberInput(MDTextField):
    min_text_length = NumericProperty(0)

    def __init__(self, **kwargs):
        self.helper_text_mode = "on_error"
        self.helper_text = f"Needs to be between {self.min_text_length} and {self.max_text_length} numbers long"
        super().__init__(**kwargs)

    def on_min_text_length(self, *args):
        self.helper_text = f"Needs to be between {self.min_text_length} and {self.max_text_length} numbers long"

    def on_max_text_length(self, *args):
        self.helper_text = f"Needs to be between {self.min_text_length} and {self.max_text_length} numbers long"

    def on_text(self, *args):
        if self.min_text_length > len(self.text):
            self.error = True
        elif self.max_text_length and len(self.text) > self.max_text_length:
            self.error = True
        else:
            self.error = False
