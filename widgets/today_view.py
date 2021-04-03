from datetime import datetime, timedelta

from kivy.properties import StringProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.snackbar import Snackbar

from api import api


class Attendance(MDBoxLayout):
    student_name = StringProperty()
    group = StringProperty()
    state = StringProperty()
    student_id = StringProperty()
    date = StringProperty()


class AttendanceContent(MDBoxLayout):
    pass


class TodayView(MDBoxLayout):
    def __init__(self, **kwargs):
        Builder.load_file('widgets/today_view.kv')
        super().__init__(**kwargs)

    def reload(self):
        try:
            students = api.students()
        except Exception as e:
            Snackbar(
                text=f"You seem to be offline, trying again in 10 seconds.",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=.5
            ).open()
            print(str(e))
            Clock.schedule_once(lambda *args: self.reload(), 10)
            return
        try:
            attendance = api.attendance()
        except Exception as e:
            Snackbar(
                text=f"You seem to be offline, trying again in 10 seconds.",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=.5
            ).open()
            print(str(e))
            Clock.schedule_once(lambda *args: self.reload(), 10)
            return

        self.attendance.clear_widgets()

        self.today_att = AttendanceContent()
        self.yesterday_att = AttendanceContent()

        std = MDExpansionPanel(
            content=self.today_att,
            panel_cls=MDExpansionPanelOneLine(
                text="Today"
            )
        )
        self.attendance.add_widget(std)
        std = MDExpansionPanel(
            content=self.yesterday_att,
            panel_cls=MDExpansionPanelOneLine(
                text="Yesterday"
            )
        )
        self.attendance.add_widget(std)

        today = datetime.today()
        today_ = today.strftime('%Y-%m-%d')
        yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        for student in students:
            if student['status'] == 'inactive':
                continue
            try:
                info = next(
                    att for att in attendance if att['student_id'] == student['id'] and att['date'] == today_)
            except StopIteration:
                info = {'student_id': student['id'], 'date': today_, 'status': ''}

            att = Attendance(
                student_name=student['student_name'], group='today'+student['id'], state=info['status'],
                student_id=info['student_id'], date=today_
            )
            self.today_att.add_widget(att)

            has_yesterday = any(
                att['status'] for att in attendance if att['student_id'] == student['id'] and att['date'] == yesterday)
            if not has_yesterday:
                att = Attendance(
                    student_name=student['student_name'], group='yesterday' + student['id'],
                    student_id=student['id'], date=yesterday
                )
                self.yesterday_att.add_widget(att)

    def save(self):
        data = []
        for att in self.today_att.children:
            data.append({'student_id': att.student_id, 'date': att.date, 'status': att.state})
        for att in self.yesterday_att.children:
            data.append({'student_id': att.student_id, 'date': att.date, 'status': att.state})
        try:
            api.upsert_attendance(data)
        except Exception as e:
            Snackbar(
                text=f"Attendance could not be saved because of: {str(e)}\nTrying again soon.",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=.5
            ).open()
