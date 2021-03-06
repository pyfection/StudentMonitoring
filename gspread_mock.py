

class Worksheet:
    def get_all_records(self, head):
        return __TEST_STUDENTS

    def get(self, range_name):
        return _TEST_STUDENTS

    def append_row(self, data):
        _TEST_STUDENTS.append(data)

    @property
    def row_count(self):
        return len(_TEST_STUDENTS)


class Sheet:
    def worksheet(self, name):
        return Worksheet()


class Client:
    def open_by_url(self, link):
        return Sheet()


def authorize(credentials):
    return Client()


_TEST_STUDENTS = [
    [1, "Aizah Shahid", "Oct 13, 2020", "1 A", "Mohd Saheed", "Farzana Khatoon", "M block52", "7543992278", "", "April 30, 2015", "209002752202", "1", "0", "Housewife", "Factory worker", "", "", "", ""],
    [2, "Jaishu", "Oct 14, 2020", "1 A", "Manoj", "Reena", "WZ-92", "9873733297", "", "Sep 23, 2015", "", "1", "0", "Housewife", "Shopkeeper", "", "", "", ""],
    [3, "yash", "Oct 14, 2020", "1 A", "Durgesh kumar", "Chandni singh", "WZ-9 A", "8010905280", "7834963592", "Apr 4, 2015", "346069723512", "1", "0", "Housewife", "Electrician", "", "", "", ""],
    [4, "Niharika OL", "Oct 14, 2020", "1 A", "Santosh kumar", "Suman", "M-66", "8860147896", "9582531145", "Sep 29, 2014", "218374994306", "1", "0", "Housewife", "", "", "", "", ""],
    [5, "Monu", "Oct 14, 2020", "1 A", "Ram Gopal", "Mamta", "", "8860379021", "", "Jun 11, 2014", "NO", "1", "0", "Factory worker", "vegetable/fruit seller", "", "", "", ""],
    [6, "Anshuman", "Oct 14, 2020", "1 A", "Ajeet Kumar", "Gayatri", "wz179", "9918456281", "7292012739", "Mar 25, 2015", "888658899296", "1", "0", "Factory worker", "Factory worker", "", "", "", ""],
]
