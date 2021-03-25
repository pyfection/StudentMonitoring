from datetime import datetime

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from api import api
from widgets.date_picker_button import DatePickerButton


class GradesView(MDBoxLayout):
    def __init__(self, **kwargs):
        Builder.load_file('widgets/grades_view.kv')
        super().__init__(**kwargs)

    def reload(self):
        self.grades_list.clear_widgets()

        students = api.students()
        grades = api.grades()

        today = datetime.today()
        for student in students:
            if student['status'] == 'inactive':
                continue
            bx = MDBoxLayout(padding=(10, 10, 10, 10), spacing=10, adaptive_height=True)
            name = MDLabel(text=student['student_name'])
            date = DatePickerButton(format='%b-%Y')
            gtype = MDTextField(hint_text="Type")
            math = MDTextField(hint_text="Math")
            english = MDTextField(hint_text="English")
            hindi = MDTextField(hint_text="Hindi")
            for grade in grades:
                if grade['student_id'] != student['id']:
                    continue
                dt = datetime(*map(int, grade['date'].split('-')), 1)
                if dt.year != today.year or dt.month != today.month:
                    continue
                date.text = dt.strftime('%b-%Y')
                gtype.text = grade['gtype']
                math.text = grade['math']
                english.text = grade['english']
                hindi.text = grade['hindi']
                break
            bx.add_widget(name)
            bx.add_widget(date)
            bx.add_widget(gtype)
            bx.add_widget(math)
            bx.add_widget(english)
            bx.add_widget(hindi)

            self.grades_list.add_widget(bx)
