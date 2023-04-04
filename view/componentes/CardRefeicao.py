import sys
sys.path.append("../../")
from controllers.refeicao_crud import *

from view.colors_definitions import *
from kivymd.uix.card import MDCard
from kivymd.uix.widget import MDWidget 
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton


class CardRefeicao(MDCard):
    def __init__(self,objeto = None,**kwargs):
        super().__init__(**kwargs)

        #Configurações do card
        self.orientation = "vertical"
        self.md_bg_color = TERCIARY_COLOR
        self.line_color=(0.2, 0.2, 0.2, 0.8)
        self.padding="4dp"
        self.valign = 'center'
        self.size_hint = (1, None)
        self.height = 500

        # linha de cima
        linha1 = MDGridLayout(rows=2,cols=3,orientation="tb-lr",padding="8dp")
        linha1.add_widget(MDLabel(bold=True, italic=True, text=objeto.nome, font_style="H5"))
        if objeto.descricao is not None: linha1.add_widget(MDLabel(italic=True, text=objeto.descricao, font_style="Body1"))
        if objeto.calorias_totais is not None: 
            linha1.add_widget(MDLabel(valign="center", text=f"Calorias totais: {str(objeto.calorias_totais)}kcal")) 
        else: 
            linha1.add_widget(MDWidget())
        linha1.add_widget(MDWidget())
        linha1.add_widget(MDIconButton(icon="pencil"))
        linha1.add_widget(MDIconButton(icon="delete"))
        
        # linha de baixo
        linha2 = MDGridLayout(rows=4, cols=2, orientation="lr-tb", padding="8dp")

        alimentos = ler_alimentos_refeicao(objeto)
        alimentos = [alimento for alimento in alimentos]
        for alimento in alimentos:
            texto = f"{alimento.alimento.nome}: {alimento.quantidade}"
            linha2.add_widget(MDLabel(text=texto, font_style="Body1"))

        # adiciona as linhas ao Card
        self.add_widget(linha1)
        self.add_widget(linha2)
