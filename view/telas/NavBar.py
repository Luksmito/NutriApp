from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.screen import MDScreen

import sys
sys.path.append("../../")

from view.colors_definitions import *
from view.telas.TelaAlimentos import TelaAlimentos
from view.telas.TelaRefeicoes import TelaRefeicoes

KV = """
MDBottomNavigation:
    
"""
from kivymd.uix.screenmanager import MDScreenManager

class MyScreenManager(MDScreenManager):
    pass

class NavBar(MDFloatLayout, FakeRectangularElevationBehavior):
    def __init__(self, manager=None, **kwargs):
        super(NavBar,self).__init__(**kwargs)
        self.manager = manager
        self.elevation = 10
        #Cria a barra de navegação de baixo
        self.nav = Builder.load_string(KV)
        self.nav.panel_color = PRIMARY_COLOR
        self.nav.text_color_normal = TEXT_COLOR_2
        sm = MyScreenManager()

        #Cria os itens da barra de navegação
        self.dieta_nav = MDBottomNavigationItem(
            name="tela-dieta", 
            text="Dietas",
            icon="nutrition"
        )
        self.refeicao_nav = MDBottomNavigationItem(
            TelaRefeicoes(),
            name="tela-refeicao", 
            text="Refeições",
            icon="silverware-fork-knife"
        )
        self.alimento_nav = MDBottomNavigationItem(
            TelaAlimentos(),
            name="tela-alimento", 
            text="Alimentos",
            icon="food-apple"
        )
        self.alimento_nav.bind(on_tab_press=self.tela_alimentos)
        #Adiciona os itens a barra
        self.nav.add_widget(self.dieta_nav)
        self.nav.add_widget(self.refeicao_nav)
        self.nav.add_widget(self.alimento_nav)
        #self.nav.add_widget(MDScreen(name="nome"))
        #Adiciona a barra a tela
        self.add_widget(self.nav)

    def tela_alimentos(self, *args):
        pass