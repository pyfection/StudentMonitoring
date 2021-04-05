from datetime import date, timedelta

from kivy.lang.builder import Builder
from kivy.properties import ListProperty, DictProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.label import MDLabel
from kivymd.uix.picker import MDDatePicker

from api import api


Builder.load_file('widgets/plan_view.kv')


DEFAULT_SUBJECTS = ["Math", "English", "Hindi"]


class SubjectDesc(MDTextFieldRect):
    pass


class MonthRow(MDBoxLayout):
    initial = True
    month = StringProperty()
    data = ListProperty()
    descs = ListProperty()

    def on_data(self, inst, data):
        for i, desc in enumerate(self.descs):
            desc.text = data[i]

    def add_subject(self):
        sj = SubjectDesc()
        self.descs.append(sj)
        self.add_widget(sj)


class RangeRow(MDBoxLayout):
    initial = True
    start = StringProperty()
    end = StringProperty()
    data = ListProperty()
    descs = ListProperty()

    def on_data(self, inst, data):
        for i, desc in enumerate(self.descs):
            desc.text = data[i]

    def add_subject(self):
        sj = SubjectDesc()
        self.descs.append(sj)
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
        if subject in DEFAULT_SUBJECTS:
            wg = MDLabel(size_hint_x=None, width=400, text=subject, halign='center', bold=True)
        else:
            wg = MDTextField(size_hint_x=None, width=400, text=subject)

        self.ids.subjects.add_widget(wg)
        for row in self.rows.children:
            row.add_subject()
        self.ids.subjects.width = sum(c.width for c in self.ids.subjects.children)

    def add_range(self, start, end, data=None):
        row = RangeRow(start=start, end=end)
        for subject in self.ids.subjects.children[:-1]:
            row.add_subject()
        if not data:
            data = {}
        row.data = [data.get(s, '') for s in self.subjects]
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
        for subject in self.ids.subjects.children[:-1]:
            row.add_subject()
        if not mdata:
            mdata = {}
        row.data = [mdata.get(s, '') for s in self.subjects]
        self.rows.add_widget(row)

    def new_month(self):
        if self.data['months']:
            latest = max(self.data['months'].keys())
            year, month = map(int, latest.split('-'))
            latest_month = date(year, month+1, 1)
        else:  # Doesn't have any months set yet
            latest_month = date.today()
        month_str = latest_month.strftime('%Y-%m')
        self.add_month(month_str)
        self.data['months'][month_str] = {}

    def save(self):
        data = {'months': [], 'ranges': []}

        for row in self.rows.children:
            for i, subject in enumerate(self.subjects):
                desc = row.descs[i]
                if isinstance(row, MonthRow):
                    data['months'].append({'date': row.month, 'subj': subject, 'text': desc.text})
                elif isinstance(row, RangeRow):
                    data['ranges'].append({'start': row.start, 'end': row.end, 'subj': subject, 'text': desc.text})
                else:
                    raise TypeError("row needs to be of type MonthRow or RangeRow")

        api.upsert_plan(data)

    def reload(self):
        subjects = DEFAULT_SUBJECTS.copy()

        months = {}
        for plan in api.month_plans():
            if plan['subj'] not in subjects:
                subjects.append(plan['subj'])
            try:
                months[plan['date']][plan['subj']] = plan['text']
            except KeyError:
                months[plan['date']] = {plan['subj']: plan['text']}

        ranges = {}
        for plan in api.range_plans():
            if plan['subj'] not in subjects:
                subjects.append(plan['subj'])
            try:
                ranges[(plan['start'], plan['end'])][plan['subj']] = plan['text']
            except KeyError:
                ranges[(plan['start'], plan['end'])] = {plan['subj']: plan['text']}

        self.subjects = subjects
        self.data = {
            'months': months,
            'ranges': ranges
        }
