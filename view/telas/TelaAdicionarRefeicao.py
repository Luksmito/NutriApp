from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import MDWidget


import sys
from functools import partial
sys.path.append("../../")

from view.componentes.InputPesquisa import InputPesquisa
from view.componentes.CardAlimento import CardAlimento
from view.colors_definitions import ERROR_COLOR, PRIMARY_COLOR
from controllers.alimento_crud import ler_alimento
from controllers.refeicao_crud import *


            
class EscolhaQuantidade(MDGridLayout):
    def __init__(self,texto="texto",funcao_callback=None,**kwargs):
        super(EscolhaQuantidade, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.value = texto
        self.caixa = MDCheckbox(group="quantidades")
        self.caixa.bind(on_active=funcao_callback)
        self.add_widget(self.caixa)
        self.add_widget(MDLabel(text=texto))
        


class TelaAdicionarRefeicao(MDScreen):
    def __init__(self,atualizacao=False,refeicao=None,**kwargs):
        super(TelaAdicionarRefeicao,self).__init__(**kwargs)
        self.alimentos_adicionados_widgets = None
        self.atualizacao = atualizacao
        self.refeicao = refeicao
        self.alimentos_adicionados = list()
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
        self.adicionar_alimentos = None
        self.barra_pesquisa = None
        self.container_quantidade = None
        self.quantidade = None
        self.colheres = None
        self.gramas = None
        self.mls = None
        self.botao_add_alimento = None
        self.alimento = None
        self.calorias_totais = 0
        self.gorduras_totais = 0
        self.proteinas_totais = 0
        self.carboidratos_totais = 0
        self.atualizado = False
        self.criar_tela()
        
    def set_quantidade(self, checkbox,value):
        print(checkbox)

    def funcao_retorno(self, *args):
        if self.atualizacao and not self.atualizado:
            self.criar_refeicao_db()
        self.manager.troca_tela_refeicoes(self.atualizado)

    def criar_refeicao_db(self,*args):
        if not self.atualizacao:
            refeicao = {
                "nome": self.nome_input.text,
                "descricao": self.descricao.text
            }
            resposta = criar_refeicao(refeicao)
        else:
            resposta = True

        if resposta == True:
            if not self.atualizacao:
                refeicao = ler_refeicao(refeicao["nome"])
            else:
                self.atualizado = True
                refeicao=self.refeicao
            for alimento in self.alimentos_adicionados:
                add_alimento(refeicao, alimento[0], quantidade=alimento[1])    
            calcula_informacoes_nutricionais(refeicao)
            self.label_erros.text = "Refeiçao criada com sucesso"
            self.label_erros.color = PRIMARY_COLOR
        else: 
            self.label_erros.text = "Refeição com esse nome já cadastrada"
            self.label_erros.color = ERROR_COLOR
    
    def calcula_calorias_totais(self):
        self.calorias_totais = 0
        self.gorduras_totais = 0
        self.proteinas_totais = 0
        self.carboidratos_totais = 0
        for alimento in self.alimentos_adicionados:
            quantidade = processa_quantidade(alimento[1])
            alimento = alimento[0]
            #Calcula a quantidade de calorias
            if quantidade[1] == 'gr':
                if alimento.calorias_por_grama is not None:
                    self.calorias_totais += quantidade[0]*alimento.calorias_por_grama
            elif quantidade[1] == 'ml':
                if alimento.calorias_por_ml is not None:
                    self.calorias_totais += quantidade[0]*alimento.calorias_por_ml
            elif quantidade[1] == 'cl':
                if alimento.calorias_por_colher is not None:
                    self.calorias_totais += quantidade[0]*alimento.calorias_por_colher
            
            #Calcula a quantidade de gordura
            if alimento.gorduras_por_grama is not None and quantidade[1] == 'gr':
                self.gorduras_totais += alimento.gorduras_por_grama*quantidade[0]
            elif alimento.gorduras_por_colher is not None and quantidade[1] == 'cl':
                self.gorduras_totais += alimento.gorduras_por_colher*quantidade[0]
            elif alimento.gorduras_por_ml is not None and quantidade[1] == 'ml':
                self.gorduras_totais += alimento.gorduras_por_ml*quantidade[0]
            
            #Calcula a quantidade de carboídratos
            if alimento.carboidratos_por_grama is not None and quantidade[1] == 'gr':
                self.carboidratos_totais += alimento.carboidratos_por_grama*quantidade[0]
            elif alimento.carboidratos_por_colher is not None and quantidade[1] == 'cl':
                self.carboidratos_totais += alimento.carboidratos_por_colher*quantidade[0]
            elif alimento.carboidratos_por_ml is not None and quantidade[1] == 'ml':
                self.carboidratos_totais += alimento.carboidratos_por_ml*quantidade[0]
            
            if alimento.proteinas_por_grama is not None and quantidade[1] == 'gr':
                self.proteinas_totais += alimento.proteinas_por_grama*quantidade[0]
            elif alimento.proteinas_por_colher is not None and quantidade[1] == 'cl':
                self.proteinas_totais += alimento.proteinas_por_colher*quantidade[0]
            elif alimento.proteinas_por_ml is not None and quantidade[1] == 'ml':
                self.proteinas_totais += alimento.proteinas_por_ml*quantidade[0]
        
        self.label_calorias.text = "Calorias: " + f"{self.calorias_totais:.2f}"
        self.label_carboidratos.text = "Carboidratos: " + f"{self.carboidratos_totais:.2f}"
        self.label_gorduras.text = "Gorduras: " + f"{self.gorduras_totais:.2f}"
        self.label_proteinas.text = "Proteinas: " + f"{self.proteinas_totais:.2f}"
            
      
    def add_alimento(self,*args):
        quantidade = ''
        if self.alimento == None:
            self.label_erros.text = "Busque um alimento para adicionar"
            self.label_erros.color = ERROR_COLOR
            return
        if self.quantidade.text != "":
            if not self.is_float(self.quantidade.text):
                self.barra_pesquisa_label.text = "Quantidade deve ser um número"
                self.barra_pesquisa_label.color = ERROR_COLOR
                return
            if self.colheres.caixa.active:
                quantidade="cl"
                self.barra_pesquisa_label.text = ""
            elif self.gramas.caixa.active:
                quantidade="gr"
                self.barra_pesquisa_label.text = ""
            elif self.mls.caixa.active:
                quantidade="ml"
                self.barra_pesquisa_label.text = ""
            else:
                self.barra_pesquisa_label.text = "Marque uma caixa"
                self.barra_pesquisa_label.color = ERROR_COLOR
                return
            self.tipo_quantidade = quantidade
            self.alimentos_adicionados.append((self.alimento,f"{self.quantidade.text}{quantidade}"))
            self.calcula_calorias_totais()
            self.alimentos_adicionados_widgets.add_widget(CardAlimento(objeto=self.alimento, mostrar_atributos=False, quantidade=f"{self.quantidade.text} {quantidade}"))
        else:
            self.alimentos_adicionados.append((self.alimento,None))
            self.alimentos_adicionados_widgets.add_widget(CardAlimento(objeto=self.alimento, mostrar_atributos=False, quantidade=""))
        

    def is_float(self,string):
        """Função para verificar se um string é um float"""
        try:
            string = string.replace(',', '.')
            float(string)
            return True
        except:
            return False
        
    def remover_alimento(self,nome):
        for alimento in self.alimentos_adicionados:
            if alimento[0].nome == nome:
                self.alimentos_adicionados.remove(alimento)
        self.calcula_calorias_totais()

    def _funcao_retorno(self, *args):
        if self.atualizacao and not self.atualizado:
            self.criar_refeicao_db()
        self.funcao_retorno()
        
    def pesquisa(self, *args):
        args[0].clear_widgets()
        alimento = ler_alimento(args[1])
        self.alimento = alimento
        if alimento:
            args[0].add_widget(CardAlimento(objeto=alimento, mostrar_delete=False))
            self.barra_pesquisa_label.text = ""
        else:
            self.barra_pesquisa_label.text = "Alimento não encontrado"
            self.barra_pesquisa_label.color = ERROR_COLOR

    def criar_tela(self):
        self.items = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        
        self.scroll = MDScrollView()
        
        self.items.bind(minimum_height=self.items.setter("height"))
        
        self.botao_volta = MDRectangleFlatIconButton(icon="arrow-left", text="voltar")
        self.botao_volta.bind(on_release=self._funcao_retorno)
        
        self.items.add_widget(self.botao_volta)
        
        if not self.atualizacao:
            self.nome_input = MDTextField(hint_text="Nome da refeição", required=True)
            self.descricao = MDTextField(hint_text="Descrição da refeição (opcional)")
            self.items.add_widget(self.nome_input)
            self.items.add_widget(self.descricao)   
        
        #Widget com os cards dos alimentos adicionados
        self.alimentos_adicionados_widgets = MDGridLayout(cols=1, size_hint_y=None, padding=[40,40,40,40], spacing=50)
        
        self.alimentos_adicionados_widgets.bind(minimum_height=self.alimentos_adicionados_widgets.setter("height"))
        self.label_calorias = MDLabel(text="Calorias: " + str(self.calorias_totais))
        self.label_gorduras = MDLabel(text="Gorduras: " + str(self.gorduras_totais))
        self.label_proteinas = MDLabel(text="Proteinas: " + str(self.proteinas_totais))
        self.label_carboidratos = MDLabel(text="Carboidratos: " + str(self.carboidratos_totais))
        
        self.alimentos_adicionados_widgets.add_widget(self.label_calorias)
        self.alimentos_adicionados_widgets.add_widget(self.label_gorduras)
        self.alimentos_adicionados_widgets.add_widget(self.label_carboidratos)
        self.alimentos_adicionados_widgets.add_widget(self.label_proteinas)
        self.alimentos_adicionados_widgets.add_widget(MDLabel(text="Alimentos adicionados: "))
        
        if self.atualizacao:
            alimentos = ler_alimentos_refeicao(self.refeicao)
            for alimento in alimentos:
                self.alimentos_adicionados.append((alimento.alimento,alimento.quantidade))
                self.calcula_calorias_totais()
                self.alimentos_adicionados_widgets.add_widget(CardAlimento(objeto=alimento.alimento, mostrar_atributos=False, quantidade=f"{alimento.quantidade}"))
                remove_alimento(self.refeicao, alimento.alimento)
            
                
        self.adicionar_alimentos = MDGridLayout(cols=1,size_hint_y=None, padding=[40,40,40,40], spacing=50)
        self.adicionar_alimentos.bind(minimum_height=self.adicionar_alimentos.setter("height"))

        #espaço para aparecer o alimento buscado
        self.espaco_alimento = MDGridLayout(cols=1,size_hint_y=None, padding=[40,100,40,100], spacing=50)
        self.espaco_alimento.bind(minimum_height=self.espaco_alimento.setter("height"))

        self.barra_pesquisa = InputPesquisa("Pesquisar alimento para adicionar...",search_callback=partial(self.pesquisa, self.espaco_alimento))
        self.barra_pesquisa_label = MDLabel(text="", color=ERROR_COLOR)
        self.container_quantidade = MDGridLayout(cols=4, rows=1,spacing=10)
        self.quantidade = MDTextField(hint_text="quantidade", required=False)
        self.colheres = EscolhaQuantidade(texto="colheres", funcao_callback=self.set_quantidade)
        self.gramas = EscolhaQuantidade(texto="gramas", funcao_callback=self.set_quantidade)
        self.mls = EscolhaQuantidade(texto="mls", funcao_callback=self.set_quantidade)
        self.botao_add_alimento = MDRectangleFlatIconButton(icon="plus", text="Adicionar alimento")
        self.botao_add_alimento.bind(on_release=self.add_alimento)

        self.container_quantidade.add_widget(self.quantidade)
        self.container_quantidade.add_widget(self.colheres)
        self.container_quantidade.add_widget(self.gramas)
        self.container_quantidade.add_widget(self.mls)

        
        self.adicionar_alimentos.add_widget(self.barra_pesquisa)
        self.adicionar_alimentos.add_widget(self.barra_pesquisa_label)
        self.adicionar_alimentos.add_widget(self.container_quantidade)
        self.adicionar_alimentos.add_widget(MDWidget())
        self.adicionar_alimentos.add_widget(self.espaco_alimento)
        self.adicionar_alimentos.add_widget(self.botao_add_alimento)

        self.label_erros = MDLabel(text="", color=ERROR_COLOR)

        self.botao_submeter = MDRectangleFlatIconButton(icon="plus", text="Adicionar refeição" if not self.atualizacao else "Atualizar refeição")
        self.botao_submeter.bind(on_release=self.criar_refeicao_db)

        
        self.items.add_widget(self.alimentos_adicionados_widgets)
        self.items.add_widget(self.adicionar_alimentos)
        self.items.add_widget(self.botao_submeter)
        self.items.add_widget(self.label_erros)

        self.scroll.add_widget(self.items)
        self.add_widget(self.scroll)