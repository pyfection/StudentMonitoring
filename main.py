import os
import json
from threading import Thread

from kivymd.app import MDApp as App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout

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


class MonitoringApp(App):
    def build(self):
        self.icon = 'icon.png'
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "LightGreen"
        self.manager = self.root.manager

    def on_start(self):
        thread = Thread(target=self.on_ready)
        thread.start()
        # Clock.schedule_interval(lambda *args: api.sync(), 60)

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
Factory.register('NewStudentView', module='widgets.new_student_view')
Factory.register('GradesView', module='widgets.grades_view')
Factory.register('FeesView', module='widgets.fees_view')
Factory.register('PlanView', module='widgets.plan_view')
Factory.register('OverviewView', module='widgets.overview_view')
Factory.register('MDFillRoundToggleButton', module='widgets.md_toggle_button')
Factory.register('DataTable', module='widgets.data_table')


if __name__ == '__main__':
    app = MonitoringApp()
    app.run()
