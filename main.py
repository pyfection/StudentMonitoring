import os
import re
from datetime import datetime
import json
from uuid import uuid4
from threading import Thread

from kivymd.app import MDApp as App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDList

from api import api


Window.softinput_mode = 'pan'


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
        data = {
            "id": str(uuid4()),
            "student_name": self.name.text,
            "student_gender": self.gender.text,
            'joining_date': self.date_of_joining.text,
            "group": self.group.text,
            "name_father": self.name_father.text,
            "name_mother": self.name_mother.text,
            "address": self.address.text,
            "phone_number_mother": self.phone_mother.text,
            "phone_number_father": self.phone_father.text,
            "dob": self.dob.text,
            "aadhar_card_number": self.aadhar.text,
            "official_class": self.official_class.text,
            "goes_goverment_school": str(int(self.goes_government_school_yes.state == "down")),
            "occupation_mother": self.occupation_mother.text,
            "occupation_father": self.occupation_father.text,
            "status": 'active',
            "teacher": api.teacher,
            "comment": self.comment.text,
        }
        app = App.get_running_app()
        app.manager.current = 'students'
        api.add_student(**data)


class MonitoringApp(App):
    def build(self):
        self.icon = 'icon.png'
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "LightGreen"
        self.manager = self.root.manager

    def on_start(self):
        # Clock.schedule_once(lambda *args: self.on_ready(), 4)
        thread = Thread(target=self.on_ready)
        print('thread starting')
        thread.start()
        print('thread started')
        Clock.schedule_interval(lambda *args: api.sync(), 60)

    def on_ready(self):
        def change_screen(name):
            self.manager.current = name
        path = 'session.json'
        if os.path.exists(path):
            with open(path) as f:
                session = json.load(f)

            success = api.auth(
                session.get('key'), session.get('email'), session.get('first_name'), session.get('last_name')
            )
            if success:
                print("Successfully Authenticated")
            else:
                print("Couldn't Authenticated, starting offline mode")
            current = 'today'
        else:
            current = 'auth'
        Clock.schedule_once(lambda dt, current=current: change_screen(current))

    def check_authenticate(self, key, email, first_name, last_name):
        print('authorize')
        if not api.auth(key, email, first_name, last_name):
            print("Couldn't authenticate")
            self.manager.current = 'auth'
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
