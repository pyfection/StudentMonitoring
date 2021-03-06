from pprint import pprint
import re
from datetime import datetime
import json

from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.accordion import AccordionItem
import gspread_mock as gspread
from google.oauth2.service_account import Credentials
from kivy.config import Config
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')


class AuthView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            with open('session.json') as f:
                self.session = json.load(f)
        except FileNotFoundError:
            self.session = {}

    def check_authenticate(self):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_file(
            'teacher_credentials.json',
            scopes=scopes
        )
        gc = gspread.authorize(credentials)
        print('authorize')
        # ToDo: add check if actually authorized
        # ToDo: check if part of secret key is same part of teacher secret key in config
        app = App.get_running_app()
        app.root.current = 'teacher'
        app.root.ids.teacher_view.gc = gc
        app.root.ids.teacher_view.load_sheet('link to center sheet')


class TeacherView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.student_list.bind(minimum_height=self.student_list.setter('height'))
        self.sh = None
        self.student_master = {}
        self.headers = (
            "Name of student",
            'Date of joining',
            "gr #",
            "Father's name",
            "Mother's name",
            "Address",
            "Phone number (Mother)",
            "Phone number (Father)",
            "Date of birth",
            "Aadhar Card number",
            "Official Class",
            "Goes to goverment school",
            "Mother' main occupation",
            "Father' main occupation",
            "baseline Math",
            "Baseline English",
            "Baseline Hindi",
            "Comment"
        )

    def new_sheet(self):
        sh = self.gc.create()
        # print(sh.sheet1.get('A1'))

    def load_sheet(self, link):
        self.sh = self.gc.open_by_url(link)
        print('open url')
        self.load_students()

    def load_student_master(self):
        ws = self.sh.worksheet("Student master")
        print('get worksheet')
        records = ws.get_all_records(head=2)
        for student in records:
            student = {key.strip(): value for key, value in student.items()}
            std = AccordionItem(title=student["Name of student"])
            bx = BoxLayout(orientation='vertical')
            std.add_widget(bx)
            for header in self.headers:
                key_value = BoxLayout(size_hint_y=None, height=20)
                key = Label(text=header)
                value = Label(text=str(student[header]))
                key_value.add_widget(key)
                key_value.add_widget(value)
                bx.add_widget(key_value)

            self.student_list.add_widget(std)

    def load_students(self):
        ws = self.sh.worksheet("Students")
        records = ws.get(f'A2:R{ws.row_count-1}')

        # Adding students to attendance sheet
        for student in records:
            bx = BoxLayout()
            name = Label(text=student[1])
            attended = ToggleButton(text='attended', group=f'attended_{student[0]}')
            missed = ToggleButton(text='missed', group=f'attended_{student[0]}')
            late = ToggleButton(text='late', group=f'attended_{student[0]}')
            bx.add_widget(name)
            bx.add_widget(attended)
            bx.add_widget(missed)
            bx.add_widget(late)

            self.attendance_list.add_widget(bx)

        # Adding students to students list
        for student in records:
            std = AccordionItem(title=student[1])
            bx = BoxLayout(orientation='vertical')
            std.add_widget(bx)
            for i, header in enumerate(self.headers, 1):
                key_value = BoxLayout(size_hint_y=None, height=20)
                key = Label(text=header)
                value = Label(text=str(student[i]))
                key_value.add_widget(key)
                key_value.add_widget(value)
                bx.add_widget(key_value)

            self.student_list.add_widget(std)

    def add_child(self, data):
        ws = self.sh.worksheet("Students")
        ws.append_row(data)


class NewChildView(BoxLayout):
    # @staticmethod
    # def correct_date_format(inst):
    #     for i in (4, 7, 10):
    #         try:
    #             if inst.text[i] != '-':
    #                 inst.text = inst.text[:i] + '-' + inst.text[i:]
    #                 inst.cursor = inst.get_cursor_from_index(inst.cursor_index() + 1)
    #         except IndexError:
    #             break

    @staticmethod
    def check_date_format(text):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', text):
            return False
        year, month, day = map(int, text.split('-'))
        today = datetime.today()
        if not (1950 < year < today.year and 1 <= month <= 12 and 1 <= day <= 31):
            return False
        try:
            datetime(year, month, day)
        except ValueError:
            return False
        return True

    def submit(self):
        # ToDo: add validation checks
        data = [
            self.name.text,
            self.date_of_joining.text,
            self.group.text,
            self.name_father.text,
            self.name_mother.text,
            self.address.text,
            self.phone_mother.text,
            self.phone_father.text,
            self.dob.text,
            self.aadhar.text,
            self.official_class.text,
            self.goes_government_school_yes.state == "down",
            self.occupation_mother.text,
            self.occupation_father.text,
            self.baseline_math.text,
            self.baseline_english.text,
            self.baseline_hindi.text,
            self.comment.text,
        ]
        app = App.get_running_app()
        app.root.current = 'teacher'
        app.root.ids.teacher_view.add_child(data)


class MonitoringApp(App):
    pass


Factory.register('TeacherView', module='main')
Factory.register('AuthView', module='main')


if __name__ == '__main__':
    app = MonitoringApp()
    app.run()
