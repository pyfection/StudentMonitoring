
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout

from api import api
from widgets.detail_list import DetailList


class StudentsView(BoxLayout):
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

    def new_student(self):
        App.get_running_app().manager.current = 'student_detail'

    def show_detail(self, uid):
        app = App.get_running_app()
        app.manager.current = 'student_detail'
        self.student_detail_view.reload(uid)

    def reload(self):
        students = api.students()

        self.ids.list.data = [
            {
                'text': student['student_name'],
                'size_hint': (1, None),
                'height': dp(50),
                'on_press': lambda uid=student['id']: self.show_detail(uid)
            } for student in students
        ]
