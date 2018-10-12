from Screen.Login import LoginScreen
from Screen.SignUp import SignUpScreen
from Screen.Pref import PrefScreen
from Screen.Admin import AdminScreen

from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivy.clock import Clock


class SwitchScreen(ScreenManager):
    #Switch Screen is the main screen manager of the application
    def loginC(self):
        self.l = LoginScreen()
        self.l.set()
        self.add_widget(self.l)
        self.current = 'login'
        self.s = SignUpScreen()
        self.s.set()
        self.add_widget(self.s)
        self.p = PrefScreen()
        self.p.set()
        self.username = self.l.B.LMB.LM.username
        self.p.username = self.username
        self.add_widget(self.p)
        self.ad = AdminScreen()
        self.ad.set()
        self.add_widget(self.ad)
    def update(self,dt):
        # Checks if there is any change in the screen
        if self.p.p.backf == True:
            self.current = 'login'
        elif self.l.B.LMB.LM.LoginT == True:
            if self.l.B.LMB.LM.admin==True:
                self.current = 'admin'
            else:
                self.username = self.l.B.LMB.LM.username
                self.p.p.username = self.username
                self.current = 'pref'
        elif self.l.B.LMB.LM.SignUpT == True:
            self.current = 'signup'
            self.s.X.SL.su.signupT = False
            self.s.X.SL.su.backtl = False
            self.l.B.LMB.LM.SignUpT = False
        elif self.s.X.SL.su.signupT == True or self.s.X.SL.su.backtl == True :
            self.current = 'login'



class ElectiveAllotmentSystemApp(App):
    # main application
    def build (self):
        self.a = SwitchScreen()
        self.a.loginC()
        Clock.schedule_interval(self.a.update, 1.0 / 60.0)
        return self.a

if __name__== '__main__':
    ElectiveAllotmentSystemApp().run()
