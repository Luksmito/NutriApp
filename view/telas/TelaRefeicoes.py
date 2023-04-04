from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRectangleFlatIconButton


import sys
sys.path.append("../../")

from view.componentes.CardRefeicao import CardRefeicao
from controllers.refeicao_crud import *

class TelaRefeicoes(MDScreen):
    def __init__(self, **kwargs):
        super(TelaRefeicoes, self).__init__(**kwargs)

        #Containers
        self.scroll = MDScrollView()
        self.items = MDGridLayout(cols=1,size_hint_y=None, padding=[15,15,15,15], spacing=20)
        self.items.bind(minimum_height=self.items.setter("height"))
        
        #Botao adicionar novos alimentos
        self.botao_adicionar = MDRectangleFlatIconButton(icon="plus", text="Adicionar nova refeicao")
        self.items.add_widget(self.botao_adicionar)
        
        #Busca os alimentos e cria os cards
        self.gera_refeicoes()
        
        self.scroll.add_widget(self.items)
        self.add_widget(self.scroll)
        
    def gera_refeicoes(self):
        refeicoes = ler_refeicoes()
        for refeicao in refeicoes:
            self.items.add_widget(CardRefeicao(objeto = refeicao))