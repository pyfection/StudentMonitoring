import datetime

from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.picker import MDDatePicker


Builder.load_file('widgets/date_picker_button.kv')


class DatePickerButton(MDRoundFlatIconButton):
    date = StringProperty()
    format = StringProperty('%d-%m-%Y')
    date_dialog = MDDatePicker()
    min_year = NumericProperty(1914)
    max_year = (datetime.date.today() + datetime.timedelta(days=365)).year

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.width = 400
        self.date_dialog.bind(on_save=self.on_save)

    def show_date_picker(self):
        self.date_dialog.min_year = self.min_year
        self.date_dialog.max_year = self.max_year
        self.date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.date = value.strftime("%Y-%m-%d")
