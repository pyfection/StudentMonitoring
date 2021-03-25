from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel


Builder.load_string('''
<AdvancedLabel>:
    size_hint: 1, 1
    bg_color: 1, 1, 1, 0
    halign: 'center'
    canvas.before:
        Color:
            rgba: root.bg_color
        Rectangle:
            size: self.size
            pos: self.pos
''')


class AdvancedLabel(MDLabel):
    def __init__(self, bg_color=None, **kwargs):
        super().__init__(**kwargs)
        if bg_color:
            self.bg_color = bg_color
