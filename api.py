
import gspread_mock as gspread
from google.oauth2.service_account import Credentials


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
        ws = self.sh.worksheet("Teachers")
        values = [email, first_name, last_name]
        for i in range(ws.row_count):
            if ws.row_values(i) == values:
                break
        else:
            ws.append_row(values)
        self.teacher = email
        return True

    def holidays(self):
        ws = self.sh.worksheet("Holidays")
        holidays = ws.get(f'A2:B{ws.row_count - 1}')
        return {key: value for key, value in holidays}

    def students(self):
        ws = self.sh.worksheet("Students")
        students = ws.get(f'A2:P{ws.row_count-1}')
        return [{
            "id": student[0],
            "student_name": student[1],
            'joining_date': student[2],
            "group": student[3],
            "name_father": student[4],
            "name_mother": student[5],
            "address": student[6],
            "phone_number_mother": student[7],
            "phone_number_father": student[8],
            "dob": student[9],
            "aadhar_card_number": student[10],
            "official_class": student[11],
            "goes_goverment_school": student[12],
            "occupation_mother": student[13],
            "occupation_father": student[14],
            "status": student[15],
            "teacher": student[16],
            "comment": student[17],
        } for student in students if student[16] == self.teacher]

    def teachers(self):
        ws = self.sh.worksheet("Teachers")
        teachers = ws.get(f'A2:D{ws.row_count-1}')
        return [{
            'email': teacher[0],
            'first_name': teacher[1],
            'last_name': teacher[2],
        } for teacher in teachers]

    def attendance(self):
        ws = self.sh.worksheet("Attendance")
        attendance = ws.get(f'A2:C{ws.row_count-1}')
        return [{
            'student_id': att[0],
            'date': att[1],
            'status': att[2],
        } for att in attendance]

    def fees(self):
        ws = self.sh.worksheet("Fees")
        fees = ws.get(f'A2:E{ws.row_count-1}')
        return [{
            'student_id': fee[0],
            'date': fee[1],
            'amount': fee[2],
            'receipt': fee[3],
            'books': fee[4],
        } for fee in fees]

    def grades(self):
        ws = self.sh.worksheet("Grades")
        grades = ws.get(f'A2:F{ws.row_count-1}')
        return [{
            'student_id': grade[0],
            'date': grade[1],
            'gtype': grade[2],
            'math': grade[3],
            'english': grade[4],
            'hindi': grade[5],
        } for grade in grades]

    def range_plans(self):
        # ToDo: to be implemented
        ws = self.sh.worksheet("RangePlans")
        range_plans = ws.get(f'A2:R{ws.row_count-1}')

    def month_plans(self):
        # ToDo: to be implemented
        ws = self.sh.worksheet("MonthPlans")
        month_plans = ws.get(f'A2:R{ws.row_count-1}')

    def add_student(self, *data):
        data = list(data)
        data.insert(-1, self.teacher)
        ws = self.sh.worksheet("Students")
        i = ws.row_count + 1
        ws.append_row([str(i)] + data)


api = API()
