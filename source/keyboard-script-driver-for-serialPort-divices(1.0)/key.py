import json
import threading
import time

ProgramName="Adukey"
import tkinter
from tkinter import ttk, messagebox

import keyboard
import pyautogui
import win10toast as win10toast

import ConfigMenue
import Static_Var
import gridlessEngine as gE


from gridlessEngine import GameFunction
MAIN_THREAD_OPERATION=""
DoOperaration=False
winTo= win10toast.ToastNotifier()
KeyDict={}
keyList=[]
def runKey(signal):

    key=KeyDict.get(signal)
    if(key==None):
        print("[LOG]:unregistered Signal '"+signal+"'")
    else:
        t=threading.Thread(target=key.execute)
        t.start()

def Dumb():
    global KeyDict

    out=[]
    for key in KeyDict.keys():
        kk=KeyDict[key]
        out+=[{"Name":kk.Name,
                "code":key,
                  "script":kk.keyscript,
                  "cords":(kk.gra_key.b_x,kk.gra_key.b_y)
                  }]

    with open("configs/keyconfig.json","w")as f_:

        json.dump(out,f_,ensure_ascii=False, indent=4)
        f_.close()
def render():
    for item in KeyDict.keys():
        KeyDict[item].keyElement()

def Remove(value):
    for key in KeyDict.keys():
        k=KeyDict[key]
        if k==value:
            KeyDict.pop(key)
            return
class Key:
    def __init__(self,trigerSignal,keyscript="",Name="<Name>",cords=(180,280),render=False,textL=None):  #keySequence=["p__<KeyName>",r__<KeyName>"]
        global KeyDict
        self.keyscript=keyscript
        self.Name=Name
        self.gra_key=None
        self.textLink =None
        self.trigger=trigerSignal
        KeyDict[trigerSignal]=self
        self.pos = cords
        if(render):
            self.keyElement()

    def execute(self):
        global winTo
        with open(self.keyscript,"r")as sh:
            try:
                for KeyAction in sh.readlines():
                    act,code=KeyAction.replace("\n","").split(" ")
                    if act =="r":
                        keyboard.release(code)
                    elif act =="p":
                        keyboard.press(code)
                    elif act == "b":
                        keyboard.release(code)
                        keyboard.press(code)
                    elif act == "w":
                        c=code/1000
                        time.sleep(float(c))
                    elif act == "#":
                        continue
                    elif act == "\n":
                        continue

                    else:
                        winTo.show_toast(ProgramName,
                                         f"script '{self.keyscript}' in corupted, invalid Action Code '{act}'",
                                         # icon_path="",
                                         duration=10)

            except FileNotFoundError:
                winTo.show_toast(ProgramName,
                           f"Missing Script '{self.keyscript}'",
                           #icon_path="",
                           duration=10)

            except Exception:
                winTo.show_toast(ProgramName,
                                 f"Unexpected Error while executing '{self.keyscript}'",
                                 # icon_path="",
                                 duration=10)
    def keyElement(self):
        placex,placey=self.pos
        c0 = gE.PlaceImage("resources/editor/key.png", placex, placey, Name="key") #40
        f0 = gE.PlaceText(self.Name, placex+40, placey+40, Name="key-"+self.Name, Collor="white")
        c0.function=GameFunction(MoveKey,args=(c0,self))
        self.gra_key=c0
        self.textLink=f0
        c0.addFollower(f0)
        return c0,f0
    def configure(self,key_script=None,Name=None,triger=None):
        if key_script!=None:
            if(self.keyscript!=key_script):
                self.keyscript = key_script
        if Name!=None:
            if self.Name!=Name:
                self.Name=Name
                try:
                    self.textLink.setText(Name)
                except EOFError:
                     pass


        if triger!=None:
            if self.trigger!=triger:
                Remove(self)
                KeyDict[triger] = self




k=1
def Save(t1,t2,path,tk,key_classE):#,key_b,text_e):
    name,code,script=t1.get("0.0",tkinter.END).replace("\n",""),t2.get("0.0",tkinter.END).replace("\n",""),path.get("0.0",tkinter.END).replace("\n","")
    #print(f"..- {name =}--{code=}+--{script=}")
    Error=False
    if(name==""):
        t1.configure(bg="#c73e34")
        Error=True
    else:
        t1.configure(bg="white")
    if (code == ""):
        t2.configure(bg="#c73e34")
        Error = True
    else:
        t2.configure(bg="white")
    if (script == ""):
        path.configure(bg="#c73e34")
        Error = True
    else:
        path.configure(bg="white")
    if not (Error):

        key_classE.configure(Name=name,key_script=script,triger=code)
        tk.destroy()
    else:
        messagebox.showerror("Error","Missing Required filds")
def keyEditor(dsdfews="",key_classE=None):
    tk= tkinter.Tk()
    x, y = pyautogui.position()

    tk.wm_geometry("%dx%d+%d+%d" % (300, 150,x,y))

    #tk.overrideredirect(True)
    t1=ConfigMenue.Box("Name:",tk,width=15)
    t1.insert("0.0",key_classE.Name )
    t2=ConfigMenue.Box("Code:",tk,width=15)
    t2.insert("0.0", key_classE.trigger)
    sp= ConfigMenue.Box("scriptPath:", tk, width=12)
    sp.insert("0.0", key_classE.keyscript)
    b1=ttk.Button(master=tk, text="browse", command=lambda : ConfigMenue.durchs(sp))
    b1.pack(side="right",anchor="ne")
    #key_b, text = keyElement()
    b2 = ttk.Button(master=tk, text="Save", command=lambda: Save(t1,t2,sp,tk,key_classE))#,key_b,text))
    b2.pack(side="left",anchor="nw")

def MoveKey(key_b,key_classE):
    global k,keyList
    if ConfigMenue.move_Enabled:
        if k==0:
            return


        elif k==1:


            t=threading.Thread(target=lambda:mthread(key_b))
            t.start()
    elif ConfigMenue.delMode:
        Grafic_k=KeyDict.pop(key_classE.trigger)
        gE.forgetE(key_classE.textLink)
        gE.forgetE(key_b)

    else:
        keyEditor("",key_classE)


def mthread(key_b):
    global k

    tk=Static_Var.screen_link.getTk()
    tk.configure(cursor="cross")
    cx,cy=getCursorPos()

    k=0
    while True:

        c2x, c2y = getCursorPos()

        if gE.emp_klick:
            if not((c2x<=35)|(c2y<=223)|(c2x>=1063)|(c2y>=680)):
                key_b.moveTo(c2x,c2y)

            tk.configure(cursor="arrow")
            k=1
            return


def getCursorPos():
    x,y=pyautogui.position()
    tk=Static_Var.screen_link.getTk()
    mx,my=tk.winfo_x()+44,tk.winfo_y()+80

    return x-mx,y-my

def read():
    global KeyDict
    with open("configs/keyconfig.json", "r") as f_:
        KeyDict={}
        l=json.load(f_)

        for item in l:

            #(self,trigerSignal,keyscript="",Name="<Name>",cords=(180,80)):  #keySequence=["p__<KeyName>",r__<KeyName>"]

            key_b=Key(item["code"],item["script"],item["Name"],cords=(item["cords"][0],item["cords"][1]))





read()
