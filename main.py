import os
from threading import Thread

from kivymd.app import MDApp as App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.factory import Factory

from api import api


Window.softinput_mode = 'below_target'


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

        print("Syncing...")
        for sync in (api.sync_students, api.sync_attendance, api.sync_fees, api.sync_grades, api.sync_plans):
            success = sync(threading=False)
            if success is False:
                print("Couldn't synchronize, starting offline mode")
                break
        print("Everything synced!")
        Clock.schedule_once(lambda dt: change_screen('today'))


Factory.register('TodayView', module='views.today_view')
Factory.register('StudentsView', module='views.students_view')
Factory.register('StudentDetailView', module='views.student_detail_view')
Factory.register('GradesView', module='views.grades_view')
Factory.register('FeesView', module='views.fees_view')
Factory.register('PlanView', module='views.plan_view')
Factory.register('OverviewView', module='views.overview_view')
Factory.register('NumberInput', module='widgets.number_input')
Factory.register('MDFillRoundToggleButton', module='widgets.md_toggle_button')
Factory.register('DataTable', module='widgets.data_table')


if __name__ == '__main__':
    app = MonitoringApp()
    app.run()
