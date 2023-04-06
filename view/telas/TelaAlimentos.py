from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.widget import MDWidget
from kivymd.uix.label import MDLabel
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
from view.colors_definitions import ERROR_COLOR, PRIMARY_COLOR
from controllers.alimento_crud import *

CARDS_POR_TELA = 7

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

    def tela_adicionar_alimento(self, *args):
        
        self.clear_widgets()
        
        items = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        
        scroll = MDScrollView()
        
        items.bind(minimum_height=items.setter("height"))
        
        botao_volta = MDRectangleFlatIconButton(icon="arrow-left", text="voltar")
        botao_volta.bind(on_release=self.criar_tela)
        
        items.add_widget(botao_volta)
        
        items.add_widget(MDLabel(
            text="Algumas dicas: O único atributo obrigatório é o nome, adicione apenas os que forem relevantes para você,\
 se não souber alguma informação sobre o alimento você pode pesquisar no google ou no endereço: https://vitat.com.br/alimentacao/busca-de-alimentos\
 as informações fornecidas aqui serão utilizadas no cálculo da dieta", height=200))

        nome_input = MDTextField(hint_text="Nome do alimento", required=True)
        descricao = MDTextField(hint_text="Descrição do alimento (opcional)")
        
        calorias_por_grama = MDTextField(hint_text="Calorias por grama do alimento (opcional)")
        calorias_por_ml = MDTextField(hint_text="Calorias por ml do alimento (opcional)")
        calorias_por_colher = MDTextField(hint_text="Calorias por colher do alimento (opcional)")

        proteinas_por_grama = MDTextField(hint_text="Proteínas por grama (opcional)")
        proteinas_por_colher = MDTextField(hint_text="Proteínas por colher (opcional)")
        proteinas_por_ml = MDTextField(hint_text="Proteínas por ml (opcional)")
        
        carboidratos_por_grama = MDTextField(hint_text="Carboídratos por grama (opcional)")
        carboidratos_por_colher = MDTextField(hint_text="Carboídratos por colher (opcional)")
        carboidratos_por_ml = MDTextField(hint_text="Carboídratos por ml (opcional)")
        
        gorduras_por_grama = MDTextField(hint_text="Gorduras por grama (opcional)")
        gorduras_por_colher = MDTextField(hint_text="Gorduras por colher (opcional)")
        gorduras_por_ml = MDTextField(hint_text="Gorduras por ml (opcional)")
        
        label_erros = MDLabel(text="", color=ERROR_COLOR)

        botao_submeter = MDRectangleFlatIconButton(icon="plus", text="Adicionar")
        botao_submeter.bind(
            on_release=lambda _:self.criar_alimento(
                nome=nome_input.text,
                descricao=descricao.text,
                calorias_por_grama=calorias_por_grama.text,
                calorias_por_colher=calorias_por_colher.text,
                calorias_por_ml=calorias_por_ml.text,
                proteinas_por_grama=proteinas_por_grama.text,
                proteinas_por_colher=proteinas_por_colher.text,
                proteinas_por_ml=proteinas_por_ml.text,
                carboidratos_por_grama=carboidratos_por_grama.text,
                carboidratos_por_colher=carboidratos_por_colher.text,
                carboidratos_por_ml=carboidratos_por_ml.text,
                gorduras_por_grama=gorduras_por_grama.text,
                gorduras_por_colher=gorduras_por_colher.text,
                gorduras_por_ml=gorduras_por_ml.text,
                erros=label_erros
            ))

        items.add_widget(nome_input)
        items.add_widget(descricao)
        items.add_widget(calorias_por_grama)
        items.add_widget(calorias_por_colher)
        items.add_widget(calorias_por_ml)
        items.add_widget(proteinas_por_grama)
        items.add_widget(proteinas_por_colher)
        items.add_widget(proteinas_por_ml)
        items.add_widget(carboidratos_por_grama)
        items.add_widget(carboidratos_por_colher)
        items.add_widget(carboidratos_por_ml)
        items.add_widget(gorduras_por_grama)
        items.add_widget(gorduras_por_colher)
        items.add_widget(gorduras_por_ml)    
        items.add_widget(botao_submeter)
        items.add_widget(label_erros)

        scroll.add_widget(items)
        self.add_widget(scroll)
    
    def is_float(self,string):
        try:
            string = string.replace(',', '.')
            float(string)
            return True
        except ValueError:
            return False
        
    def criar_alimento(self,**kwargs):
        erros = kwargs.pop("erros")
        erros.text = ""
        erros.color = ERROR_COLOR
        for chave, valor in kwargs.items():
            if chave == "nome" or chave == "descricao":
                continue
            if valor is not "":
                if not self.is_float(valor):
                    nome_campo = chave.replace('_', " ")
                    erros.text += f"{nome_campo} deve ser um numero\n"
                else:
                    kwargs[chave] = float(kwargs[chave])
            else:
                kwargs[chave] = None
        resposta = criar_alimento(kwargs)
        if resposta is True:
            erros.color = PRIMARY_COLOR
            erros.text = "Alimento adicionado com sucesso!"
        else:
            erros.text = "Alimento com esse nome já cadastrado"

    def criar_tela(self,*args):

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