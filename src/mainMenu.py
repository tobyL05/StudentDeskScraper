from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
import webbrowser as wb
import pprint as pp
import keyring as kr
import time
from src.cryptFile import Encryptor as enc
import src.main as sel
import pandas as pd
import math
import os

browser = None
loadedScores_term1 = False
loadedScores_term2 = False
loadedScores_term3 = False
loadedScores_term4 = False

class Home(Screen):
    pass

class WelcomeLbl(MDLabel):
    def setLabel(self, *args):
        MDApp.get_running_app().root.ids['welcomeLabel'].text = f"Welcome to Student Desk v2, {self.getName()}"

    def getName(self):
        global browser
        return browser.getName()

class Scores(Screen):
    def on_pre_enter(self):
        global loadedScores_term1
        if loadedScores_term1:
            return
        #GET SCORE FOR TERM 1 HERE
        self.scoreDF = browser.getScores(1)[0]
        row = 2
        for subject,grade in zip(self.scoreDF.iloc[:, 0].values, self.scoreDF.iloc[:, 1].values):
            MDApp.get_running_app().root.ids['firstTermScoreTable'].ids[f'subjectNameR{row}C1'].text = str(subject)
            if not math.isnan(grade):
                MDApp.get_running_app().root.ids['firstTermScoreTable'].ids[f'subjectScoreR{row}C2'].text = str(grade)[:-2]
            else:
                MDApp.get_running_app().root.ids['firstTermScoreTable'].ids[f'subjectScoreR{row}C2'].text = "N/A"
            row += 1
        loadedScores_term1 = True
        pass

class ScoresTerm(MDBottomNavigationItem):
    def getScore(self, term):
        global browser,loadedScores_term2,loadedScores_term3,loadedScores_term4
        #conditional for term and set text
        row = 2
        if term == 2:
            if loadedScores_term2:
                return
            key = 'secondTermScoreTable'
            self.scoreDF = browser.getScores(2)[0]
            loadedScores_term2 = True
        elif term == 3:
            if loadedScores_term3:
                return
            key = 'thirdTermScoreTable'
            self.scoreDF = browser.getScores(3)[0]
            loadedScores_term3 = True
        else:
            if loadedScores_term4:
                return
            key = 'fourthTermScoreTable'
            self.scoreDF = browser.getScores(4)[0]
            loadedScores_term4 = True

        for subject,grade in zip(self.scoreDF.iloc[:, 0].values, self.scoreDF.iloc[:, 1].values):
            MDApp.get_running_app().root.ids[key].ids[f'subjectNameR{row}C1'].text = str(subject)
            if not math.isnan(grade):
                MDApp.get_running_app().root.ids[key].ids[f'subjectScoreR{row}C2'].text = str(grade)[:-2]
            else:
                MDApp.get_running_app().root.ids[key].ids[f'subjectScoreR{row}C2'].text = "N/A"
            row += 1
        #print(term)

class SACAS(Screen):
    pass

class Calendar(Screen):
    def on_pre_enter(self):
        wb.open("https://binusianorg-my.sharepoint.com/personal/inquiries_simprug_binus_edu/_layouts/15/guestaccess.aspx?docid=08579cfb9b81b406392b3bec113bb396e&authkey=ARauMurcR9vFVKyLJNX49ws&e=OK9k8t", new=2)

class Setting(Screen):
    def on_pre_enter(self):
        if "studesk.key" in os.listdir(os.getcwd()):
            MDApp.get_running_app().root.ids['autoLoginOpt'].active = True
       

class ContentNavigationDrawer(Screen):
        
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class TestNavigationDrawer(MDApp):
    def build(self):
        self.title = ""
        welcome = WelcomeLbl()
        Clock.schedule_interval(self.update_clock,1)
        Clock.schedule_once(welcome.setLabel)
        return Builder.load_file("src/mainMenu.kv")

    def update_clock(self,*args):
        MDApp.get_running_app().root.ids['DigiClock'].text = time.asctime()

    def autoLogin(self,checkbox,value):
        global browser
        if value:
            if "studesk.key" in os.listdir(os.getcwd()):
                return
            #option is on
            creds = enc().encrypt(browser.id,browser.pwd) 
            #get encrypted credentials and save them
            kr.set_password("StudentDesk2", "studeskUser",creds[0].decode())
            kr.set_password("StudentDesk2","studeskPwd", creds[1].decode())
            #print(type(creds[0].decode()))
            #print(creds[1].decode())
        else:
            #delete saved files and delete from keyring (reset everything)
            os.remove("studesk.key")
            kr.delete_password("StudentDesk2","studeskUser")
            kr.delete_password("StudentDesk2",'studeskPwd')
            #print("off")


def start(browserObj):
    global browser
    browser = browserObj
    Window.size = (800,600)
    TestNavigationDrawer().run()
    browser.quitBrowser()

if __name__ == "__main__":
    browser = sel.browser()
    browser.login("1670004246","070505-02")
    start(browser)
    browser.quitBrowser()
