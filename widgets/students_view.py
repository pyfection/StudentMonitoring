
from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from api import api
from widgets.detail_list import DetailList


class StudentsView(MDBoxLayout):
    def __init__(self, **kwargs):
        Builder.load_file('widgets/students_view.kv')
        super().__init__(**kwargs)
        self.detail_list = DetailList(
            headers=[
                "ID", "Name of student", "Gender of student", 'Date of joining', "gr #", "Father's name",
                "Mother's name", "Address", "Phone number (Mother)", "Phone number (Father)", "Date of birth",
                "Aadhar Card number", "Official Class", "Goes to goverment school", "Mother' main occupation",
                "Father' main occupation", "Status", "Comment"
            ]
        )
        Clock.schedule_once(lambda dt: self.add_widget(self.detail_list))

    def add_child(self):
        App.get_running_app().manager.current = 'add_child'

    def reload(self):
        students = api.students()

        self.detail_list.data = [
            (
                (student['id'], student['student_name']),
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
                    student["comment"],
                )
            ) for student in students
        ]
