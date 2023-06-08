from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton

class InputPesquisa(MDGridLayout):
    search_callback = ObjectProperty(None)

    def __init__(self,mensagem="", **kwargs):
        super(InputPesquisa, self).__init__(**kwargs)
        self.orientation = "lr-tb"
        self.rows=2
        self.cols=2
        self.size_hint_y = None
        self.search_input = MDTextField(
            hint_text=mensagem,
            size_hint=(0.9, 1),
            mode="round"
        )
        self.botao_pesquisa = MDIconButton(icon="magnify")
        self.botao_pesquisa.bind(on_release=self._trigger_search)

        self.add_widget(self.search_input)
        self.add_widget(self.botao_pesquisa)
    

    def _trigger_search(self, *args):
        if self.search_callback:
            self.search_callback(self.search_input.text)

    def clear_search(self):
        self.search_input.text = ''