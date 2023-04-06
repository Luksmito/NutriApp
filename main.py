from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout

#Import do app
from view.telas.NavBar import NavBar


class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.material_style = "M3"
        return MDFloatLayout(NavBar())

if __name__ == '__main__':
    MyApp().run()
