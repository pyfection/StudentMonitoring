
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from api import api
from widgets.data_table import DataTable


class StudentsView(MDBoxLayout):
    def __init__(self, **kwargs):
        Builder.load_file('widgets/students_view.kv')
        super().__init__(**kwargs)
        self.data_table = DataTable(
            # size_hint=(0.8, 0.7),
            use_pagination=True,
            check=True,
            rows_num=5,
            sorted_on="Name of Student",
            sorted_order="ASC",
            elevation=2,
            column_data=[
                ("ID", dp(60), self.sort_on_id),
                ("Name of student", dp(30), self.sort_on_student_name),
                ("Gender of student", dp(30)),
                ('Date of joining', dp(30)),
                ("gr #", dp(30)),
                ("Father's name", dp(30)),
                ("Mother's name", dp(30)),
                ("Address", dp(30)),
                ("Phone number (Mother)", dp(30)),
                ("Phone number (Father)", dp(30)),
                ("Date of birth", dp(30)),
                ("Aadhar Card number", dp(30)),
                ("Official Class", dp(30)),
                ("Goes to goverment school", dp(30)),
                ("Mother' main occupation", dp(30)),
                ("Father' main occupation", dp(30)),
                ("Status", dp(30)),
                ("Teacher", dp(30)),
                ("Comment", dp(30)),
            ],
        )
        Clock.schedule_once(lambda dt: self.add_widget(self.data_table))

    def add_child(self):
        App.get_running_app().manager.current = 'add_child'

    def reload(self):
        students = api.students()

        self.data_table.row_data = [
            (
                student["id"],
                student["student_name"],
                student["student_gender"],
                student['joining_date'],
                student["group"],
                student["name_father"],
                student["name_mother"],
                student["address"],
                student["phone_number_mother"],
                student["phone_number_father"],
                student["dob"],
                student["aadhar_card_number"],
                student["official_class"],
                student["goes_goverment_school"],
                student["occupation_mother"],
                student["occupation_father"],
                student["status"],
                student["teacher"],
                student["comment"],
            ) for student in students
        ]

    def sort_on_id(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][0]
            )
        )

    def sort_on_student_name(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][1]
            )
        )
