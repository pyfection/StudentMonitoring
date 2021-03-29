
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.picker import MDDatePicker


Builder.load_file('widgets/date_picker_button.kv')


class DatePickerButton(MDRoundFlatIconButton):
    date = StringProperty()
    format = StringProperty('%d-%m-%Y')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.date = value.strftime("%Y-%m-%d")
