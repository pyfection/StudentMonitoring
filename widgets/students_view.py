
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from api import api


class StudentContent(MDBoxLayout):
    student_name = StringProperty()
    student_gender = StringProperty()
    joining_date = StringProperty()
    group = StringProperty()
    name_father = StringProperty()
    name_mother = StringProperty()
    address = StringProperty()
    phone_number_mother = StringProperty()
    phone_number_father = StringProperty()
    dob = StringProperty()
    aadhar_card_number = StringProperty()
    official_class = StringProperty()
    goes_goverment_school = StringProperty()
    occupation_mother = StringProperty()
    occupation_father = StringProperty()
    status = StringProperty()
    teacher = StringProperty()
    comment = StringProperty()


class StudentsView(MDBoxLayout):
    def __init__(self, **kwargs):
        Builder.load_file('widgets/students_view.kv')
        super().__init__(**kwargs)

    def reload(self):
        self.student_list.clear_widgets()

        students = api.students()

        for student in students:
            cnt = StudentContent()
            std = MDExpansionPanel(
                icon='human-child',
                content=cnt,
                panel_cls=MDExpansionPanelOneLine(
                    text=student['student_name']
                )
            )
            for key, value in student.items():
                if key == 'id':
                    continue
                setattr(cnt, key, value)

            self.student_list.add_widget(std)
