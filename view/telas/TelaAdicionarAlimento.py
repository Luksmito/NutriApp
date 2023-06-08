from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.widget import MDWidget

import sys
sys.path.append("../../")

from view.colors_definitions import ERROR_COLOR, PRIMARY_COLOR
from controllers.alimento_crud import criar_alimento

class TelaAdicionarAlimento(MDScreen):
    def __init__(self,**kwargs):
        super(TelaAdicionarAlimento,self).__init__(**kwargs)
        self.criar_tela()
        
        
    def criar_alimento_db(self,**kwargs):
        erros = kwargs.pop("erros")
        erros.text = ""
        erros.color = ERROR_COLOR
        
        chaves_preenchidas_em_centenas = [
            'calorias_por_grama', 
            'proteinas_por_grama', 
            'carboidratos_por_grama', 
            'gorduras_por_grama',
            'calorias_por_ml', 
            'proteinas_por_ml', 
            'carboidratos_por_ml', 
            'gorduras_por_ml'
            ]
        #Passa por todas as chaves de kwargs para verificar se há alguma campo preenchido errado
        for chave, valor in kwargs.items():
            if chave == "nome" or chave == "descricao":
                continue
            if valor != "":
                if self.is_float(valor) == False:
                    nome_campo = chave.replace('_', " ")
                    erros.text += f"{nome_campo} deve ser um numero\n"
                    return
                else:
                    if chave in chaves_preenchidas_em_centenas:
                        kwargs[chave] = round(float(kwargs[chave])/100, 2)
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
    
    def is_float(self,string):
        """Função para verificar se um string é um float"""
        try:
            string = string.replace(',', '.')
            float(string)
            return True
        except:
            return False

    def funcao_retorno(self, *args):
        self.manager.current = "tela-alimentos"
    
    def criar_tela(self):
        items = MDGridLayout(cols=1,size_hint_y=None, padding=[40,120,40,120], spacing=150)
        box = MDGridLayout(cols=1,size_hint_y=None, padding=[40,120,40,200], spacing=50)
        scroll = MDScrollView()
        
        items.bind(minimum_height=items.setter("height"))
        
        botao_volta = MDRectangleFlatIconButton(icon="arrow-left", text="voltar")
        botao_volta.bind(on_release=self.funcao_retorno)
        
        items.add_widget(botao_volta)
        
        label = MDLabel(
            text="Algumas dicas: O único atributo obrigatório é o nome, adicione apenas os que forem relevantes para você,\
 se não souber alguma informação sobre o alimento você pode pesquisar no google ou no endereço: https://vitat.com.br/alimentacao/busca-de-alimentos\
 as informações fornecidas aqui serão utilizadas no cálculo da dieta")
        box.add_widget(label)
        items.add_widget(box)
        items.add_widget(MDWidget())
        nome_input = MDTextField(hint_text="Nome do alimento", required=True)
        descricao = MDTextField(hint_text="Descrição do alimento (opcional)")
        
        calorias_por_grama = MDTextField(hint_text="Calorias em 100 gramas do alimento (opcional)")
        calorias_por_ml = MDTextField(hint_text="Calorias em 100 ml's do alimento (opcional)")
        calorias_por_colher = MDTextField(hint_text="Calorias por colher do alimento (opcional)")

        proteinas_por_grama = MDTextField(hint_text="Proteínas em 100 gramas (opcional)")
        proteinas_por_colher = MDTextField(hint_text="Proteínas por colher (opcional)")
        proteinas_por_ml = MDTextField(hint_text="Proteínas em 100 ml's (opcional)")
        
        carboidratos_por_grama = MDTextField(hint_text="Carboídratos em 100 gramas (opcional)")
        carboidratos_por_colher = MDTextField(hint_text="Carboídratos por colher (opcional)")
        carboidratos_por_ml = MDTextField(hint_text="Carboídratos em 100 ml's (opcional)")
        
        gorduras_por_grama = MDTextField(hint_text="Gorduras em 100 gramas (opcional)")
        gorduras_por_colher = MDTextField(hint_text="Gorduras por colher (opcional)")
        gorduras_por_ml = MDTextField(hint_text="Gorduras em 100 ml's (opcional)")
        
        label_erros = MDLabel(text="", color=ERROR_COLOR)

        botao_submeter = MDRectangleFlatIconButton(icon="plus", text="Adicionar")
        botao_submeter.bind(
            on_release=lambda _:self.criar_alimento_db(
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