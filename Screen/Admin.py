from sys import path
path.append('/usr/lib/python3/dist-packages/')
path.append('/usr/local/lib/python3.5/dist-packages')
from kivy.app import App
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from Screen.Login import Title
import mysql.connector as db
import pandas
elect = db.connect(host="localhost", user="root", passwd="1997", db="elective")
cursor = elect.cursor()

Builder.load_string('''
<display>:
    canvas:
        Color:
            rgba: .7,.3,.6,1
        Rectangle:
            size : self.size
            pos : self.pos
''')

class sublist(StackLayout):
    def set(self,name):
        self.orientation = 'tb-lr'
        self.size_hint = (.2,1)
        self.name = Label(text = name,size_hint = (1,None),height=40,color=(0,0,0,1))
        self.add_widget(self.name)

class display(BoxLayout):
    def set(self,sub):
        self.orientation = 'horizontal'
        self.size_hint = (1,.9)
        self.sub = sub
        self.obj = []
        for i in range(len(self.sub)):
            self.l = sublist()
            self.l.set(self.sub[i])
            self.obj.append(self.l)
            self.add_widget(self.l)

    def show(self,alloted):
        for i in range(len(alloted)):
            for j in range(len(alloted[i])):
                self.i = Label(text = str(alloted[i][j]),color=(0,0,0,1),size_hint=(1,None),height =40)
                self.obj[i].add_widget(self.i)


class AdminBg(BoxLayout):
    def set(self):
        self.sub = ['IT','Mech','Comp','Civil','Petro','Extc','Elect','Chem']
        self.alloted = [[],[],[],[],[],[],[],[]]
        self.size_hint = (1,.9)
        self.orientation = 'vertical'
        self.b = Button(text='Allot', size_hint=(None, None), height=50, width=100, on_press=self.allot,pos_hint = {'center_x': .5,'top':.5})
        self.add_widget(self.b)
        self.limit = 1
        self.d = display()
        self.d.set(self.sub)
        self.add_widget(self.d)


    def allot(self,a):
        df = pandas.read_sql('select * from pref',elect)
        df =df.sort_values(by = 'cgpa',ascending=False)
        print(df)
        for i in df.index:
            self.a = [int(i) for i in df.loc[i][:9]]
            self.rollno = self.a[0]
            self.a = self.a[1:]
            self.af = False
            if self.af == False:
                for k in range(1,len(self.a)+1):
                    if self.af == False:
                        for j in range(len(self.a)):
                            if self.a[j] == k and len(self.alloted[j]) < self.limit and self.af==False:
                                self.alloted[j].append(self.rollno)
                                self.af = True
                                break
                    else:
                        break
        self.d.show(self.alloted)




class AdminScreen(Screen,BoxLayout):
    def set(self):
        self.orientation = 'vertical'
        self.name = 'admin'
        self.T = Title()
        self.T.set()
        self.add_widget(self.T)
        self.b= AdminBg()
        self.b.set()
        self.add_widget(self.b)

class AdminApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.a= AdminScreen()
        self.a.set()
        inspector.create_inspector(Window, AdminScreen)
        self.sm.add_widget(self.a)
        return self.sm

if __name__ == '__main__':
    AdminApp().run()