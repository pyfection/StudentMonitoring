import calendar
from datetime import datetime

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.label import Label
from kivy.lang.builder import Builder

Builder.load_file('widgets/student_overview.kv')


class StudentOverview(TabbedPanelItem):
    def __init__(self, students, year, month, **kwargs):
        super(StudentOverview, self).__init__(text=f'{year} {month}', **kwargs)
        self.students = students

        days = calendar.monthrange(year, month)[1]
        for i in range(1, 31+1):
            if i <= days:
                dt = datetime(year=year, month=month, day=i)
                day = f'{i}\n{dt.strftime("%a")}'
            else:
                day = ''
            self.grid.add_widget(Label(text=day, size_hint_x=None, width=40))

        for id_, student in students.items():
            self.grid.add_widget(Label(text=id_))
            self.grid.add_widget(Label(text=student['name']))
            self.grid.add_widget(Label(text=student.get('math', '')))
            self.grid.add_widget(Label(text=student.get('english', '')))
            self.grid.add_widget(Label(text=student.get('hindi', '')))
            self.grid.add_widget(Label(text=student.get('date', '')))
            self.grid.add_widget(Label(text=student.get('amount', '')))
            self.grid.add_widget(Label(text=student.get('receipt', '')))
            self.grid.add_widget(Label(text=student.get('books', '')))
            for i in range(1, 31+1):
                self.grid.add_widget(Label(text=student.get(str(i), '')))
