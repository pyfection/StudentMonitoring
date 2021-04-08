
from kivy.clock import Clock
from kivymd.uix.datatables import MDDataTable


class DataTable(MDDataTable):
    def on_row_data(self, inst, data):
        print(inst, data)
        self.table_data.row_data = data
        self.table_data.on_rows_num(None, self.table_data.rows_num)
        self.table_data.set_next_row_data_parts('reset')
