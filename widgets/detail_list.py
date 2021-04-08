
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('widgets/detail_list.kv')


class DetailItem(BoxLayout):
    header = StringProperty()
    value = StringProperty()


class DetailList(ScreenManager):
    headers = ListProperty()
    ''' Example:
    ['Name', 'Phone', 'Email']
    '''
    data = ListProperty()
    ''' Example:
    [
        (('id', 'title'), ('Jon Doe', '4536565666', 'jon@doe.com'))
    ]
    '''

    def on_data(self, inst, data):
        self.ids.list.data = [
            {
                'text': entry[0][1],
                'size_hint': (1, None),
                'height': dp(50),
                'on_press': lambda id=entry[0][0]: self.show_detail(id)
            } for entry in data
        ]
        # self.ids.detail.data = [{'header': header, 'value': data[1][i]} for i, header in enumerate(self.headers)]

    def show_detail(self, id):
        entry = next(e for e in self.data if e[0][0] == id)
        self.ids.detail.title = entry[0][1]
        self.ids.detail.data = [
            {
                'header': header,
                'value': entry[1][i],
                'size_hint': (1, None),
                'height': dp(50),
            } for i, header in enumerate(self.headers)
        ]
        self.current = 'detail'
