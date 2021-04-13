from datetime import datetime

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu

from api import api


class GradesRow(MDBoxLayout):
    student_id = StringProperty()
    name = StringProperty()
    date = StringProperty()
    gtype = StringProperty()
    math = StringProperty()
    english = StringProperty()
    hindi = StringProperty()
    key_map = {"monthly": "Monthly", "mid_term": "Mid-Term", "final": "Final"}


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        menu_items = [
            {
                "text": "Monthly",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="monthly": self.menu_callback(self.key_map[x], x),
            },
            {
                "text": "Mid-Term",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="mid_term": self.menu_callback(self.key_map[x], x),
            },
            {
                "text": "Final",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="final": self.menu_callback(self.key_map[x], x),
            },
        ]
        self.gtype_menu = MDDropdownMenu(
            caller=self.ids.gtype,
            items=menu_items,
            width_mult=4,
        )

    def menu_callback(self, text, gtype):
        self.ids.gtype.text = text
        self.gtype = gtype
        self.gtype_menu.dismiss()


class GradesView(MDBoxLayout):
    def __init__(self, **kwargs):
        Builder.load_file('views/grades_view.kv')
        super().__init__(**kwargs)

    def reload(self):
        self.grades_list.clear_widgets()

        students = api.students()
        grades = api.grades()

        today = datetime.today()
        for student in students:
            if student['status'] == 'inactive':
                continue

            row = GradesRow()
            row.student_id = student['id']
            row.name = student['student_name']

            for grade in grades:
                if grade['student_id'] != student['id']:
                    continue
                dt = datetime(*map(int, grade['date'].split('-')), 1)
                if dt.year != today.year or dt.month != today.month:
                    continue
                row.date = dt.strftime('%Y-%m-%d')
                row.gtype = grade['gtype']
                row.ids.gtype.text = row.key_map.get(row.gtype, 'Grade Type')
                row.math = grade['math']
                row.english = grade['english']
                row.hindi = grade['hindi']
                break

            self.grades_list.add_widget(row)

    def save(self):
        data = []
        for row in self.grades_list.children:
            data.append({
                'student_id': row.student_id, 'date': row.date[:-3], 'gtype': row.gtype,
                'math': row.math, 'english': row.english, 'hindi': row.hindi
            })
        api.upsert_grades(data)
        api.sync_grades()
