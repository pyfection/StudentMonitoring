

PATHS = {
    'Students': 'mock_files/students.csv',
    'Teachers': 'mock_files/teachers.csv',
    'Attendance': 'mock_files/attendance.csv',
    'Grades': 'mock_files/grades.csv',
    'Fees': 'mock_files/fees.csv',
    'MonthPlans': 'mock_files/month_plans.csv',
    'RangePlans': 'mock_files/range_plans.csv',
    'Holidays': 'mock_files/holidays.csv',
}


class Worksheet:
    records = []

    def __init__(self, name):
        self.name = name
        self.reload()

    def reload(self):
        with open(PATHS[self.name]) as f:
            self.records = [line.split(';') for line in f.read().split('\n')]

    def get_all_values(self):
        return self.records

    def get(self, range_name):
        return self.records

    def append_row(self, data):
        self.records.append(data)

    def insert_rows(self, rows, row=1):
        self.records = self.records[:row-1] + rows + self.records[row-1:]
        with open(PATHS[self.name], 'w') as f:
            f.write('\n'.join(';'.join(row) for row in self.records))

    def row_values(self, row):
        return self.records[row]

    @property
    def row_count(self):
        return len(self.records)

    def clear(self):
        self.records.clear()
        with open(PATHS[self.name], 'w') as f:
            pass  # Clear


class Sheet:
    def worksheet(self, name):
        ws = Worksheet(name)
        return ws


class Client:
    def open_by_key(self, key):
        return Sheet()


def authorize(credentials):
    return Client()
