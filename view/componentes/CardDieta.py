import sys
sys.path.append("../../")
from functools import partial

from controllers.dieta_crud import *
from controllers.geraPdfDieta import *
from kivy.utils import platform
from kivy.clock import Clock
from view.colors_definitions import *
from kivymd.uix.card import MDCard
from kivymd.uix.widget import MDWidget 
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from view.componentes.TelaCarregamento import TelaCarregamento

path_home='/'


#Se estiver rodando no android pede permissão e busca o caminho para o diretorio raiz
if platform == "android":
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
    path_home = primary_external_storage_path()



class EscolhaDeArquivo(MDFileManager):
    """Classe que implementa as funcionalidades da tela de escolher um diretório"""
    
    def __init__(self,dieta,card,**kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.card = card
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        self.dieta = dieta
        
        
    def file_manager_open(self, *args):
        self.file_manager.show(path_home)  # output manager to the screen
        self.manager_open = True
          
    
    def select_path(self, path: str):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''
        
        self.clear_widgets()
        self.exit_manager()
        gerar_pdf(self.dieta, path)
        toast(f"PDF salvo em: {path}" )
        
        
        
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        self.card.clear_widgets()
        self.card.criar_card()
        self.manager_open = False
        self.file_manager.close()

        
        
class CardDieta(MDCard):
    """Classe que implementa os cards que mostram a dieta"""
    
    def __init__(self,objeto = None,funcao_retorno=None,**kwargs):
        super().__init__(**kwargs)

        #Configurações do card
        self.orientation = "vertical"
        self.md_bg_color = TERCIARY_COLOR
        self.line_color=(0.2, 0.2, 0.2, 0.8)
        self.padding="4dp"
        self.valign = 'center'
        self.size_hint = (1, None)
        self.height = 700
        self.objeto = objeto
        self.criar_card()
       
    
    def gera_pdf(self,*args):
        self.clear_widgets()
        self.add_widget(TelaCarregamento())
        files = EscolhaDeArquivo(self.objeto, self)
        Clock.schedule_once(files.file_manager_open)
        
    def criar_card(self, *args):
        self.clear_widgets()
         # linha de cima
        linha1 = MDGridLayout(rows=3,cols=3,orientation="tb-lr",padding="8dp")
        linha1.add_widget(MDLabel(bold=True, italic=True, text=self.objeto.nome, font_style="H5"))
        if self.objeto.descricao is not None: linha1.add_widget(MDLabel(italic=True, text=self.objeto.descricao, font_style="Body1"))
        
        else: linha1.add_widget(MDWidget())
        
        if self.objeto.calorias_totais is not None: 
            linha1.add_widget(MDLabel(valign="center", text=f"Calorias totais: {str(self.objeto.calorias_totais)}kcal")) 
        else: 
            linha1.add_widget(MDWidget())
        
        self.botao_delete = MDIconButton(icon="delete")
        self.botao_editar = MDIconButton(icon="pencil")
        self.botao_pdf = MDIconButton(icon="file-pdf-box")
        self.botao_delete.bind(on_release=self.show_confirmation_dialog)
        self.botao_editar.bind(on_release=self.editar)
        self.botao_pdf.bind(on_release=self.gera_pdf)
        
        linha1.add_widget(self.botao_editar)
        linha1.add_widget(self.botao_delete)
        linha1.add_widget(self.botao_pdf)
        
        # linha de baixo
        linha2 = MDGridLayout(rows=4, cols=2, orientation="lr-tb", padding="8dp")

        refeicoes = self.objeto.refeicoes
        refeicoes = [refeicao for refeicao in refeicoes]
        for refeicao in refeicoes:
            texto = f"{refeicao.nome}: {refeicao.calorias_totais}kcal" if refeicao.calorias_totais is not None else f"{refeicao.nome}"
            linha2.add_widget(MDLabel(text=texto, font_style="Body1"))

        # adiciona as linhas ao Card
        self.add_widget(linha1)
        self.add_widget(linha2)
    
    def show_confirmation_dialog(self, button):
        dialog = MDDialog(
            title="Excluir dieta",
            text="Tem certeza que deseja excluir essa dieta?",
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
        """Deleta a dieta do banco de dados"""
        
        args[0].dismiss() #Fecha o dialogo de confirmação de exclusão
        deletar_dieta(self.objeto.nome)
        toast("Dieta deletada")
        self.parent.remove_widget(self)#Se remove da tela
    
    def editar(self, *args):
        #Chama a tela de atualizar o alimento com a refeicao a ser atualizada como argumento
        #e 'True' é o argumento que indica que a tela deve ser renderizada na configuração de atualização
        self.parent.parent.parent.tela_adicionar_dieta(self.objeto, True)
        