
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRaisedButton


class MDFillRoundToggleButton(MDRaisedButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.background_down = (1, 1, 1, 0)
        # self.background_normal = (1, 1, 1, 0)

    def update_md_bg_color(self, instance, value):
        pass

    def on_md_bg_color(self, instance, value):
        pass

    def set_md_bg_color(self, interval):
        pass
