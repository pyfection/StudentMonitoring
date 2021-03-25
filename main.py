from pprint import pprint
import re
from datetime import datetime
import json

from kivymd.app import MDApp as App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDList

from api import api


class AuthView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            with open('session.json') as f:
                self.session = json.load(f)
        except FileNotFoundError:
            self.session = {}


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
        self.icon = 'icon.png'
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "LightGreen"
        self.manager = self.root.manager

    def on_start(self):
        Clock.schedule_once(lambda *args: self.on_ready(), 4)  # ToDo: make sure this gets executed after everything is loaded

    def on_ready(self):
        with open('session.json') as f:
            session = json.load(f)

        self.check_authenticate(
            session.get('key'), session.get('email'), session.get('first_name'), session.get('last_name')
        )

    def check_authenticate(self, key, email, first_name, last_name):
        print('authorize')
        if not api.auth(key, email, first_name, last_name):
            print("Couldn't authenticate")
            self.root.current = 'auth'
            return False
        print("Successful authenticated")
        self.manager.current = 'today'
        # self.root.ids.teacher_view.load_students()

        with open('session.json', 'w') as f:
            json.dump(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "key": key,
                },
                f, indent=4
            )

        return True


Factory.register('AuthView', module='main')
# Factory.register('TeacherView', module='widgets.teacher_view')
Factory.register('TodayView', module='widgets.today_view')
Factory.register('StudentsView', module='widgets.students_view')
Factory.register('GradesView', module='widgets.grades_view')
Factory.register('FeesView', module='widgets.fees_view')
Factory.register('PlanView', module='widgets.plan_view')
Factory.register('OverviewView', module='widgets.overview_view')
Factory.register('MDFillRoundToggleButton', module='widgets.md_toggle_button')


if __name__ == '__main__':
    app = MonitoringApp()
    app.run()
