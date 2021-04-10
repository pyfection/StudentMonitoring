from uuid import uuid4
import re
from datetime import datetime

from kivymd.app import MDApp as App
from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import BoxLayout

from api import api


Builder.load_file('views/student_detail_view.kv')


class StudentDetailView(BoxLayout):
    # @staticmethod
    # def correct_date_format(inst):
    #     for i in (4, 7, 10):
    #         try:
    #             if inst.text[i] != '-':
    #                 inst.text = inst.text[:i] + '-' + inst.text[i:]
    #                 inst.cursor = inst.get_cursor_from_index(inst.cursor_index() + 1)
    #         except IndexError:
    #             break

    @staticmethod
    def check_date_format(text):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', text):
            return False
        year, month, day = map(int, text.split('-'))
        today = datetime.today()
        if not (1950 < year < today.year and 1 <= month <= 12 and 1 <= day <= 31):
            return False
        try:
            datetime(year, month, day)
        except ValueError:
            return False
        return True

    def reload(self, uid=''):
        student = next((s for s in api.students() if s['id'] == uid), {})
        self.student_id.text = uid
        self.name.text = student.get("student_name", '')
        self.gender.text = student.get("student_gender", '')
        self.date_of_joining.text = student.get('joining_date', '')
        self.group.text = student.get("group", '')
        self.name_father.text = student.get("name_father", '')
        self.name_mother.text = student.get("name_mother", '')
        self.address.text = student.get("address", '')
        self.phone_mother.text = student.get("phone_number_mother", '')
        self.phone_father.text = student.get("phone_number_father", '')
        self.dob.text = student.get("dob", '')
        self.aadhar.text = student.get("aadhar_card_number", '')
        self.official_class.text = student.get("official_class", '')
        self.goes_government_school_yes.state = "down" if student.get("goes_goverment_school", '0') == '1' else "normal"
        self.occupation_mother.text = student.get("occupation_mother", '')
        self.occupation_father.text = student.get("occupation_father", '')
        self.comment.text = student.get("comment", '')

    def submit(self):
        # ToDo: add validation checks
        uid = self.student_id.text
        data = {
            "id": uid or str(uuid4()),
            "student_name": self.name.text,
            "student_gender": self.gender.text,
            'joining_date': self.date_of_joining.text,
            "group": self.group.text,
            "name_father": self.name_father.text,
            "name_mother": self.name_mother.text,
            "address": self.address.text,
            "phone_number_mother": self.phone_mother.text,
            "phone_number_father": self.phone_father.text,
            "dob": self.dob.text,
            "aadhar_card_number": self.aadhar.text,
            "official_class": self.official_class.text,
            "goes_goverment_school": str(int(self.goes_government_school_yes.state == "down")),
            "occupation_mother": self.occupation_mother.text,
            "occupation_father": self.occupation_father.text,
            "status": 'active',
            "comment": self.comment.text,
        }
        app = App.get_running_app()
        if uid:
            api.upsert_students([data])
        else:
            api.add_student(**data)
        api.sync_students()
        app.manager.current = 'students'

