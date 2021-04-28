from datetime import datetime

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from api import api
from widgets.date_picker_button import DatePickerButton


class FeesRow(MDBoxLayout):
    student_id = StringProperty()
    name = StringProperty()
    date = StringProperty()
    amount = StringProperty()
    receipt = StringProperty()
    books = StringProperty()


class FeesView(MDBoxLayout):
    def __init__(self, **kwargs):
        Builder.load_file('views/fees_view.kv')
        super().__init__(**kwargs)

    def reload(self):
        self.fees_list.clear_widgets()

        students = api.students()
        fees = api.fees()

        total_fees = 0
        today = datetime.today()
        for student in students:
            if student['status'] == 'inactive':
                continue

            row = FeesRow()
            row.student_id = student['id']
            row.name = student['student_name']

            for fee in fees:
                if fee['student_id'] != student['id']:
                    continue
                dt = datetime.fromisoformat(fee['date'])
                if dt.year != today.year or dt.month != today.month:
                    continue
                row.date = dt.strftime('%Y-%m-%d')
                row.amount = fee['amount']
                total_fees += float(row.amount)
                row.receipt = fee['receipt']
                row.books = fee['books']
                break

            self.fees_list.add_widget(row)
        self.toolbar.title = f"Fees     [size=10]{total_fees} \u20B9[/size]"

    def save(self):
        data = []
        for row in self.fees_list.children:
            data.append({
                'student_id': row.student_id, 'date': row.date,
                'amount': row.amount, 'receipt': row.receipt, 'books': row.books
            })
        api.upsert_fees(data)
        api.sync_fees()
