from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton

class TelaCarregamento(FloatLayout):
    def __init__(self, **kwargs):
        super(TelaCarregamento, self).__init__(**kwargs)
        self.add_widget(MDIconButton(icon='refresh', pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.add_widget(MDLabel(text="Carregando", halign="center", valign="middle", pos_hint={'center_x': 0.5, 'center_y': 0.4}))