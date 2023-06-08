import sys
sys.path.append("../../")
from controllers.refeicao_crud import *

from view.colors_definitions import *
from kivymd.uix.card import MDCard
from kivymd.uix.widget import MDWidget 
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast

from controllers.refeicao_crud import deletar_refeicao

class CardRefeicao(MDCard):
    def __init__(self,objeto = None, mostrar_delete=True, mostrar_edit=True, funcao_retorno=None,deletar_do_banco=True,**kwargs):
        super().__init__(**kwargs)

        self.deletar_do_banco = deletar_do_banco
        #Configurações do card
        self.orientation = "vertical"
        self.md_bg_color = TERCIARY_COLOR
        self.line_color=(0.2, 0.2, 0.2, 0.8)
        self.padding="4dp"
        self.valign = 'center'
        self.size_hint = (1, None)
        self.height = 500
        self.objeto = objeto
        # linha de cima
        linha1 = MDGridLayout(rows=2,cols=3,orientation="tb-lr",padding="8dp")
        linha1.add_widget(MDLabel(bold=True, italic=True, text=objeto.nome, font_style="H5"))
        
        if objeto.descricao is not None: linha1.add_widget(MDLabel(italic=True, text=objeto.descricao, font_style="Body1"))
        
        if objeto.calorias_totais is not None: 
            linha1.add_widget(MDLabel(valign="center", text=f"Calorias totais: {str(objeto.calorias_totais)}kcal")) 
        else: 
            linha1.add_widget(MDWidget())
        linha1.add_widget(MDWidget())
        
        if mostrar_delete:
            self.botao_delete = MDIconButton(icon="delete")
            self.botao_delete.bind(on_release=self.show_confirmation_dialog)
            linha1.add_widget(self.botao_delete)
        if mostrar_edit:
            self.botao_editar = MDIconButton(icon="pencil")
        
            self.botao_editar.bind(on_release=self.editar)
            linha1.add_widget(self.botao_editar)
        
        
        # linha de baixo
        linha2 = MDGridLayout(rows=8, cols=2, orientation="lr-tb", padding="8dp")

        alimentos = ler_alimentos_refeicao(objeto)
        alimentos = [alimento for alimento in alimentos]
        for alimento in alimentos:
            texto = f"{alimento.alimento.nome}: {alimento.quantidade}"
            linha2.add_widget(MDLabel(text=texto, font_style="Body1"))

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
                    on_release=lambda _: dialog.dismiss()
                ),
            ]
        )

        dialog.open()

    def deletar(self,*args):
        if self.deletar_do_banco:
            args[0].dismiss()
            deletar_refeicao(self.objeto.nome)
            toast("Deletar refeição")
            self.parent.remove_widget(self)
        else:
            args[0].dismiss()
            self.parent.parent.parent.parent.remover_refeicao(self.objeto.nome)
            self.parent.remove_widget(self)
    
    def editar(self, *args):
        #Chama a tela de atualizar o alimento com a refeicao a ser atualizada como argumento
        #e 'True' é o argumento que indica que a tela deve ser renderizada na configuração de atualização
        self.parent.parent.parent.tela_adicionar_refeicao(self.objeto, True)
        