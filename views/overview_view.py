import calendar
from datetime import datetime

from kivy.lang.builder import Builder
from kivy.properties import DictProperty, NumericProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout

from api import api
import settings
from widgets.advanced_label import AdvancedLabel

Builder.load_file('views/overview_view.kv')


class GridLabel(MDLabel):
    pass


class OverviewTab(MDBoxLayout, MDTabsBase):
    year = NumericProperty()
    month = NumericProperty()
    students = DictProperty()
    holidays = DictProperty()

    def on_students(self, inst, students):
        # General headers
        data = [
            {'text': "ID", 'width': 800},
            {'text': "Name", 'width': 600},
            {'text': "Attendance Days", 'width': 500},
            {'text': "Math", 'width': 200},
            {'text': "English", 'width': 200},
            {'text': "Hindi", 'width': 200},
            {'text': "Fees Amount", 'width': 180},
            {'text': "Fees Date", 'width': 180},
            {'text': "Fees Receipt", 'width': 180},
            {'text': "Fees Books", 'width': 180},
        ]

        # Days headers
        holidays = set(
            d
            for y, m, d in [tuple(map(int, hd.split('-'))) for hd in self.holidays.keys()]
            if y == self.year and m == self.month
        )

        days = calendar.monthrange(self.year, self.month)[1]
        school_days = 0
        for i in range(1, 31 + 1):
            if i <= days:
                dt = datetime(year=self.year, month=self.month, day=i)
                weekday = dt.weekday()
                day = f'{i}\n{dt.strftime("%a")}'
            else:
                weekday = 0
                day = ''
            bg_color = (1, 1, 1, 0)
            if weekday == 6:
                bg_color = settings.SUNDAY_COLOR
            elif i in holidays:
                bg_color = settings.HOLIDAY_COLOR
            else:
                school_days += 1
            data.append({'text': day, 'bg_color': bg_color, 'width': 90})

        # Student rows
        for id_, student in students.items():
            days_present = len([a for a in student.values() if a in ("present", "late")])
            data.append({'text': id_, 'width': 800})
            data.append({'text': student['name'], 'width': 600})
            data.append({'text': f'{days_present}/{school_days}/{days}', 'width': 500})
            data.append({'text': student.get('math', ''), 'width': 200})
            data.append({'text': student.get('english', ''), 'width': 200})
            data.append({'text': student.get('hindi', ''), 'width': 200})
            data.append({'text': student.get('amount', ''), 'width': 180})
            data.append({'text': student.get('date', ''), 'width': 180})
            data.append({'text': student.get('receipt', ''), 'width': 180})
            data.append({'text': student.get('books', ''), 'width': 180})
            for i in range(1, 31 + 1):
                if i <= days:
                    weekday = datetime(year=self.year, month=self.month, day=i).weekday()
                else:
                    weekday = 0
                att = student.get(str(i), '')
                bg_color = None
                if weekday == 6:
                    bg_color = settings.SUNDAY_COLOR
                elif i in holidays:
                    bg_color = settings.HOLIDAY_COLOR
                elif att == 'present':
                    att = 'P'
                    bg_color = settings.PRESENT_COLOR
                elif att == 'absent':
                    att = 'A'
                    bg_color = settings.ABSENT_COLOR
                elif att == 'late':
                    att = 'L'
                    bg_color = settings.LATE_COLOR
                attrs = {'text': att, 'width': 90}
                if bg_color:
                    attrs['bg_color'] = bg_color
                data.append(attrs)

        self.grid.data = data


class OverviewView(MDBoxLayout):
    HOLIDAY_COLOR = (.2, .4, .7, 1)
    SUNDAY_COLOR = (.3, .5, .7, 1)

    def reload(self):
        students = api.students()
        fees = api.fees()
        grades = api.grades()
        attendance = api.attendance()
        holidays = api.holidays()

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
            tab = OverviewTab(year=date[0], month=date[1])
            tab.holidays = holidays
            tab.students = students_
            self.ids.tabs.add_widget(tab)
