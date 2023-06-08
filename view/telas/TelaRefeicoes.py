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

from view.componentes.CardRefeicao import CardRefeicao
from view.componentes.SeletorPagina import SeletorPagina
from view.componentes.InputPesquisa import InputPesquisa
from view.telas.TelaAdicionarRefeicao import TelaAdicionarRefeicao
from view.componentes.TelaCarregamento import TelaCarregamento
from controllers.refeicao_crud import *

CARDS_POR_TELA = 3

class TelaRefeicoesManager(MDScreenManager):
    def __init__(self, **kwargs):
        super(TelaRefeicoesManager, self).__init__(**kwargs)
        self.tela_adicionar_refeicoes = TelaAdicionarRefeicao(name="tela-add-refeicoes")
        self.tela_refeicoes = TelaRefeicoes(name="tela-refeicoes")
        self.add_widget(self.tela_refeicoes)
        self.add_widget(self.tela_adicionar_refeicoes)
    
    def troca_tela_refeicoes(self, atualizado):
        if atualizado:
            self.tela_refeicoes.criar_tela()
        self.current = 'tela-refeicoes'
    
    def troca_tela_addrefeicao(self, refeicao, atualizacao):
        if atualizacao:
            self.remove_widget(self.tela_adicionar_refeicoes)
            self.tela_adicionar_refeicoes = TelaAdicionarRefeicao(name="tela-add-refeicoes", atualizacao=True, refeicao=refeicao)
            self.add_widget(self.tela_adicionar_refeicoes)
            self.current = 'tela-add-refeicoes'
        elif self.tela_adicionar_refeicoes.refeicao == None: 
            self.current = 'tela-add-refeicoes'     
        else: 
            self.remove_widget(self.tela_adicionar_refeicoes)
            self.tela_adicionar_refeicoes = TelaAdicionarRefeicao(name="tela-add-refeicoes")
            self.add_widget(self.tela_adicionar_refeicoes)
            self.current = 'tela-add-refeicoes'
            

class TelaRefeicoes(MDScreen):
    def __init__(self, **kwargs):
        super(TelaRefeicoes, self).__init__(**kwargs)
        self.total_pages = math.ceil(quantidade_refeicoes()/CARDS_POR_TELA) 
        self.pagina_atual = 1
        self.busca=False
        self.criar_tela()
    

    def tela_adicionar_refeicao(self, *args):
        """Chama a tela de formulario para adicionar alimento"""
        self.manager.troca_tela_addrefeicao(args[0], args[1])
    
    def retornar_a_tela(self, *args, refeicao=None, atualizacao=False):
        """Essa funcao serve para passar de argumento as telas que
            forem chamadas a partir dessa classe
        """
        self.clear_widgets() 
        self.add_widget(TelaCarregamento())
        Clock.schedule_once(self.criar_tela)

    def pesquisa(self, *args):
        nome_refeicao = args[0]
        if nome_refeicao == '':
            self.busca=False
            self.pagina_atual = 1
            self.clear_widgets()
            self.add_widget(TelaCarregamento())
            Clock.schedule_once(self.criar_tela)
            return 
        refeicao = busca_refeicoes(nome_refeicao) 
        if refeicao:
            self.total_pages = math.ceil(len(refeicao)/10) 
            self.pagina_atual = 1
            self.busca=refeicao
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
        botao_adicionar = MDRectangleFlatIconButton(icon="plus", text="Adicionar nova refeicao")
        botao_adicionar.bind(on_release=partial(self.tela_adicionar_refeicao, None, False))
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
            self.gera_refeicoes(items)
            self.total_pages = math.ceil(quantidade_refeicoes()/CARDS_POR_TELA) 
        else:
            i = (self.pagina_atual-1)*CARDS_POR_TELA
            elementos = 0
            while i < len(self.busca):
                if elementos == CARDS_POR_TELA:
                    break
                items.add_widget(CardRefeicao(objeto=self.busca[i]))
                
                elementos+=1
                i+=1
        
        scroll.add_widget(items)
        self.add_widget(scroll)
    
    def gera_refeicoes(self, items):
        refeicoes = ler_refeicoes(paginacao=True, items_por_pagina=CARDS_POR_TELA ,pagina=self.pagina_atual)
        for refeicao in refeicoes:
            items.add_widget(CardRefeicao(objeto = refeicao))