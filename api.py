from uuid import uuid4
import json

import gspread
from gspread.exceptions import APIError
from google.oauth2.service_account import Credentials
from google.auth.exceptions import TransportError


class API:
    gc = None
    sh = None
    teacher = None

    def auth(self, key, email, first_name, last_name):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_file(
            'credentials.json',
            scopes=scopes
        )
        self.gc = gspread.authorize(credentials)
        self.sh = self.gc.open_by_key(key)
        try:
            ws = self.sh.worksheet("Teachers")
        except (APIError, TransportError):
            return False

        values = [email, first_name, last_name]
        for row in ws.get_all_values():
            if row == values:
                break
        else:
            ws.append_row(values)
        self.teacher = email
        return True

    def holidays(self):
        try:
            with open('local/holidays.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def students(self):
        try:
            with open('local/students.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def teachers(self):
        try:
            with open('local/teachers.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def attendance(self):
        try:
            with open('local/attendance.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def fees(self):
        try:
            with open('local/fees.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def grades(self):
        try:
            with open('local/grades.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def range_plans(self):
        try:
            with open('local/range_plans.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def month_plans(self):
        try:
            with open('local/month_plans.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def add_student(self, **data):
        students = self.students()
        students.append(data)
        with open('local/students.json', 'w') as f:
            json.dump(students, f)

    def upsert_students(self, data):
        students = {
            student['id']: student
            for student in self.students()
        }
        data = {
            student['id']: student
            for student in data
        }
        students.update(data)
        students = [
            student for student in students.values()
        ]
        with open('local/students.json', 'w') as f:
            json.dump(students, f)

    def upsert_attendance(self, data):
        attendance = {(att['student_id'], att['date']): att['status'] for att in self.attendance()}
        data = {(att['student_id'], att['date']): att['status'] for att in data}
        attendance.update(data)
        attendance = [{'student_id': uid, 'date': date, 'status': status} for (uid, date), status in attendance.items()]
        with open('local/attendance.json', 'w') as f:
            json.dump(attendance, f)

    def upsert_grades(self, data):
        grades = {
            (grade['student_id'], grade['date']): (grade['gtype'], grade['math'], grade['english'], grade['hindi'])
            for grade in self.grades()
        }
        data = {
            (grade['student_id'], grade['date']): (grade['gtype'], grade['math'], grade['english'], grade['hindi'])
            for grade in data
        }
        grades.update(data)
        grades = [
            {'student_id': student_id, 'date': date, 'gtype': gtype, 'math': math, 'english': english, 'hindi': hindi}
            for (student_id, date), (gtype, math, english, hindi) in grades.items()
            if date and gtype and math and english and hindi
        ]
        with open('local/grades.json', 'w') as f:
            json.dump(grades, f)

    def upsert_fees(self, data):
        fees = {
            (fee['student_id'], fee['date']): (fee['amount'], fee['receipt'], fee['books'])
            for fee in self.fees()
        }
        data = {
            (fee['student_id'], fee['date']): (fee['amount'], fee['receipt'], fee['books'])
            for fee in data
        }
        fees.update(data)
        fees = [
            {'student_id': student_id, 'date': date, 'amount': amount, 'receipt': receipt, 'books': books}
            for (student_id, date), (amount, receipt, books) in fees.items()
            if date and amount and receipt
        ]
        with open('local/fees.json', 'w') as f:
            json.dump(fees, f)

    def upsert_plan(self, data):
        data['months'] = {(plan['date'], plan['subj']): plan for plan in data['months']}
        data['ranges'] = {(plan['start'], plan['end'], plan['subj']): plan for plan in data['ranges']}
        month_plans = {(plan['date'], plan['subj']): plan for plan in self.month_plans()}
        range_plans = {(plan['start'], plan['end'], plan['subj']): plan for plan in self.range_plans()}

        month_plans.update(data['months'])
        range_plans.update(data['ranges'])

        month_plans = [plan for plan in month_plans.values() if plan['text']]
        range_plans = [plan for plan in range_plans.values() if plan['text']]

        with open('local/month_plans.json', 'w') as f:
            json.dump(month_plans, f)

        with open('local/range_plans.json', 'w') as f:
            json.dump(range_plans, f)

    def sync(self):
        # Students
        local_students = self.students()
        local_students = {student['id']: student for student in local_students}
        online_students = self.sh.worksheet("Students").get_all_values()
        online_students = {
            student[0]: {
                "id": student[0],
                "student_name": student[1],
                "student_gender": student[2],
                'joining_date': student[3],
                "group": student[4],
                "name_father": student[5],
                "name_mother": student[6],
                "address": student[7],
                "phone_number_mother": student[8],
                "phone_number_father": student[9],
                "dob": student[10],
                "aadhar_card_number": student[11],
                "official_class": student[12],
                "goes_goverment_school": student[13],
                "occupation_mother": student[14],
                "occupation_father": student[15],
                "status": student[16],
                "teacher": student[17],
                "comment": student[18],
            } for student in online_students}

        online_students.update(local_students)
        self.upsert_students(list(online_students.values()))
        data = [
            [
                student["id"],
                student["student_name"],
                student["student_gender"],
                student['joining_date'],
                student["group"],
                student["name_father"],
                student["name_mother"],
                student["address"],
                student["phone_number_mother"],
                student["phone_number_father"],
                student["dob"],
                student["aadhar_card_number"],
                student["official_class"],
                student["goes_goverment_school"],
                student["occupation_mother"],
                student["occupation_father"],
                student["status"],
                student["teacher"],
                student["comment"],
            ] for student in online_students.values()]
        ws = self.sh.worksheet("Students")
        ws.clear()
        ws.insert_rows(data)

        # Attendance
        local_attendance = self.attendance()
        local_attendance = {(attendance['student_id'], attendance['date']): attendance for attendance in local_attendance}
        online_attendance = self.sh.worksheet("Attendance").get_all_values()
        online_attendance = {
            (attendance[0], attendance[1]): {
                "student_id": attendance[0],
                "date": attendance[1],
                "status": attendance[2],
            } for attendance in online_attendance}

        online_attendance.update(local_attendance)
        self.upsert_attendance(list(online_attendance.values()))
        data = [
            [
                attendance["student_id"],
                attendance["date"],
                attendance["status"],
            ] for attendance in online_attendance.values() if attendance['status']]
        ws = self.sh.worksheet("Attendance")
        ws.clear()
        ws.insert_rows(data)

        # Fees
        local_fees = self.fees()
        local_fees = {(fee['student_id'], fee['date']): fee for fee in local_fees}
        online_fees = self.sh.worksheet("Fees").get_all_values()
        online_fees = {
            (fee[0], fee[1]): {
                "student_id": fee[0],
                "date": fee[1],
                "amount": fee[2],
                "receipt": fee[3],
            } for fee in online_fees}

        online_fees.update(local_fees)
        self.upsert_fees(list(online_fees.values()))
        data = [
            [
                fee["student_id"],
                fee["date"],
                fee["amount"],
                fee["receipt"],
            ] for fee in online_fees.values()]
        ws = self.sh.worksheet("Fees")
        ws.clear()
        ws.insert_rows(data)

        # Grades
        local_grades = self.grades()
        local_grades = {(grade['student_id'], grade['date']): grade for grade in local_grades}
        online_grades = self.sh.worksheet("Grades").get_all_values()
        online_grades = {
            (grade[0], grade[1]): {
                "student_id": grade[0],
                "date": grade[1],
                "gtype": grade[2],
                "math": grade[3],
                "english": grade[4],
                "hindi": grade[5],
            } for grade in online_grades}

        online_grades.update(local_grades)
        self.upsert_grades(list(online_grades.values()))
        data = [
            [
                grade["student_id"],
                grade["date"],
                grade["gtype"],
                grade["math"],
                grade["english"],
                grade["hindi"],
            ] for grade in online_grades.values() if grade['date']]
        ws = self.sh.worksheet("Grades")
        ws.clear()
        ws.insert_rows(data)

        # Plans
        local_month_plans = self.month_plans()
        local_month_plans = {(plan['date'], plan['subj']): plan for plan in local_month_plans}
        online_month_plans = self.sh.worksheet("MonthPlans").get_all_values()
        online_month_plans = {
            (plan[0], plan[1]): {
                "date": plan[0],
                "subj": plan[1],
                "text": plan[2],
            } for plan in online_month_plans}

        online_month_plans.update(local_month_plans)
        data = [
            [
                plan["date"],
                plan["subj"],
                plan["text"],
            ] for plan in online_month_plans.values() if plan['subj'] and plan['text']]
        ws = self.sh.worksheet("MonthPlans")
        ws.clear()
        ws.insert_rows(data)

        local_range_plans = self.range_plans()
        local_range_plans = {(plan['start'], plan['end'], plan['subj']): plan for plan in local_range_plans}
        online_range_plans = self.sh.worksheet("RangePlans").get_all_values()
        online_range_plans = {
            (plan[0], plan[1]): {
                "start": plan[0],
                "end": plan[1],
                "subj": plan[2],
                "text": plan[3],
            } for plan in online_range_plans}

        online_range_plans.update(local_range_plans)
        data = [
            [
                plan["start"],
                plan["end"],
                plan["subj"],
                plan["text"],
            ] for plan in online_range_plans.values() if plan['subj'] and plan['text']]
        ws = self.sh.worksheet("RangePlans")
        ws.clear()
        ws.insert_rows(data)
        self.upsert_plan({'months': list(online_month_plans.values()), 'ranges': list(online_range_plans.values())})


api = API()
