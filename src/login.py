from kivy.core.window import Window
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
import src.mainMenu as next
from src.cryptFile import Decryptor as dec
import src.main as sel
import src.mainMenu as next

browser = None
autologin = False

class Connected(Screen):
    pass

class Error(Screen):
    pass

class Login(Screen):
    def do_login(self, loginText, passwordText):
        global browser
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        if browser.login(loginText,passwordText):
            if autologin:
                App.get_running_app().stop()
                next.start(browser)
            #print("Logged in")
            #self.manager.transition = SlideTransition(direction="left")
            #self.manager.current = 'connected'
            App.get_running_app().stop()
            next.start(browser)
        else:
            self.ids['invalid'].opacity = 100
            #print("Login failed")
            self.resetForm()
            self.manager.current = 'login'

    def resetForm(self):
        self.ids['binusID'].text = ""
        self.ids['password'].text = ""

    def logout(self):
        self.ids['binusID'].text = ""
        self.ids['password'].text = ""
        self.ids['invalid'].text = ""

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        global browser, autologin
        self.title = "Student Desk v2"
        manager = ScreenManager()
        try:
            browser = sel.browser()
        except:
            manager.add_widget(Error(name='error'))
            #print("An error occurred")
            return manager
            #App.get_running_app().stop()

        if "studesk.key" not in os.listdir(os.getcwd()):
            manager.add_widget(Login(name='login'))
            manager.add_widget(Connected(name='connected'))
            return manager
        else:
            #login first and show main menu
            #call decrypt from crypt.py and return user and pass from keyring
            autologin = True
            creds = dec().decrypt() 
            browser.login(creds[0].decode(),creds[1].decode())
            #print(creds[0].decode() + " " + creds[1].decode())
            App.get_running_app().stop()

def start():
    Window.size = (500,300)
    LoginApp().run()
    if autologin:
        next.start(browser)

if __name__ == "__main__":
    Window.size = (500,300)
    LoginApp().run()
    if autologin:
        next.start(browser)
