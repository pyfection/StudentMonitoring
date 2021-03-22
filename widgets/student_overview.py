import calendar
from datetime import datetime

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.label import Label
from kivy.lang.builder import Builder

from widgets.advanced_label import AdvancedLabel

Builder.load_file('widgets/student_overview.kv')


class StudentOverview(TabbedPanelItem):
    HOLIDAY_COLOR = (.2, .4, .7, 1)
    SUNDAY_COLOR = (.3, .5, .7, 1)
    PRESENT_COLOR = (0, .7, 0, 1)
    ABSENT_COLOR = (1, .7, 0, 1)
    LATE_COLOR = (.7, .7, 0, 1)

    def __init__(self, students, year, month, holidays, **kwargs):
        super(StudentOverview, self).__init__(text=f'{year} {month}', **kwargs)
        self.students = students
        holidays = set(
            d
            for y, m, d in [tuple(map(int, hd[0].split('-'))) for hd in holidays]
            if y == year and m == month
        )

        days = calendar.monthrange(year, month)[1]
        school_days = 0
        for i in range(1, 31+1):
            if i <= days:
                dt = datetime(year=year, month=month, day=i)
                weekday = dt.weekday()
                day = f'{i}\n{dt.strftime("%a")}'
            else:
                weekday = 0
                day = ''
            bg_color = None
            if weekday == 6:
                bg_color = self.SUNDAY_COLOR
            elif i in holidays:
                bg_color = self.HOLIDAY_COLOR
            else:
                school_days += 1
            self.grid.add_widget(AdvancedLabel(text=day, size_hint_x=None, width=80, bg_color=bg_color))

        for id_, student in students.items():
            days_present = len([a for a in student.values() if a in ("present", "late")])
            self.grid.add_widget(Label(text=id_))
            self.grid.add_widget(Label(text=student['name']))
            self.grid.add_widget(Label(text=f'{days_present}/{school_days}/{days}'))
            self.grid.add_widget(Label(text=student.get('math', '')))
            self.grid.add_widget(Label(text=student.get('english', '')))
            self.grid.add_widget(Label(text=student.get('hindi', '')))
            self.grid.add_widget(Label(text=student.get('amount', '')))
            self.grid.add_widget(Label(text=student.get('date', '')))
            self.grid.add_widget(Label(text=student.get('receipt', '')))
            self.grid.add_widget(Label(text=student.get('books', '')))
            for i in range(1, 31+1):
                if i <= days:
                    weekday = datetime(year=year, month=month, day=i).weekday()
                else:
                    weekday = 0
                att = student.get(str(i), '')
                bg_color = None
                if weekday == 6:
                    bg_color = self.SUNDAY_COLOR
                elif i in holidays:
                    bg_color = self.HOLIDAY_COLOR
                elif att == 'present':
                    att = 'P'
                    bg_color = self.PRESENT_COLOR
                elif att == 'absent':
                    att = 'A'
                    bg_color = self.ABSENT_COLOR
                elif att == 'late':
                    att = 'L'
                    bg_color = self.LATE_COLOR
                self.grid.add_widget(AdvancedLabel(text=att, bg_color=bg_color))
