from dataclasses import dataclass
import sys
sys.path.append("../../")

from view.colors_definitions import *
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton

CARD_HEIGHT = 500

@dataclass
class Alimento:
    nome: str
    calorias_por_grama: float
    calorias_por_colher: float
    calorias_por_ml: float
    proteinas_por_grama: float
    carboidratos_por_grama: float
    gorduras_por_grama: float
    proteinas_por_colher: float
    carboidratos_por_colher: float
    gorduras_por_colher: float
    proteinas_por_ml: float
    carboidratos_por_ml: float
    gorduras_por_ml: float


class CardAlimento(MDCard):
    def __init__(self,objeto: Alimento = None,**kwargs):
        super().__init__(**kwargs)

        #Configurações do card
        self.orientation = "vertical"
        self.md_bg_color = TERCIARY_COLOR
        self.line_color=(0.2, 0.2, 0.2, 0.8)
        self.padding="4dp"
        self.valign = 'center'
        self.size_hint = (1, None)
        self.height = CARD_HEIGHT
        self.id = objeto.id
        # linha de cima
        linha1 = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="48dp")
        linha1.add_widget(MDLabel(bold=True, italic=True, text=objeto.nome, font_style="H5"))
        if objeto.descricao is not None: linha1.add_widget(MDLabel(italic=True, text=objeto.descricao, font_style="Subtitle1"))
        linha1.add_widget(MDIconButton(icon="pencil"))
        linha1.add_widget(MDIconButton(icon="delete"))
        
        # linha de baixo
        linha2 = MDGridLayout(rows=4, cols=2, orientation="lr-tb", padding="8dp")


        if objeto.calorias_por_grama is not None: linha2.add_widget(MDLabel(text=f"Calorias por grama: {objeto.calorias_por_grama}kcal"))
        if objeto.calorias_por_colher is not None: linha2.add_widget(MDLabel(text=f"Calorias por colher: {objeto.calorias_por_colher}kcal"))
        if objeto.calorias_por_ml is not None: linha2.add_widget(MDLabel(text=f"Calorias por ml: {objeto.calorias_por_ml}kcal"))
        
        if objeto.proteinas_por_grama is not None: linha2.add_widget(MDLabel(text=f"Proteínas por grama: {objeto.proteinas_por_grama}gr"))
        if objeto.carboidratos_por_grama is not None: linha2.add_widget(MDLabel(text=f"Carboidratos por grama: {objeto.carboidratos_por_grama}gr"))
        if objeto.gorduras_por_grama is not None: linha2.add_widget(MDLabel(text=f"Gorduras por grama: {objeto.gorduras_por_grama}gr"))

        if objeto.proteinas_por_colher is not None: linha2.add_widget(MDLabel(text=f"Proteinas por colher: {objeto.proteinas_por_colher}gr"))
        if objeto.carboidratos_por_colher is not None: linha2.add_widget(MDLabel(text=f"Carboidratos por colher: {objeto.carboidratos_por_colher}gr"))
        if objeto.gorduras_por_colher is not None: linha2.add_widget(MDLabel(text=f"Gorduras por colher: {objeto.gorduras_por_colher}gr"))
        
        if objeto.proteinas_por_ml is not None: linha2.add_widget(MDLabel(text=f"Proteinas por ml: {objeto.proteinas_por_ml}gr"))
        if objeto.carboidratos_por_ml is not None: linha2.add_widget(MDLabel(text=f"Carboidratos por ml: {objeto.carboidratos_por_ml}gr"))
        if objeto.gorduras_por_ml is not None: linha2.add_widget(MDLabel(text=f"Gorduras por ml: {objeto.gorduras_por_ml}gr"))
        # adiciona as linhas ao Card
        self.add_widget(linha1)
        self.add_widget(linha2)
