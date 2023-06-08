from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.screenmanager import MDScreenManager
from kivy.clock import Clock

import sys
sys.path.append("../../")

from view.colors_definitions import *
from view.telas.TelaAlimentos import TelaAlimentosManager
from view.telas.TelaRefeicoes import TelaRefeicoesManager
from view.telas.TelaDietas import TelaDietasManager
from view.componentes.TelaCarregamento import TelaCarregamento

KV = """
MDBottomNavigation:
    
"""

class NavBar(MDFloatLayout, FakeRectangularElevationBehavior):
    def __init__(self, manager=None, **kwargs):
        super(NavBar,self).__init__(**kwargs)
        self.elevation = 10
        self._criar_tela()
    
    def _criar_tela(self):
        self.clear_widgets()
        self.add_widget(TelaCarregamento())
        Clock.schedule_once(self.criar_tela)
        
    def criar_tela(self, *args):
        self.clear_widgets()
        #Cria a barra de navegação de baixo
        self.nav = Builder.load_string(KV)
        self.nav.panel_color = PRIMARY_COLOR
        self.nav.text_color_normal = TEXT_COLOR_2

        #Cria os itens da barra de navegação
        self.dieta_nav = MDBottomNavigationItem(
            TelaDietasManager(),
            name="tela-dieta", 
            text="Dietas",
            icon="nutrition"
        )
        self.refeicao_nav = MDBottomNavigationItem(
            TelaRefeicoesManager(),
            name="tela-refeicao", 
            text="Refeições",
            icon="silverware-fork-knife"
        )
        self.alimento_nav = MDBottomNavigationItem(
            TelaAlimentosManager(),
            name="tela-alimento", 
            text="Alimentos",
            icon="food-apple"
        )
        self.alimento_nav.bind(on_tab_press=self.tela_alimentos)
        #Adiciona os itens a barra
        self.nav.add_widget(self.dieta_nav)
        self.nav.add_widget(self.refeicao_nav)
        self.nav.add_widget(self.alimento_nav)
        
        #Adiciona a barra a tela
       
        self.add_widget(self.nav)
   
        
    def tela_alimentos(self, *args):
        pass