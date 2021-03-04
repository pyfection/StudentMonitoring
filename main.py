from pprint import pprint

from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.accordion import AccordionItem
import gspread_mock as gspread
from google.oauth2.service_account import Credentials


class AuthView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_authenticate(self):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_file(
            'teacher_credentials.json',
            scopes=scopes
        )
        gc = gspread.authorize(credentials)
        print('authorize')
        # ToDo: add check if actually authorized
        # ToDo: check if part of secret key is same part of teacher secret key in config
        app = App.get_running_app()
        app.root.current = 'teacher'
        app.root.ids.teacher_view.gc = gc
        if self.existing_link.text:
            app.root.ids.teacher_view.load_sheet(self.existing_link.text)
        else:
            app.root.ids.teacher_view.new_sheet()


class TeacherView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.student_list.bind(minimum_height=self.student_list.setter('height'))
        self.sh = None
        self.student_master = {}
        self.headers = (
            'Date of joining',
            "roll no",
            "Name of student",
            "gr #",
            "Father's name",
            "Mother's name",
            "Address",
            "Phone number (Mother)",
            "Phone number (Father)",
            "Date of birth",
            "Aadhar Card number",
            "official Class",
            "Goes to goverment school (0 for no or 1 for yes",
            "Mother' main occupation",
            "Father' main occupation",
            "baseline M",
            "Baseline E",
            "Baseline Hindi",
            "Comment",
            "Teacher"
        )

    def new_sheet(self):
        sh = self.gc.create()
        # print(sh.sheet1.get('A1'))

    def load_sheet(self, link):
        self.sh = self.gc.open_by_url(link)
        print('open url')
        self.load_student_master()

    def load_student_master(self):
        ws = self.sh.worksheet("Student master")
        print('get worksheet')
        records = ws.get_all_records(head=2)
        # records = _TEST_DATA
        for student in records:
            student = {key.strip(): value for key, value in student.items()}
            std = AccordionItem(title=student["Name of student"])
            # std = BoxLayout(orientation='vertical', size_hint_y=None, height=500)
            # name = ToggleButton(text=student["Name of student"], group="students")
            # std.add_widget(name)
            bx = BoxLayout(orientation='vertical')
            std.add_widget(bx)
            for header in self.headers:
                key_value = BoxLayout(size_hint_y=None, height=20)
                key = Label(text=header)
                value = Label(text=str(student[header]))
                key_value.add_widget(key)
                key_value.add_widget(value)
                bx.add_widget(key_value)

            self.student_list.add_widget(std)


class NewChildView(BoxLayout):
    pass


class MonitoringApp(App):
    def build(self):
        # ToDo: remove after testing:
        self.root.ids.first_name.text = 'Abida'
        self.root.ids.last_name.text = 'Teacher'
        self.root.ids.email.text = 'abida@gmail.com'
        self.root.ids.private_key.text = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD1kPVfoyWeBEJh\nUGdS4662qwp0qIctqOBRfvpRVYWuXZKqqxoszRN8L4QbnFa2o3ULgA4QfcXTNBZa\nV8GEe6ueOP875pVDJa+FIRPRg3B+S5tYkSZwRW7HeaMXcqr+4TWUsQv21EL04nEW\nNrWeP4XOEOXsUaU3hqIGaJVh1GZ7UiBxsc9VkOPV+Kx9vUjqu4Q3RrKLqFi4MYdo\nfZKEVAc7++9BsT8mlyS85S8ZsQnSt7A4JzDahu4rjf71fOp2sA3xC2zF2MVbPg0O\nhJH2ql2dqx1wsCb/RkXxGGcb/lG3FRkoCb0AzhRh98sg9Lzs2bSEHONWSCDlhCE1\n9eMXuW+xAgMBAAECggEAPWHXb+lCTyod5KDaPvYyNy9wbOIubgujTMO6cue3g3MY\n5QfhglbdusJO2a793ufjazU+bsFdmHJR7xG2CfV229U/+XtlDpSGN/chctLR5QPl\nqCEaNGCqtPpy+bq8QvtM7ybFSJTcysUqguS4h761peGD84siCwvghs0QIBTdbBAJ\nNVFb5H3sd0yNMwoNsOTqeop9KgNS+jwkoCuWQlnsqIQteAw/lo1c5Q9lIdqJgfJn\nPHHk7X9sstwbJtTY0UfH2YlDZ5J3VQz55Gpq9N1xAZTUli2ffbUt4JZeYZE8chyK\nVK5aw7JMqcfM7ne4abfP2du/k9kYu1VtaxcdbpF3hQKBgQD/XtbYB1A7Xuv1o7ui\n7Hh7W8iNmgjmWIFW+t5ax2PxOFOILkqWClCqmVEhYoBxOQ5ToNvSazYjE4/5fc/B\n32Zx1TIxlBIKDF0yA9A5Nbu5fg4Z+OrQ0ArDWfKmzcc2ZPj3oLGE/UfrxMhlL9cJ\nsbWO8SQMXRezWvb3acwJ7ondNQKBgQD2K+6UJ10GoXgiom6u58jREbQuBe81N01J\ngkAXrQ7LDkJujMMO0KYDtbkIPwCxeJmOTaZCI8C6PkMl2hCfffVToAhtFzBQZw14\n1q9HFi4L3itdzOl9x00s3xFLtl9MrnRu3S1+us5Yto5vb2CIDt6w2y/7KxN8NFh+\n8BX6X57kDQKBgQCYz/a+RPoU3QNT9YuFvf2Gy/CiE4e510Jmey5toh1DLpKFzjWh\nvUByJdavpJL5rcvN7Vc9fhxiNwWTpV6aRAW4nnwvwMxeqPFnyXJjmazhHfZwQky5\ncZTPO1cBy+emvBtjiwxPaYUNJ69HJa6HRYlApToOD/Lrx8Y7XVrUoqJq9QKBgQDX\nhF67Fjs7MuIacFq2hfYqE3XLVSa3UFM5p+60y63H2BQQ9OtQbRrq5I25ym6w8QR+\nsTx9aw+v/hKLcP5co8nEDLdTyplhytbglBOgCKsHeNo+pMdGdtX6EtDxmBiW6aTF\n6p2J9cHxqOHKbZf1hg8whrTbEDte4fUYLNkQ+eYBgQKBgAPTwAt5n8gw5cdGzFtL\nzBrpY4GtY5jHPGIEoP/w/NU+oy8OBuegtImTaQhZ999OYSGyNBXdLXnP+xQydsbM\nb4IKtY7oCLejodUmFdzDWn1K7GU3MwWCUvxoOH3ldzA+NOXXiSFOYrqnIrMrx3P0\nd0tYpWydA4FYUHR8Qg4UJDKj\n-----END PRIVATE KEY-----\n"
        self.root.ids.existing_link.text = 'https://docs.google.com/spreadsheets/d/1YsJGfi9c32wdVyIR-JpQwPnjRiIlM8mSWCZZjRiv-cM'


Factory.register('TeacherView', module='main')
Factory.register('AuthView', module='main')


if __name__ == '__main__':
    app = MonitoringApp()
    app.run()
