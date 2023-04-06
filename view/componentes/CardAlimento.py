from dataclasses import dataclass
import sys
sys.path.append("../../")

from view.colors_definitions import *
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

from controllers.alimento_crud import deletar_alimento

CARD_HEIGHT = 900

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
        self.objeto = objeto
        #Configurações do card
        self.orientation = "vertical"
        self.md_bg_color = TERCIARY_COLOR
        self.line_color=(0.2, 0.2, 0.2, 0.8)
        self.padding="4dp"
        self.valign = 'center'
        self.size_hint = (1, None)
        self.height = CARD_HEIGHT
        self.id = self.objeto.id
        # linha de cima
        linha1 = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="48dp")
        linha1.add_widget(MDLabel(bold=True, italic=True, text=self.objeto.nome, font_style="H5"))
        if self.objeto.descricao is not None: linha1.add_widget(MDLabel(italic=True, text=self.objeto.descricao, font_style="Subtitle1"))
        
        botao_delete = MDIconButton(icon="delete")
        botao_delete.bind(on_release=self.show_confirmation_dialog)
        linha1.add_widget(botao_delete)
        
        # linha de baixo
        linha2 = MDGridLayout(rows=6, cols=2, orientation="lr-tb", padding="8dp")


        if self.objeto.calorias_por_grama is not None: linha2.add_widget(MDLabel(text=f"Calorias por grama: {self.objeto.calorias_por_grama}kcal"))
        if self.objeto.calorias_por_colher is not None: linha2.add_widget(MDLabel(text=f"Calorias por colher: {self.objeto.calorias_por_colher}kcal"))
        if self.objeto.calorias_por_ml is not None: linha2.add_widget(MDLabel(text=f"Calorias por ml: {self.objeto.calorias_por_ml}kcal"))
        
        if self.objeto.proteinas_por_grama is not None: linha2.add_widget(MDLabel(text=f"Proteínas por grama: {self.objeto.proteinas_por_grama}gr"))
        if self.objeto.carboidratos_por_grama is not None: linha2.add_widget(MDLabel(text=f"Carboidratos por grama: {self.objeto.carboidratos_por_grama}gr"))
        if self.objeto.gorduras_por_grama is not None: linha2.add_widget(MDLabel(text=f"Gorduras por grama: {self.objeto.gorduras_por_grama}gr"))

        if self.objeto.proteinas_por_colher is not None: linha2.add_widget(MDLabel(text=f"Proteinas por colher: {self.objeto.proteinas_por_colher}gr"))
        if self.objeto.carboidratos_por_colher is not None: linha2.add_widget(MDLabel(text=f"Carboidratos por colher: {self.objeto.carboidratos_por_colher}gr"))
        if self.objeto.gorduras_por_colher is not None: linha2.add_widget(MDLabel(text=f"Gorduras por colher: {self.objeto.gorduras_por_colher}gr"))
        
        if self.objeto.proteinas_por_ml is not None: linha2.add_widget(MDLabel(text=f"Proteinas por ml: {self.objeto.proteinas_por_ml}gr"))
        if self.objeto.carboidratos_por_ml is not None: linha2.add_widget(MDLabel(text=f"Carboidratos por ml: {self.objeto.carboidratos_por_ml}gr"))
        if self.objeto.gorduras_por_ml is not None: linha2.add_widget(MDLabel(text=f"Gorduras por ml: {self.objeto.gorduras_por_ml}gr"))
        # adiciona as linhas ao Card
        self.add_widget(linha1)
        self.add_widget(linha2)

    def show_confirmation_dialog(self, button):
        dialog = MDDialog(
            title="Excluir alimento",
            text="Tem certeza que deseja excluir esse alimento?",
            size_hint=(0.8, 1),
            buttons=[
                MDFlatButton(
                    text="Sim",
                    on_release=lambda x: self.deletar(dialog)
                ),
                MDFlatButton(
                    text="Não",
                    on_release=lambda x: dialog.dismiss()
                ),
            ]
        )

        dialog.open()

    def deletar(self,*args):
        deletar_alimento(self.objeto.nome)
        args[0].dismiss()
        self.parent.remove_widget(self)
        
