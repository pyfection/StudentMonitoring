

class Worksheet:
    records = []

    def get_all_records(self, head):
        return self.records

    def get(self, range_name):
        return self.records

    def append_row(self, data):
        self.records.append(data)

    @property
    def row_count(self):
        return len(self.records)


class Sheet:
    def worksheet(self, name):
        ws = Worksheet()
        if name == 'Students':
            ws.records = students
        elif name == 'Attendance':
            ws.records = attendance
        if name == 'Grades':
            ws.records = grades
        if name == 'Fees':
            ws.records = fees
        return ws


class Client:
    def open_by_url(self, link):
        return Sheet()


def authorize(credentials):
    return Client()


with open('mock_files/students.csv') as f:
    students = [line.split(';') for line in f.read().split('\n')]

with open('mock_files/attendance.csv') as f:
    attendance = [line.split(';') for line in f.read().split('\n')]

with open('mock_files/grades.csv') as f:
    grades = [line.split(';') for line in f.read().split('\n')]

with open('mock_files/fees.csv') as f:
    fees = [line.split(';') for line in f.read().split('\n')]
