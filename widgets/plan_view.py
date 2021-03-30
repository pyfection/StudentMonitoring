from datetime import date, timedelta

from kivy.lang.builder import Builder
from kivy.properties import ListProperty, DictProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.label import MDLabel
from kivymd.uix.picker import MDDatePicker

from api import api


Builder.load_file('widgets/plan_view.kv')


PROTECTED_SUBJECTS = ["Math", "English", "Hindi"]


class SubjectDesc(MDTextFieldRect):
    pass


class MonthRow(MDBoxLayout):
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


class RangeRow(MDBoxLayout):
    initial = True
    start = StringProperty()
    end = StringProperty()
    data = DictProperty()
    descs = DictProperty()

    def on_data(self, inst, data):
        for subject, desc in self.descs.items():
            desc.text = data.get(subject, '')

    def add_subject(self, subject):
        sj = SubjectDesc()
        self.descs[subject] = sj
        # sj.bind(text=lambda inst, text: self.)
        self.add_widget(sj)


class PlanView(MDBoxLayout):
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
        for (start, end), mdata in data['ranges'].items():
            self.add_range(start, end, mdata)

    def show_date_picker(self, month):
        year, month = map(int, month.split('-'))
        date_dialog = MDDatePicker(year=year, month=month, mode="range")
        date_dialog.bind(on_save=lambda inst, value, date_range: self.add_date_range(*date_range))
        date_dialog.open()

    def add_subject(self, subject):
        if subject in PROTECTED_SUBJECTS:
            wg = MDLabel(size_hint_x=None, width=400, text=subject, halign='center', bold=True)
        else:
            wg = MDTextField(size_hint_x=None, width=400, text=subject)

        self.ids.subjects.add_widget(wg)
        for row in self.rows.children:
            row.add_subject(subject)
        self.ids.subjects.width = sum(c.width for c in self.ids.subjects.children)

    def add_range(self, start, end, data=None):
        row = RangeRow(start=start, end=end)
        for subject in self.subjects:
            row.add_subject(subject)
        if data:
            row.data = data
        for i, row_ in enumerate(reversed(self.rows.children)):
            try:
                smaller = start < row_.month
            except AttributeError:
                smaller = start < row_.start
            if smaller:
                self.rows.add_widget(row, index=-i)
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

    def save(self):
        data = {'months': {}, 'ranges': {}}

        for row in self.rows.children:
            for subject, desc in row.descs.items():
                if isinstance(row, MonthRow):
                    data['months'][(row.month, subject)] = desc.text
                elif isinstance(row, RangeRow):
                    data['ranges'][(row.start, row.end, subject)] = desc.text
                else:
                    raise TypeError("row needs to be of type MonthRow or RangeRow")

        api.upsert_plan(data)

    def reload(self):
        subjects = ["Math", "English", "Hindi"]

        months = {}
        for (month, subject), desc in api.month_plans().items():
            if subject not in subjects:
                subjects.append(subject)
            try:
                months[month][subject] = desc
            except KeyError:
                months[month] = {subject: desc}

        ranges = {}
        for (start, end, subject), desc in api.range_plans().items():
            if subject not in subjects:
                subjects.append(subject)
            try:
                ranges[(start, end)][subject] = desc
            except KeyError:
                ranges[(start, end)] = {subject: desc}

        self.subjects = list(subjects)
        self.data = {
            'months': months,
            'ranges': ranges
        }
