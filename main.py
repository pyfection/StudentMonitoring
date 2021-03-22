from pprint import pprint
import re
from datetime import datetime, timedelta
import json

from kivymd.app import MDApp as App
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.accordion import AccordionItem
from kivy.core.window import Window
from kivymd.uix.list import MDList
import gspread_mock as gspread
from google.oauth2.service_account import Credentials

import settings
from widgets.student_overview import StudentOverview


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
            "Comment"
        )

    def new_sheet(self):
        sh = self.gc.create()
        # print(sh.sheet1.get('A1'))

    def load_sheet(self, link):
        self.sh = self.gc.open_by_url(link)
        print('open url')
        self.load_students()

    def load_students(self):
        ws = self.sh.worksheet("Holidays")
        holidays = ws.get(f'A2:R{ws.row_count-1}')
        ws = self.sh.worksheet("Students")
        students = ws.get(f'A2:R{ws.row_count-1}')
        ws = self.sh.worksheet("Attendance")
        attendance = ws.get(f'A2:R{ws.row_count-1}')
        ws = self.sh.worksheet("Fees")
        fees = ws.get(f'A2:R{ws.row_count-1}')
        ws = self.sh.worksheet("Grades")
        grades = ws.get(f'A2:R{ws.row_count-1}')
        ws = self.sh.worksheet("RangePlans")
        range_plans = ws.get(f'A2:R{ws.row_count-1}')
        ws = self.sh.worksheet("MonthPlans")
        month_plans = ws.get(f'A2:R{ws.row_count-1}')

        # Adding students to attendance sheet
        today = datetime.today()
        today_ = today.strftime('%Y-%m-%d')
        yesterday = (today - timedelta(days=1)).strftime(settings.date_format)
        for student in students:
            try:
                state = next(att[2] for att in attendance if att[0] == student[0] and att[1] == today_)
            except StopIteration:
                state = ''
            bx = BoxLayout()
            name = Label(text=student[1])
            present = ToggleButton(text='present', group=f'attended_{student[0]}', state='down' if state == 'present' else 'normal')
            absent = ToggleButton(text='absent', group=f'attended_{student[0]}', state='down' if state == 'absent' else 'normal')
            late = ToggleButton(text='late', group=f'attended_{student[0]}', state='down' if state == 'late' else 'normal')
            bx.add_widget(name)
            bx.add_widget(present)
            bx.add_widget(absent)
            bx.add_widget(late)

            self.attendance_list.add_widget(bx)

            has_yesterday = any(att[2] for att in attendance if att[0] == student[0] and att[1] == yesterday)
            if not has_yesterday:
                bx = BoxLayout()
                name = Label(text=student[1])
                present = ToggleButton(text='present', group=f'attended_{student[0]}')
                absent = ToggleButton(text='absent', group=f'attended_{student[0]}')
                late = ToggleButton(text='late', group=f'attended_{student[0]}')
                bx.add_widget(name)
                bx.add_widget(present)
                bx.add_widget(absent)
                bx.add_widget(late)

                self.attendance_list_yesterday.add_widget(bx)

        # Adding students to students list
        for student in students:
            std = AccordionItem(title=student[1])
            bx = BoxLayout(orientation='vertical', size_hint_y=None)
            std.add_widget(bx)
            for i, header in enumerate(self.headers, 1):
                key_value = BoxLayout(size_hint_y=None, height=80)
                key = Label(text=header)
                value = Label(text=str(student[i]))
                key_value.add_widget(key)
                key_value.add_widget(value)
                bx.add_widget(key_value)
            bx.height = sum(c.height for c in bx.children)

            self.student_list.add_widget(std)
        min_space = len(self.student_list.children) * self.student_list.min_space
        self.student_list.height = min_space + 1200

        # Adding grades
        today = datetime.today()
        for student in students:
            bx = BoxLayout()
            name = Label(text=student[1])
            date = TextInput(hint_text="Date (YYYY-MM-DD)")
            math = TextInput(hint_text="Math")
            english = TextInput(hint_text="English")
            hindi = TextInput(hint_text="Hindi")
            for grade in grades:
                if grade[0] != student[0]:
                    continue
                dt = datetime.fromisoformat(grade[1])
                if dt.year != today.year or dt.month != today.month:
                    continue
                date.text = grade[1]
                math.text = grade[2]
                english.text = grade[3]
                hindi.text = grade[4]
                break
            bx.add_widget(name)
            bx.add_widget(date)
            bx.add_widget(math)
            bx.add_widget(english)
            bx.add_widget(hindi)

            self.grades_list.add_widget(bx)

        # Adding fees
        today = datetime.today()
        for student in students:
            bx = BoxLayout()
            name = Label(text=student[1])
            date = TextInput(hint_text="Date (YYYY-MM-DD)")
            amount = TextInput(hint_text="Amount")
            receipt = TextInput(hint_text="Receipt")
            books = TextInput(hint_text="Books Payment")
            for fee in fees:
                if fee[0] != student[0]:
                    continue
                dt = datetime.fromisoformat(fee[1])
                if dt.year != today.year or dt.month != today.month:
                    continue
                date.text = fee[1]
                amount.text = fee[2]
                receipt.text = fee[3]
                books.text = fee[4]
                break
            bx.add_widget(name)
            bx.add_widget(date)
            bx.add_widget(amount)
            bx.add_widget(receipt)
            bx.add_widget(books)

            self.fees_list.add_widget(bx)

        # Adding plan
        self.plan_list.subjects = ["Math", "English", "Hindi", "Arts"]
        self.plan_list.data = {
            'months': {
                '2021-03': {
                    "Math": "Test data math",
                    "Arts": "Test data arts",
                },
                '2021-04': {
                    "English": "Test data english",
                    "Arts": "Test data arts",
                },
            },
            'ranges': {
                ('2021-03-01', '2021-03-05'): {
                    "Math": "Exact math subject"
                }
            }
        }

        # Adding overview
        students = {s[0]: s[1:] for s in students}
        info = {}
        for fee in fees:
            dt = datetime.fromisoformat(fee[1])
            date = (dt.year, dt.month)
            st = students[fee[0]]
            fee_data = {
                'id': fee[0], 'name': st[0], 'date': fee[1], 'amount': fee[2], 'receipt': fee[2], 'books': fee[1]
            }
            try:
                students_ = info[date]
            except KeyError:
                info[date] = {fee[0]: fee_data}
            else:
                try:
                    student = students_[fee[0]]
                except KeyError:
                    students_[fee[0]] = fee_data
                else:
                    student.update(fee_data)

        for grade in grades:
            dt = datetime.fromisoformat(grade[1])
            date = (dt.year, dt.month)
            st = students[grade[0]]
            grade_data = {'id': grade[0], 'name': st[0], 'math': grade[2], 'english': grade[3], 'hindi': grade[4]}
            try:
                students_ = info[date]
            except KeyError:
                info[date] = {grade[0]: grade_data}
            else:
                try:
                    student = students_[grade[0]]
                except KeyError:
                    students_[grade[0]] = grade_data
                else:
                    student.update(grade_data)

        for att in attendance:
            dt = datetime.fromisoformat(att[1])
            date = (dt.year, dt.month)
            st = students[att[0]]
            att_data = {'id': att[0], 'name': st[0], str(dt.day): att[2]}
            try:
                students_ = info[date]
            except KeyError:
                info[date] = {att[0]: att_data}
            else:
                try:
                    student = students_[att[0]]
                except KeyError:
                    students_[att[0]] = att_data
                else:
                    student.update(att_data)

        for date, students_ in sorted(info.items()):
            tab = StudentOverview(students_, date[0], date[1], holidays)
            self.student_overview.add_widget(tab)

    def add_child(self, data):
        ws = self.sh.worksheet("Students")
        i = ws.row_count
        ws.append_row([str(i)] + data)
        self.attendance_list.clear_widgets()
        self.student_list.clear_widgets()
        self.fees_list.clear_widgets()
        self.student_overview.clear_widgets()
        self.load_students()


class NewChildView(MDList):
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
            str(int(self.goes_government_school_yes.state == "down")),
            self.occupation_mother.text,
            self.occupation_father.text,
            self.comment.text,
        ]
        app = App.get_running_app()
        app.root.current = 'teacher'
        app.root.ids.teacher_view.add_child(data)


class MonitoringApp(App):
    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "Brown"
        self.theme_cls.theme_style = "Dark"


Factory.register('TeacherView', module='main')
Factory.register('AuthView', module='main')
Factory.register('PlanView', module='widgets.plan_view')


if __name__ == '__main__':
    app = MonitoringApp()
    app.run()
