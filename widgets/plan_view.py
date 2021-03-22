from datetime import date, timedelta

from kivy.lang.builder import Builder
from kivy.properties import ListProperty, DictProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivymd.uix.picker import MDDatePicker


Builder.load_file('widgets/plan_view.kv')


PROTECTED_SUBJECTS = ["Math", "English", "Hindi"]


class SubjectDesc(TextInput):
    pass


class MonthRow(BoxLayout):
    initial = True
    month = StringProperty()
    data = DictProperty()
    descs = {}

    def on_data(self, inst, data):
        for subject, desc in self.descs.items():
            desc.text = data.get(subject, '')

    def add_subject(self, subject):
        sj = SubjectDesc()
        self.descs[subject] = sj
        # sj.bind(text=lambda inst, text: self.)
        self.add_widget(sj)


class RangeRow(BoxLayout):
    initial = True
    start = StringProperty()
    end = StringProperty()
    data = DictProperty()
    descs = {}

    def on_data(self, inst, data):
        for subject, desc in self.descs.items():
            desc.text = data.get(subject, '')

    def add_subject(self, subject):
        sj = SubjectDesc()
        self.descs[subject] = sj
        # sj.bind(text=lambda inst, text: self.)
        self.add_widget(sj)


class PlanView(BoxLayout):
    initial = True
    subjects = ListProperty()
    data = DictProperty()

    def on_subjects(self, inst, subjects):
        if self.initial:
            for subject in subjects:
                self.add_subject(subject)
            self.initial = False
        else:
            self.add_subject(subjects[-1])

    def on_data(self, inst, data):
        for month, mdata in data['months'].items():
            self.add_month(month, mdata)

    def show_date_picker(self, month):
        year, month = map(int, month.split('-'))
        date_dialog = MDDatePicker(year=year, month=month, mode="range")
        date_dialog.bind(on_save=self.add_date_range)
        date_dialog.open()

    def add_subject(self, subject):
        if subject in PROTECTED_SUBJECTS:
            wg = Label(size_hint_x=None, width=400, text=subject)
        else:
            wg = TextInput(size_hint_x=None, width=400, text=subject)

        self.ids.subjects.add_widget(wg, index=1)
        for row in self.rows.children:
            row.add_subject(subject)
        self.ids.subjects.width = sum(c.width for c in self.ids.subjects.children)

    def add_date_range(self, instance, value, date_range):
        start = date_range[0].isoformat()
        end = date_range[-1].isoformat()
        row = RangeRow(start=start, end=end)
        row.subjects = self.subjects
        row.data = self.data['ranges']
        for i, row_ in enumerate(reversed(self.rows.children)):
            try:
                smaller = start < row_.month
            except AttributeError:
                smaller = start < row_.start
            if smaller:
                self.rows.add_widget(row, index=i)
                break
        else:
            self.rows.add_widget(row)

    def add_month(self, month, mdata=None):
        row = MonthRow(month=month)
        row.add.bind(on_press=lambda inst, month=month: self.show_date_picker(month))
        for subject in self.subjects:
            row.add_subject(subject)
        if mdata:
            row.data = mdata
        self.rows.add_widget(row)

    def new_month(self):
        latest = max(self.data['months'].keys())
        year, month = map(int, latest.split('-'))
        latest_month = date(year, month+1, 1)
        month_str = latest_month.strftime('%Y-%m')
        self.add_month(month_str)
        self.data['months'][month_str] = {}

    def update_data(self):
        data = {'months': {}, 'ranges': {}}

        for row in self.rows.children:
            if isinstance(row, MonthRow):
                row_data = {}
                data['months'][row.month] = row_data
            elif isinstance(row, RangeRow):
                row_data = {}
                data['ranges'][row.start] = row_data
            else:
                raise TypeError("row needs to be of type MonthRow or RangeRow")

            for subject, desc in row.descs.items():
                row_data[subject] = desc
