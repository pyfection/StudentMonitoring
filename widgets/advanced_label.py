from kivy.uix.label import Label
from kivy.lang.builder import Builder


Builder.load_string('''
<AdvancedLabel>:
    size_hint: 1, 1
    bg_color: 1, 1, 1, 0
    canvas.before:
        Color:
            rgba: root.bg_color
        Rectangle:
            size: self.size
            pos: self.pos
''')


class AdvancedLabel(Label):
    def __init__(self, bg_color=None, **kwargs):
        super().__init__(**kwargs)
        if bg_color:
            self.bg_color = bg_color
