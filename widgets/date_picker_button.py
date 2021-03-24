
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.picker import MDDatePicker


class DatePickerButton(MDRoundFlatIconButton):
    format = StringProperty('%d-%m-%Y')

    def __init__(self, **kwargs):
        Builder.load_file('widgets/date_picker_button.kv')
        super().__init__(**kwargs)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.text = value.strftime(self.format)
