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


class MonitoringApp(App):
    def build(self):
        self.icon = 'icon.png'
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "LightGreen"
        self.manager = self.root.manager

    def on_start(self):
        thread = Thread(target=self.sync_all)
        thread.start()
        # Clock.schedule_interval(lambda *args: api.sync(), 60)

    def sync_all(self, clear=False):
        def change_screen(name):
            self.manager.current = name

        if clear:
            for filename in os.listdir('local'):
                file_path = os.path.join('local', filename)
                os.unlink(file_path)

        print("Syncing Students")
        api.sync_students(threading=False)
        print("Syncing Attendance")
        api.sync_attendance(threading=False)
        print("Syncing Fees")
        api.sync_fees(threading=False)
        print("Syncing Grades")
        api.sync_grades(threading=False)
        print("Syncing Plans")
        api.sync_plans(threading=False)
        print("Everything synced!")
        Clock.schedule_once(lambda dt: change_screen('today'))


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
