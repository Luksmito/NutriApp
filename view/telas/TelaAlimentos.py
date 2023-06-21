"""
Tela que mostra os alimentos cadastrados
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.widget import MDWidget
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.textfield import MDTextField
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
from view.telas.TelaAdicionarAlimento import TelaAdicionarAlimento
from view.colors_definitions import ERROR_COLOR, PRIMARY_COLOR
from controllers.alimento_crud import *

CARDS_POR_TELA = 3
class TelaAlimentosManager(MDScreenManager):
    def __init__(self, **kwargs):
        super(TelaAlimentosManager, self).__init__(**kwargs)
        self.add_widget(TelaAlimentos(name="tela-alimentos"))
        self.add_widget(TelaAdicionarAlimento(name="tela-add-alimentos"))
        

class TelaAlimentos(MDScreen):
    def __init__(self, **kwargs):
        super(TelaAlimentos, self).__init__(**kwargs)
        self.total_pages = math.ceil(quantidade_alimentos()/CARDS_POR_TELA) 
        self.pagina_atual = 1
        self.busca=False
        self.criar_tela()
       
        
    def gera_alimentos(self, items):
        """
        Busca os alimentos no banco de dados e adiciona os cards no item passado por argumento
        Args:
            items (Widget): recebe um widget que vai conter os cards de alimento
        """
        alimentos = ler_alimentos(paginacao=True, items_por_pagina=CARDS_POR_TELA ,pagina=self.pagina_atual)
        for alimento in alimentos:
            items.add_widget(CardAlimento(objeto = alimento))
    
    def proxima_pagina(self):
        """
        Lida com a funcionalidade de ir para a próxima página
        """
        #Se estiver na última pagina não faz nada
        if self.pagina_atual == self.total_pages:
            return
        
        self.pagina_atual += 1
        self.clear_widgets()
        
        self.add_widget(TelaCarregamento())
        Clock.schedule_once(self.criar_tela)
    
    def pagina_anterior(self):
        """
        Lida com a logica para ir para a pagina anterior
        """
        if self.pagina_atual == 1:
            return
        self.pagina_atual -= 1
        self.clear_widgets() 
        self.add_widget(TelaCarregamento())
        Clock.schedule_once(self.criar_tela)
    

    def pesquisa(self, *args):
        """
        Busca o alimento no banco de dados e chama as funcoes para criar a tela
        dependendo do resultado da pesquisa

        Args:
            args[0] (str): Nome do alimento a ser buscado no banco de dados  
        """
        nome_alimento = args[0]
        #Se o nome pesquisado for uma string vazia retorna a busca completa
        #de todos os alimentos
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

    def tela_adicionar_alimento(self, *args):
        """Chama a tela de formulario para adicionar alimento"""
        self.manager.current = 'tela-add-alimentos'

    def retornar_a_tela(self, *args):
        """Essa funcao serve para passar de argumento as telas que
            forem chamadas a partir dessa classe
        """
        self.clear_widgets() 
        self.add_widget(TelaCarregamento())
        Clock.schedule_once(self.criar_tela)

    

    def criar_tela(self,*args):
        """
        Funcao que renderiza a tela
        Args:
            args[0] (bool): True se a busca deu certo, senão False
        """
        #Containers
        items = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        
        
        #Busca os alimentos e cria os cards
        scroll = MDScrollView()
        items.bind(minimum_height=items.setter("height"))

        #Botao adicionar novos alimentos
        botao_adicionar = MDRectangleFlatIconButton(icon="plus", text="Adicionar novo alimento")
        botao_adicionar.bind(on_release=self.tela_adicionar_alimento)
        items.add_widget(botao_adicionar)

        barra_pesquisa = InputPesquisa("Pesquisar alimento...",search_callback=self.pesquisa)
        items.add_widget(barra_pesquisa)

        if args:
            if args[0] == True:
                items.add_widget(Label(text="Alimento não encontrado", color=ERROR_COLOR))

        if self.busca:
            self.total_pages = math.ceil(len(self.busca)/CARDS_POR_TELA)
        else:
            self.total_pages = math.ceil(quantidade_alimentos()/CARDS_POR_TELA) 

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
            i = (self.pagina_atual-1)*CARDS_POR_TELA
            elementos = 0
            while i < len(self.busca):
                if elementos == CARDS_POR_TELA:
                    break
                items.add_widget(CardAlimento(objeto=self.busca[i]))
                
                elementos+=1
                i+=1
                
        scroll.add_widget(items)
        self.clear_widgets()
        self.add_widget(scroll)