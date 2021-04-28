import datetime

from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.textfield import MDTextField


class DateInput(MDTextField):
    format = StringProperty('%d/%m/%Y')
    format_hint = StringProperty('dd/mm/yyyy')
    date = ObjectProperty()

    def __init__(self, **kwargs):
        self.helper_text_mode = "on_error"
        self.helper_text = f"Needs to be of format {self.format_hint}"
        super().__init__(**kwargs)

    def on_date(self, *args):
        self.text = self.date.strftime(self.format)

    def on_format_hint(self, *args):
        self.helper_text = f"Needs to be of format {self.format_hint}"

    def on_text(self, *args):
        if not self.text:
            self.error = False
            return
        try:
            date = datetime.datetime.strptime(self.text, self.format)
        except ValueError:
            self.error = True
        else:
            self.error = False
            self.date = date
