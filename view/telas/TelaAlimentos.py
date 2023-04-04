from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.widget import MDWidget
from kivy.uix.label import Label
from kivy.clock import Clock

import time
import math
import sys
from functools import partial
sys.path.append("../../")


from view.componentes.CardAlimento import CardAlimento
from view.componentes.SeletorPagina import SeletorPagina
from view.componentes.InputPesquisa import InputPesquisa
from view.componentes.TelaCarregamento import TelaCarregamento
from view.colors_definitions import ERROR_COLOR
from controllers.alimento_crud import *

class TelaAlimentos(MDScreen):
    def __init__(self, **kwargs):
        super(TelaAlimentos, self).__init__(**kwargs)
        self.total_pages = math.ceil(quantidade_alimentos()/10) 
        self.pagina_atual = 1
        self.busca=False
        self.criar_tela()
       
        
    def gera_alimentos(self, items):
        alimentos = ler_alimentos(paginacao=True, pagina=self.pagina_atual)
        for alimento in alimentos:
            items.add_widget(CardAlimento(objeto = alimento))
    
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
        


    def pesquisa(self, *args):
        nome_alimento = args[0]
        if nome_alimento == '':
            self.busca=False
            self.pagina_atual = 1
            self.clear_widgets()
            self.add_widget(TelaCarregamento())
            Clock.schedule_once(self.criar_tela)
            return 
        alimento = busca_alimentos(nome_alimento) 
        if alimento:
            self.total_pages = math.ceil(len(alimento)/10) 
            self.pagina_atual = 1
            self.busca=alimento
            self.clear_widgets()
            self.add_widget(TelaCarregamento())
            Clock.schedule_once(self.criar_tela)
        else:
            self.clear_widgets()
            self.add_widget(TelaCarregamento())
            Clock.schedule_once(partial(self.criar_tela, True))

    def criar_tela(self,*args):

        #Containers
        items = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        
        
        #Busca os alimentos e cria os cards
        scroll = MDScrollView()
        items.bind(minimum_height=items.setter("height"))

        #Botao adicionar novos alimentos
        botao_adicionar = MDRectangleFlatIconButton(icon="plus", text="Adicionar novo alimento")
        items.add_widget(botao_adicionar)

        barra_pesquisa = InputPesquisa("Pesquisar alimento...",search_callback=self.pesquisa)
        items.add_widget(barra_pesquisa)

        if args:
            if args[0] == True:
                items.add_widget(Label(text="Alimento não encontrado", color=ERROR_COLOR))

        if self.busca:
            self.total_pages = math.ceil(len(self.busca)/10)
        else:
            self.total_pages = math.ceil(quantidade_alimentos()/10) 

        items.add_widget(
            SeletorPagina(
                total_pages=self.total_pages, 
                current_page= self.pagina_atual,
                visible_pages=[self.pagina_atual, self.pagina_atual+1], 
            ))
        items.add_widget(MDWidget(height=50))
        if not self.busca:
            self.gera_alimentos(items)
        else:
            i = (self.pagina_atual-1)*10
            elementos = 0
            while i < len(self.busca):
                if elementos == 10:
                    break
                items.add_widget(CardAlimento(objeto=self.busca[i]))
                
                elementos+=1
                i+=1
                
        scroll.add_widget(items)
        self.clear_widgets()
        self.add_widget(scroll)