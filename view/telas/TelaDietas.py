from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.widget import MDWidget
from kivymd.uix.screenmanager import MDScreenManager
from kivy.clock import Clock

import math
import sys
from functools import partial
sys.path.append("../../")

from view.componentes.CardDieta import CardDieta
from view.componentes.SeletorPagina import SeletorPagina
from view.componentes.InputPesquisa import InputPesquisa
from view.telas.TelaAdicionarDieta import TelaAdicionarDieta
from view.componentes.TelaCarregamento import TelaCarregamento
from controllers.dieta_crud import *

CARDS_POR_TELA = 3


class TelaDietasManager(MDScreenManager):
    def __init__(self, **kwargs):
        super(TelaDietasManager, self).__init__(**kwargs)
        self.tela_adicionar_dietas = TelaAdicionarDieta(name="tela-add-dietas")
        self.add_widget(TelaDietas(name="tela-dietas"))
        self.add_widget(self.tela_adicionar_dietas)
        self.on_start()
    
    def troca_tela(self, dieta, atualizacao):
        if atualizacao:
            self.remove_widget(self.tela_adicionar_dietas)
            self.tela_adicionar_dietas = TelaAdicionarDieta(name="tela-add-dietas", atualizacao=True, dieta=dieta)
            self.add_widget(self.tela_adicionar_dietas)
            self.current = 'tela-add-dietas'
        elif self.tela_adicionar_dietas.dieta == None: 
            self.current = 'tela-add-dietas'     
        else: 
            self.remove_widget(self.tela_adicionar_dietas)
            self.tela_adicionar_dietas = TelaAdicionarDieta(name="tela-add-dietas")
            self.add_widget(self.tela_adicionar_dietas)
            self.current = 'tela-add-dietas'
            
    
    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            self.current = 'tela-dietas'
        else:
            return False
        
    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.key_input)
        
class TelaDietas(MDScreen):
    def __init__(self, **kwargs):
        super(TelaDietas, self).__init__(**kwargs)
        self.total_pages = math.ceil(quantidade_dietas()/CARDS_POR_TELA) 
        self.pagina_atual = 1
        self.busca=False
        self.criar_tela()
    

    def tela_adicionar_dieta(self, *args):
        """Chama a tela de formulario para adicionar alimento"""
        self.manager.troca_tela(args[0], args[1])
        
    

    def pesquisa(self, *args):
        nome_dieta = args[0]
        if nome_dieta == '':
            self.busca=False
            self.pagina_atual = 1
            self.clear_widgets()
            self.add_widget(TelaCarregamento())
            Clock.schedule_once(self.criar_tela)
            return 
        dieta = busca_dietas(nome_dieta) 
        if dieta:
            self.total_pages = math.ceil(len(dieta)/10) 
            self.pagina_atual = 1
            self.busca=dieta
            self.clear_widgets()
            self.add_widget(TelaCarregamento())
            Clock.schedule_once(self.criar_tela)
        else:
            self.clear_widgets()
            self.add_widget(TelaCarregamento())
            Clock.schedule_once(partial(self.criar_tela, True))

    def proxima_pagina(self):
        if self.pagina_atual == self.total_pages:
            return
        self.pagina_atual += 1
        self.clear_widgets()
        self.add_widget(TelaCarregamento())
        Clock.schedule_once(self.criar_tela)
    
    def pagina_anterior(self):
        if self.pagina_atual == 1:
            return
        self.pagina_atual -= 1
        self.clear_widgets() 
        self.add_widget(TelaCarregamento())
        Clock.schedule_once(self.criar_tela)
        

    def criar_tela(self, *args):
        #Containers
        scroll = MDScrollView()
        items = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        items.bind(minimum_height=items.setter("height"))
        
        #Botao adicionar novos alimentos
        botao_adicionar = MDRectangleFlatIconButton(icon="plus", text="Adicionar nova dieta")
        botao_adicionar.bind(on_release=partial(self.tela_adicionar_dieta, None, False))
        items.add_widget(botao_adicionar)
        
        barra_pesquisa = InputPesquisa("Pesquisar refeição...",search_callback=self.pesquisa)
        items.add_widget(barra_pesquisa)

        items.add_widget(
            SeletorPagina(
                total_pages=self.total_pages, 
                current_page= self.pagina_atual,
                visible_pages=[self.pagina_atual, self.pagina_atual+1], 
            ))
        self.clear_widgets()

        #Busca as refeicoes e cria os cards
        items.add_widget(MDWidget(height=50))
        if not self.busca:
            self.gera_dietas(items)
            self.total_pages = math.ceil(quantidade_dietas()/CARDS_POR_TELA) 
        else:
            i = (self.pagina_atual-1)*CARDS_POR_TELA
            elementos = 0
            while i < len(self.busca):
                if elementos == CARDS_POR_TELA:
                    break
                items.add_widget(CardDieta(objeto=self.busca[i]))
                
                elementos+=1
                i+=1
        
        scroll.add_widget(items)
        self.add_widget(scroll)
    
    def gera_dietas(self, items):
        dietas = ler_dietas(paginacao=True, items_por_pagina=CARDS_POR_TELA ,pagina=self.pagina_atual)
        for dieta in dietas:
            items.add_widget(CardDieta(objeto = dieta))