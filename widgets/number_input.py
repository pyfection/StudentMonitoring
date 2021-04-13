
from kivymd.uix.textfield import MDTextField


class NumberInput(MDTextField):
    max_len = 10

    def insert_text(self, substring, from_undo=False):
        try:
            int(substring)
        except ValueError:
            return
        if len(self.text) >= self.max_len:
            return
        return super().insert_text(substring, from_undo=from_undo)
