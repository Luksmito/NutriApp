from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.utils import platform
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

#Import do app
from view.telas.NavBar import NavBar


class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.material_style = "M3"
        self.nav = NavBar()
        self.retorno = self.nav._criar_tela
        self.on_start()
        return MDFloatLayout(self.nav)
    
    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            self.retorno()
            return True
        else:
            return False
        
    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.key_input)
     
    def on_pause(self):
        return True
if __name__ == '__main__':
    MyApp().run()
