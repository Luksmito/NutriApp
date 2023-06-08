from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.widget import MDWidget

class SeletorPagina(MDGridLayout):
    def __init__(self,current_page=0, total_pages=0, visible_pages=[], **kwargs):
        super(SeletorPagina, self).__init__(**kwargs)
        
        self.cols = 3
        self.rows = 2
        self.orientation = 'lr-tb'
        self.size_hint_y = None
        self.current_page = 1
        
        self.total_pages = total_pages if total_pages >= 1 else 1
        self.visible_pages = visible_pages
        self.current_page = current_page
        self.label = MDLabel(text=str(self.current_page) + ' de ' + str(self.total_pages),halign='center', valign='middle')
        
        self.add_widget(MDIconButton(icon='arrow-left', on_release=self.select_previous_page))
        self.add_widget(self.label)
        self.add_widget(MDIconButton(icon="arrow-right", on_release=self.select_next_page))

    def select_page(self, page):
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.label.text = str(self.current_page) + ' de ' + str(self.total_pages)

    def select_previous_page(self, instance):
        self.parent.parent.parent.pagina_anterior()
        self.select_page(self.current_page - 1)

    def select_next_page(self, instance):
        self.parent.parent.parent.proxima_pagina()
        self.select_page(self.current_page + 1)
