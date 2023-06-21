from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.utils import platform
from kivy.core.window import Window


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
        return MDFloatLayout(self.nav)
    
    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            self.retorno()
            return True
        else:
            return False
    
    def remove_splash_custom():

        if(platform == 'android'):
            from android import loadingscreen #type: ignore
            loadingscreen.hide_loading_screen()

        return

    def on_enter(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.key_input)
        self.remove_splash_custom()
    
        
     
    def on_pause(self):
        return True
    
if __name__ == '__main__':
    MyApp().run()