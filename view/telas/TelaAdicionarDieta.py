from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.screen import MDScreen

import sys
from functools import partial
sys.path.append("../../")

from view.componentes.InputPesquisa import InputPesquisa
from view.componentes.CardRefeicao import CardRefeicao
from view.colors_definitions import ERROR_COLOR, PRIMARY_COLOR
from controllers.refeicao_crud import *
from controllers.dieta_crud import *


class EscolhaQuantidade(MDGridLayout):
    """
    Classe que contém os elementos de escolha de quantidade
    """
    def __init__(self,texto="texto",funcao_callback=None,**kwargs):
        super(EscolhaQuantidade, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.value = texto
        self.caixa = MDCheckbox(group="quantidades")
        self.caixa.bind(on_active=funcao_callback)
        self.add_widget(self.caixa)
        self.add_widget(MDLabel(text=texto))


class TelaAdicionarDieta(MDScreen):
    def __init__(self,atualizacao=False,dieta=None,**kwargs):
        super(TelaAdicionarDieta,self).__init__(**kwargs)
        self.calorias_novas = None
        self.refeicoes_adicionados_widgets = None
        self.atualizacao = atualizacao
        self.dieta = dieta
        self.refeicoes_adicionados = list()
        self.tipo_quantidade = None
        self.label_proteinas = None
        self.label_calorias = None
        self.label_gorduras = None
        self.label_carboidratos = None
        self.items = None
        self.barra_pesquisa_label = None
        self.scroll = None
        self.botao_volta = None
        self.nome_input = None
        self.descricao = None
        self.adicionar_refeicoes = None
        self.barra_pesquisa = None
        self.container_quantidade = None
        self.quantidade = None
        self.colheres = None
        self.gramas = None
        self.mls = None
        self.botao_add_refeicao = None
        self.refeicao = None
        self.espaco_refeicao = None
        self.calorias_totais = 0
        self.gorduras_totais = 0
        self.proteinas_totais = 0
        self.carboidratos_totais = 0
        self.criar_tela()
        self.atualizado = False
        
    def set_quantidade(self, checkbox,value):
        print(checkbox)

    def criar_dieta_db(self,*args):
        if not self.atualizacao:
            dieta = {
                "nome": self.nome_input.text,
                "descricao": self.descricao.text
            }
            resposta = criar_dieta(dieta)
        else:
            resposta = True

        if resposta == True:
            if not self.atualizacao:
                dieta = ler_dieta(dieta["nome"])
            else:
                dieta=self.dieta
                self.atualizado = True
            for refeicao in self.refeicoes_adicionados:
                add_refeicao(refeicao, dieta)    
            calcula_informacoes_nutricionais(dieta)
            self.label_erros.text = "Dieta criada com sucesso"
            self.label_erros.color = PRIMARY_COLOR
        else: 
            self.label_erros.text = "Dieta com esse nome já cadastrada"
            self.label_erros.color = ERROR_COLOR
    
    def calcula_calorias_totais(self):
        self.calorias_totais = 0
        self.gorduras_totais = 0
        self.proteinas_totais = 0
        self.carboidratos_totais = 0
        
        for refeicao in self.refeicoes_adicionados:
            if refeicao.calorias_totais is not None:
                self.calorias_totais += refeicao.calorias_totais
            if refeicao.gorduras_totais is not None:
                self.gorduras_totais += refeicao.gorduras_totais
            if refeicao.proteinas_totais is not None:
                self.proteinas_totais += refeicao.proteinas_totais
            if refeicao.carboidratos_totais is not None:
                self.carboidratos_totais += refeicao.carboidratos_totais
        
        self.label_calorias.text = "Calorias: " + f"{self.calorias_totais:.2f}"
        self.label_carboidratos.text = "Carboidratos: " + f"{self.carboidratos_totais:.2f}"
        self.label_gorduras.text = "Gorduras: " + f"{self.gorduras_totais:.2f}"
        self.label_proteinas.text = "Proteinas: " + f"{self.proteinas_totais:.2f}"
      
    def add_refeicao(self,*args):
        if self.refeicao == None:
            self.label_erros.text = "Busque uma refeição para adicionar"
            self.label_erros.color = ERROR_COLOR
            return
        self.refeicoes_adicionados.append(self.refeicao)
        self.calcula_calorias_totais()
        self.refeicoes_adicionados_widgets.add_widget(CardRefeicao(objeto=self.refeicao, mostrar_delete=True, mostrar_edit=False, deletar_do_banco=False))
        

    def funcao_retorno(self,*args):
        if self.atualizacao and not self.atualizado:
            self.criar_dieta_db()
        
        self.manager.current = 'tela-dietas'
    
    def is_float(self,string):
        """Função para verificar se um string é um float"""
        try:
            string = string.replace(',', '.')
            float(string)
            return True
        except:
            return False
        
    def remover_refeicao(self,nome):
        for refeicao in self.refeicoes_adicionados:
            if refeicao.nome == nome:
                self.refeicoes_adicionados.remove(refeicao)
        self.calcula_calorias_totais()

    def atualiza_dieta(self,*args):
        if self.is_float(self.calorias_novas.text):
            calorias_novas = float(self.calorias_novas.text)
            proporcao = calorias_novas/self.calorias_totais
            refeicoes_novas = []
            for refeicao in self.refeicoes_adicionados:
                refeicoes_novas.append(modifica_quantidades(refeicao, proporcao))
            
            for refeicao_antiga, refeicao_nova in zip(self.refeicoes_adicionados, refeicoes_novas):
                remove_refeicao(self.dieta, refeicao_antiga)
                self.remover_refeicao(refeicao_antiga.nome)
                add_refeicao(refeicao_nova, self.dieta)
                
            calcula_informacoes_nutricionais(self.dieta)
            self.label_erros.text = "Dieta criada com sucesso"
            self.label_erros.color = PRIMARY_COLOR
        else:
            dieta=self.dieta
            self.atualizado = True
            for refeicao in self.refeicoes_adicionados:
                add_refeicao(refeicao, dieta)    
            calcula_informacoes_nutricionais(self.dieta)
            self.label_erros.text = "Dieta criada com sucesso"
            self.label_erros.color = PRIMARY_COLOR
        
        self.calorias_totais = 0
        self.refeicoes_adicionados = []
        self.clear_widgets()
        self.criar_tela()
        
    def pesquisa(self, *args):
        args[0].clear_widgets()
        refeicao = ler_refeicao(args[1])
        self.refeicao = refeicao[0] if type(refeicao) == list else refeicao
        if refeicao:
            args[0].add_widget(CardRefeicao(objeto=refeicao, mostrar_delete=False, mostrar_edit=False))
            self.barra_pesquisa_label.text = ""
        else:
            self.barra_pesquisa_label.text = "refeição não encontrada"
            self.barra_pesquisa_label.color = ERROR_COLOR

    def criar_tela(self):
        self.items = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        
        self.scroll = MDScrollView()
        
        self.items.bind(minimum_height=self.items.setter("height"))
        
        self.botao_volta = MDRectangleFlatIconButton(icon="arrow-left", text="voltar")
        self.botao_volta.bind(on_release=self.funcao_retorno)
        
        self.items.add_widget(self.botao_volta)
        
        if not self.atualizacao:
            self.nome_input = MDTextField(hint_text="Nome da dieta", required=True)
            self.descricao = MDTextField(hint_text="Descrição da dieta (opcional)")
            self.items.add_widget(self.nome_input)
            self.items.add_widget(self.descricao)   
        else:
            self.calorias_novas = MDTextField(hint_text="Quantidade de Calorias", required=False)
            self.items.add_widget(self.calorias_novas)
        
        #Widget com os cards dos refeicoes adicionados
        self.refeicoes_adicionados_widgets = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        
        self.refeicoes_adicionados_widgets.bind(minimum_height=self.refeicoes_adicionados_widgets.setter("height"))
        self.label_calorias = MDLabel(text="Calorias: " + str(self.calorias_totais))
        self.label_gorduras = MDLabel(text="Gorduras: " + str(self.gorduras_totais))
        self.label_proteinas = MDLabel(text="Proteinas: " + str(self.proteinas_totais))
        self.label_carboidratos = MDLabel(text="Carboidratos: " + str(self.carboidratos_totais))
        
        self.refeicoes_adicionados_widgets.add_widget(self.label_calorias)
        self.refeicoes_adicionados_widgets.add_widget(self.label_gorduras)
        self.refeicoes_adicionados_widgets.add_widget(self.label_carboidratos)
        self.refeicoes_adicionados_widgets.add_widget(self.label_proteinas)
        self.refeicoes_adicionados_widgets.add_widget(MDLabel(text="Refeições adicionadas: "))
        
        if self.atualizacao:
            refeicoes = ler_refeicoes_dieta(self.dieta)
            for refeicao in refeicoes:
                self.refeicoes_adicionados.append(refeicao)
                self.calcula_calorias_totais()
                self.refeicoes_adicionados_widgets.add_widget(CardRefeicao(objeto=refeicao, mostrar_delete=True, mostrar_edit=False, deletar_do_banco=False))
                #remove_refeicao(self.dieta, refeicao)
            
                
        self.adicionar_refeicoes = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        self.adicionar_refeicoes.bind(minimum_height=self.adicionar_refeicoes.setter("height"))

        #espaço para aparecer o refeicao buscado
        self.espaco_refeicao = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        self.espaco_refeicao.bind(minimum_height=self.espaco_refeicao.setter("height"))

        self.barra_pesquisa = InputPesquisa("Pesquisar refeição para adicionar...",search_callback=partial(self.pesquisa, self.espaco_refeicao))
        self.barra_pesquisa_label = MDLabel(text="", color=ERROR_COLOR)
        self.botao_add_refeicao = MDRectangleFlatIconButton(icon="plus", text="Adicionar refeição")
        self.botao_add_refeicao.bind(on_release=self.add_refeicao)
        
        self.adicionar_refeicoes.add_widget(self.barra_pesquisa)
        self.adicionar_refeicoes.add_widget(self.barra_pesquisa_label)
        self.adicionar_refeicoes.add_widget(self.espaco_refeicao)
        self.adicionar_refeicoes.add_widget(self.botao_add_refeicao)

        self.label_erros = MDLabel(text="", color=ERROR_COLOR)

        self.botao_submeter = MDRectangleFlatIconButton(icon="plus", text="Adicionar dieta" if not self.atualizacao else "Atualizar dieta")
        self.botao_submeter.bind(on_release=self.criar_dieta_db if not self.atualizacao else self.atualiza_dieta)

        
        self.items.add_widget(self.refeicoes_adicionados_widgets)
        self.items.add_widget(self.adicionar_refeicoes)
        self.items.add_widget(self.botao_submeter)
        self.items.add_widget(self.label_erros)

        self.scroll.add_widget(self.items)
        self.add_widget(self.scroll)