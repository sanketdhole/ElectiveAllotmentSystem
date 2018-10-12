from sys import path
path.append('/usr/lib/python3/dist-packages/')
path.append('/usr/local/lib/python3.5/dist-packages')
from kivy.app import App
from kivy.lang import Builder
from Screen.Login import Title
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
import mysql.connector as db
import pandas

elect = db.connect(host="localhost", user="root", passwd="1997", db="elective")
cursor = elect.cursor()

select = [0,0,0,0,0,0,0,0]

class TButton(ToggleButton):
    def set(self,n,j,sub):
        self.text = 'Pref :'+ str(j+1)
        self.n = n
        self.j = j
        self.group = j+1
        self.on_press = self.selected

    def selected(self):
        global select
        select[self.n] = self.j+1
        print(select)

class pref(BoxLayout):
    def set(self,j,sub):
        self.orientation = 'horizontal'
        self.size_hint = (1,None)
        self.height = 50
        self.obj =[]
        self.l = Label(text = 'Pref No.:'+str(j+1))
        self.add_widget(self.l)
        for i in range(8):
            self.b = TButton()
            self.b.set(i,j,sub)
            self.add_widget(self.b)
            self.obj.append(self.b)

    def selected(self,a):
        print(self.o)



class prefsub(BoxLayout):
    def set(self):
        self.orientaion = 'horizontal'
        self.size_hint = (1,None)
        self.height = 50
        self.spacing = 10
        self.padding = (10,10)
        self.sub = ['Prefrence No.','IT','Mech','Comp','Civil','Petro','Extc','Elect','Chem']
        for i in range(9):
            self.a = Label(text = self.sub[i],size_hint=(.2,1))
            self.add_widget(self.a)



class PrefBg(BoxLayout):
    def set(self):
        self.username = ''
        self.prefgiven = False
        self.backf = False
        self.orientation = 'vertical'
        self.size_hint = (1,.9)
        self.a = prefsub()
        self.a.set()
        self.add_widget(self.a)
        self.o = []
        self.sub = ['IT','Mech','Comp','Civil','Petro','Extc','Elect','Chem']
        for i in range(8):
            self.a = pref()
            self.a.set(i,self.sub[i])
            self.o.append(self.a)
            self.add_widget(self.a)
        self.b= Button(text = 'Confirm',height = 50,width = 300,size_hint =(None,None),on_press = self.conf)
        self.add_widget(self.b)
        self.bk = Button(text = 'Back',height = 50,width = 200,size_hint = (None,None),on_press = self.back)
        self.add_widget(self.bk)

    def back(self,a):
        self.backf = True

    def conf(self,a):
        global select
        print(self.username)
        self.prefgiven = True
        self.q = 'select rollno,cgpa from studentdetails where username = "{}"'.format(self.username)
        print(self.q)
        cursor.execute(self.q)
        self.rollno = cursor.fetchone()
        self.cgpa = self.rollno[1]
        self.rollno = self.rollno[0]
        print(self.rollno,self.cgpa)
        self.query = 'insert into pref values ('
        self.query += "{},".format(self.rollno)
        for i in range(len(select)):
            self.query += "'"
            self.query += str(select[i])
            self.query += "'"
            if i == len(select)-1:
                pass
            else:
                self.query += ','
        self.query += ",'{}'".format(self.cgpa)
        self.query += ')'
        print(self.query)
        cursor.execute(self.query)
        elect.commit()



class PrefScreen(Screen):
    def set(self):
        self.username = ''
        self.name = 'pref'
        self.T = Title()
        self.T.set()
        self.add_widget(self.T)
        self.p = PrefBg()
        self.p.set()
        self.add_widget(self.p)

class PrefScreenApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.a = PrefScreen()
        self.a.set()
        self.sm.add_widget(self.a)
        return self.sm

if __name__ == '__main__':
    PrefScreenApp().run()