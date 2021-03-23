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
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.picker import MDDatePicker

from api import api
import settings
from widgets.student_overview import StudentOverview


class DatePickerButton(MDRoundFlatIconButton):
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.text = value.strftime('%b-%Y')


class AuthView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            with open('session.json') as f:
                self.session = json.load(f)
        except FileNotFoundError:
            self.session = {}


class TeacherView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.student_list.bind(minimum_height=self.student_list.setter('height'))
        self.student_master = {}
        self.headers = {
            "student_name": "Name of student",
            'joining_date': 'Date of joining',
            "group": "gr #",
            "name_father": "Father's name",
            "name_mother": "Mother's name",
            "address": "Address",
            "phone_number_mother": "Phone number (Mother)",
            "phone_number_father": "Phone number (Father)",
            "dob": "Date of birth",
            "aadhar_card_number": "Aadhar Card number",
            "official_class": "Official Class",
            "goes_goverment_school": "Goes to goverment school",
            "occupation_mother": "Mother' main occupation",
            "occupation_father": "Father' main occupation",
            "status": "Status",
            "teacher": "Teacher",
            "comment": "Comment",
        }

    def load_students(self):
        holidays = api.holidays()
        students = api.students()
        attendance = api.attendance()
        fees = api.fees()
        grades = api.grades()

        # Adding students to attendance sheet
        today = datetime.today()
        today_ = today.strftime('%Y-%m-%d')
        yesterday = (today - timedelta(days=1)).strftime(settings.date_format)
        for student in students:
            if student['status'] == 'inactive':
                continue
            try:
                state = next(att['status'] for att in attendance if att['student_id'] == student['id'] and att['date'] == today_)
            except StopIteration:
                state = ''
            bx = BoxLayout()
            name = Label(text=student['student_name'])
            present = ToggleButton(text='present', group=f'attended_{student["id"]}', state='down' if state == 'present' else 'normal')
            absent = ToggleButton(text='absent', group=f'attended_{student["id"]}', state='down' if state == 'absent' else 'normal')
            late = ToggleButton(text='late', group=f'attended_{student["id"]}', state='down' if state == 'late' else 'normal')
            bx.add_widget(name)
            bx.add_widget(present)
            bx.add_widget(absent)
            bx.add_widget(late)

            self.attendance_list.add_widget(bx)

            has_yesterday = any(att['status'] for att in attendance if att['student_id'] == student['id'] and att['date'] == yesterday)
            if not has_yesterday:
                bx = BoxLayout()
                name = Label(text=student['student_name'])
                present = ToggleButton(text='present', group=f'attended_{student["id"]}')
                absent = ToggleButton(text='absent', group=f'attended_{student["id"]}')
                late = ToggleButton(text='late', group=f'attended_{student["id"]}')
                bx.add_widget(name)
                bx.add_widget(present)
                bx.add_widget(absent)
                bx.add_widget(late)

                self.attendance_list_yesterday.add_widget(bx)

        # Adding students to students list
        for student in students:
            std = AccordionItem(title=student['student_name'])
            bx = BoxLayout(orientation='vertical', size_hint_y=None)
            std.add_widget(bx)
            for key, value in student.items():
                if key == 'id':
                    continue
                key_value = BoxLayout(size_hint_y=None, height=80)
                key = Label(text=self.headers[key])
                value = Label(text=str(value))
                key_value.add_widget(key)
                key_value.add_widget(value)
                bx.add_widget(key_value)
            bx.height = sum(c.height for c in bx.children)

            self.student_list.add_widget(std)
        min_space = len(self.student_list.children) * self.student_list.min_space
        self.student_list.height = min_space + 80 * len(self.headers)

        # Adding grades
        today = datetime.today()
        for student in students:
            if student['status'] == 'inactive':
                continue
            bx = MDBoxLayout(padding=(10, 10, 10, 10), spacing=10)
            name = MDLabel(text=student['student_name'])
            date = DatePickerButton()
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

        # Adding fees
        today = datetime.today()
        for student in students:
            if student['status'] == 'inactive':
                continue
            bx = BoxLayout()
            name = Label(text=student['student_name'])
            date = TextInput(hint_text="Date (YYYY-MM-DD)")
            amount = TextInput(hint_text="Amount")
            receipt = TextInput(hint_text="Receipt")
            books = TextInput(hint_text="Books Payment")
            for fee in fees:
                if fee['student_id'] != student['id']:
                    continue
                dt = datetime.fromisoformat(fee['date'])
                if dt.year != today.year or dt.month != today.month:
                    continue
                date.text = fee['date']
                amount.text = fee['amount']
                receipt.text = fee['receipt']
                books.text = fee['books']
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
        students = {s['id']: s for s in students if s['status'] == 'active'}
        info = {}
        for fee in fees:
            dt = datetime.fromisoformat(fee['date'])
            date = (dt.year, dt.month)
            st = students[fee['student_id']]
            fee_data = {'id': fee['student_id'], 'name': st['student_name'], **fee}
            try:
                students_ = info[date]
            except KeyError:
                info[date] = {fee['student_id']: fee_data}
            else:
                try:
                    student = students_[fee['student_id']]
                except KeyError:
                    students_[fee['student_id']] = fee_data
                else:
                    student.update(fee_data)

        for grade in grades:
            dt = datetime(*map(int, grade['date'].split('-')), 1)
            date = (dt.year, dt.month)
            st = students[grade['student_id']]
            grade_data = {'id': grade['student_id'], 'name': st['student_name'], **grade}
            try:
                students_ = info[date]
            except KeyError:
                info[date] = {grade['student_id']: grade_data}
            else:
                try:
                    student = students_[grade['student_id']]
                except KeyError:
                    students_[grade['student_id']] = grade_data
                else:
                    student.update(grade_data)

        for att in attendance:
            dt = datetime.fromisoformat(att['date'])
            date = (dt.year, dt.month)
            st = students[att['student_id']]
            att_data = {'id': att['student_id'], 'name': st['student_name'], str(dt.day): att['status']}
            try:
                students_ = info[date]
            except KeyError:
                info[date] = {att['student_id']: att_data}
            else:
                try:
                    student = students_[att['student_id']]
                except KeyError:
                    students_[att['student_id']] = att_data
                else:
                    student.update(att_data)

        for date, students_ in sorted(info.items()):
            tab = StudentOverview(students_, date[0], date[1], holidays)
            self.student_overview.add_widget(tab)

    def add_child(self, data):
        api.add_student(*data)
        self.attendance_list.clear_widgets()
        self.student_list.clear_widgets()
        self.grades_list.clear_widgets()
        self.fees_list.clear_widgets()
        self.student_overview.clear_widgets()
        self.student_overview.clear_tabs()
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
            'active',
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

        with open('session.json') as f:
            session = json.load(f)
        if self.check_authenticate(
                session.get('key'), session.get('email'), session.get('first_name'), session.get('last_name')):
            self.root.current = 'teacher'
            self.root.ids.teacher_view.load_students()
        else:
            self.root.current = 'auth'

    def check_authenticate(self, key, email, first_name, last_name):
        print('authorize')
        if not api.auth(key, email, first_name, last_name):
            print("Couldn't authenticate")
            return False
        return True


Factory.register('TeacherView', module='main')
Factory.register('AuthView', module='main')
Factory.register('PlanView', module='widgets.plan_view')


if __name__ == '__main__':
    app = MonitoringApp()
    app.run()
