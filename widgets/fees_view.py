from datetime import datetime

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from api import api
from widgets.date_picker_button import DatePickerButton


class FeesView(MDBoxLayout):
    def __init__(self, **kwargs):
        Builder.load_file('widgets/fees_view.kv')
        super().__init__(**kwargs)

    def reload(self):
        self.fees_list.clear_widgets()

        students = api.students()
        fees = api.fees()

        today = datetime.today()
        for student in students:
            if student['status'] == 'inactive':
                continue
            bx = MDBoxLayout(padding=(10, 10, 10, 10), spacing=10, adaptive_height=True)
            name = MDLabel(text=student['student_name'])
            date = DatePickerButton(format='%b-%Y')
            amount = MDTextField(hint_text="Amount")
            receipt = MDTextField(hint_text="Receipt")
            books = MDTextField(hint_text="Books Payment")
            for fee in fees:
                if fee['student_id'] != student['id']:
                    continue
                dt = datetime.fromisoformat(fee['date'])
                if dt.year != today.year or dt.month != today.month:
                    continue
                date.text = dt.strftime('%b-%Y')
                amount.text = fee['amount']
                receipt.text = fee['receipt']
                books.text = fee['books']
                break
            bx.add_widget(name)
            bx.add_widget(date)
            bx.add_widget(amount)
            bx.add_widget(receipt)
            bx.add_widget(books)

            self.fees_list.add_widget(bx)
