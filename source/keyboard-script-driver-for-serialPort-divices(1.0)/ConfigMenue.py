import os
import threading


import tkinter
import tkinter.font as tkFont

from tkinter import ttk, filedialog
from tkinter import messagebox
from tkinter.ttk import Button

import pyautogui


from Vsvpack import vsvpack

import Debuger
import key







GLB_RUNTIME_TRUE=True
setings=vsvpack("resources","Settings")
setings.new(False)
Editor_is_Open=False
import gridlessEngine as gE
from gridlessEngine import GameFunction
tk_main=None
first_run=True
comb_box_list=[]
bu=None

class StrVar:
    def __init__(self):
        self.__s=""
        self.index=0
    def get(self):
        return self.__s
    def set(self,v):
        self.__s=v
    def setIndex(self,v):
        self.index=v

def ScriptEditor():
    global b,bu
    tk= tkinter.Tk()


    f=Debuger.Obj_viever_frame(tk)
    #f.pack(anchor="nw")
    Na = Box(master=tk, insert="Name:", width=20,)
    f2 = ttk.Frame(master=tk)

    f2.pack()#anchor="w")
    b=Button(master=f2,text="+",command=lambda:return_ComboBox(tk))
    b_save = Button(master=f2, text="Save", command=lambda: SaveScript(Na))
    b.pack(side="left",anchor="s")
    bu = b
    b_save.pack(side="right",anchor="s")

    place_under_e = f




    # get first 3 letters of every month name
def SaveScript(Name):
    global  comb_box_list
    l=[]
    Name=Name.get("0.0",tkinter.END).replace("\n","")
    for dict_key in comb_box_list:
        operation,but=dict_key
        but=but.get("0.0",tkinter.END).replace("\n","")
        operation=operation.get()

        if(operation=="KeyPress"):
            l+=["p "+but]
        elif(operation=="KeyRelease"):
            l += ["r " + but]
        elif (operation == "Key"):
            l += ["b " + but]
        elif (operation == "wait"):
            l += ["w " + but]
        else:
            print("ERROR::")
    with open("scripts\\"+Name+".ksh","w") as s:

        for line in l:#
            s.write(line+"\n")

editor_frame_list=[]
def getFrameIndex(v):
    global editor_frame_list
    x=-1
    for Value in editor_frame_list :
        x+=1
        if(Value==v):
            return x

def return_ComboBox(tk,before=None,index=None):
    global bu,editor_frame_list,comb_box_list
    t=StrVar()
    font1 = tkFont.Font(family="Arial", size=3)  # weight="bold")
    f = ttk.Frame(master=tk)

    b = Button(master=f, text="-",width=5 ,command=lambda: forget(f))
    b2 = Button(master=f, text="^", width=5, command=lambda: return_ComboBox(tk,before=f))

    t0 = tkinter.Text(master=f, width=4, height=1, font=font1, fg="#113361")

    t0.bind("<Key>",lambda event,text=t0,comb=t:lock_text(text,event,comb))

    com_box = ttk.Combobox(f)
    com_box.bind('<<ComboboxSelected>>',lambda event ,var=t,b=com_box:changeVar(event,var,b))




    b.pack(side="left", anchor="w")
    b2.pack(side="left", anchor="w")
    com_box.pack(side="left", anchor="w")
    t0.pack(side="left", anchor="w")
    com_box['values'] = ["KeyPress","KeyRelease","Key","wait"]
    if before == None:
        editor_frame_list += [f]
        f.pack(before=bu, anchor="nw")
        comb_box_list += [(t, t0)]
    else:
        f.pack(before=before, anchor="nw")
        i=getFrameIndex(before)
        editor_frame_list.insert(i, f)
        comb_box_list.insert(i,(t, t0))

    return t
def changeVar(e,var,box):
    var.set(box.get())
def forget(t):
    global comb_box_list
    i=editor_frame_list.index(t)
    editor_frame_list.remove(t)
    comb_box_list.pop(i)
    t.pack_forget()

def lock_text(t,event,textV):
    textV=textV.get()
    k=event.char


    num=[str(i) for i in range(0,10)]


    if (k=="\r")|(k=="\x08")|(k=="\r"):

        return "break"
    elif (textV=="KeyPress")|(textV=="KeyRelease")|(textV=="Key"):

        t.insert("0.0",k)
        t["state"]="disabled"

    elif (k not in num)&(textV=="wait"):
        #print(f"{k},{type(k)}")
        return "break"



def open_Editor():
    global Editor_is_Open,tk_main


    if(not Editor_is_Open):
        tk_main=threading.Thread(target=RunEditor)
        try:
            tk_main.start()
        except Exception:
            pass
        Editor_is_Open = True
def RunEditor():

    while True:


        gE.openScreen(1200,800,bg_image="resources/key_editor_background.png",DevMode=False)
        #gE.DisableObjViewer()
        generateInterface()
        gE.setExitFunction(ex)

        gE.RunEngine()  #Ubergibt theath tk main
        return


def ex():
    global Editor_is_Open,move_Enabled
    Editor_is_Open=False
    key.Dumb()
    key.read()
    move_Enabled=False
    key.k=1

    gE.StopEngine()


delMode=False

def enableMove(ghf=""):
    global move_Enabled,delMode
    delMode=False

    if not move_Enabled:
        for key_b in key.KeyDict.keys():
            kk = key.KeyDict[key_b].gra_key
            kk.ChangeTexture("resources\editor\key_m.png", ChangeHitbox=False)
            kk.follower_List[0].lift()
        move_Enabled = True
    elif move_Enabled:
        for key_b in key.KeyDict.keys():
            kk = key.KeyDict[key_b].gra_key
            kk.ChangeTexture("resources\editor\key.png", ChangeHitbox=False)
            kk.follower_List[0].lift()
        move_Enabled=False

def enableDelMode(ghf=""):
    global move_Enabled,delMode
    move_Enabled=False

    if not delMode:
        for key_b in key.KeyDict.keys():
            kk = key.KeyDict[key_b].gra_key
            kk.ChangeTexture("resources\editor\key_X.png", ChangeHitbox=False)
            kk.follower_List[0].lift()
        delMode = True
    elif delMode:
        for key_b in key.KeyDict.keys():
            kk = key.KeyDict[key_b].gra_key
            kk.ChangeTexture("resources\editor\key.png", ChangeHitbox=False)
            kk.follower_List[0].lift()
        delMode=False



def generateInterface():

    gE.setTitel("Serial-Driver")
    gE.setIcon("resources/tray_image.ico")
    gE.PlaceImage("resources/editor/add_button.png", 780.0, 140.0, Name="Add", func=GameFunction(keyEditor))
    gE.PlaceImage("resources/editor/remove_button.png", 1080.0, 140.0, Name="rem",func=GameFunction(enableDelMode))
    gE.PlaceImage("resources/editor/move_button.png", 700.0, 140.0, Name="move",func=GameFunction(enableMove))
    gE.PlaceImage("resources/editor/script_add_button.png", 1100,0, Name=".ksh-add", func=GameFunction(ScriptEditor))

    gE.PlaceImage("resources/editor/logo.png", 50, 10, Name="logo")
    key.render()
    #gE.setKeyListener(keyListener)
move_Enabled=False


def keyListener(com):
    global  helpTk
    action,key_=com
    if(action=="p"):

        match key_:
            case "h":

                os.system("notepad.exe resources/editor/help.txt")
def helpWindow():
    tk = tkinter.Tk()
    x, y = pyautogui.position()

    tk.wm_geometry("%dx%d+%d+%d" % (400, 300, x, y))

    # tk.overrideredirect(True)
    t1 = Box("Name:", tk)
    t2 = Box("Code:", tk)
    sp = Box("scriptPath:", tk)


    b1 = ttk.Button(master=tk, text="browse", command=lambda: durchs(sp))
    b1.pack()

    b2 = ttk.Button(master=tk, text="Save", command=lambda: Save(t1, t2, sp, tk))
    b2.pack()



"""
def keyElement():
    c0=gE.PlaceImage("resources/editor/key.png", 80, 280, Name="key")
    f0 = gE.PlaceText("key",120,320,Name="text",Collor="white")
    c0.addFollower(f0)
    return c0,f0
"""

ins_path=""
def durchs(t):
    filetypes = (
        ('Key-script-file', '*.ksh'),
        ('All files', '*.*'))
    file_path = filedialog.askopenfilename(filetypes=filetypes,initialdir ="scripts/")
    if(file_path!=""):
        t.replace("0.0", tkinter.END, "")
        t.insert(0.0, file_path)


def Save(t1,t2,path,tk):#,key_b,text_e):
    name,code,script=t1.get("0.0",tkinter.END).replace("\n",""),t2.get("0.0",tkinter.END).replace("\n",""),path.get("0.0",tkinter.END).replace("\n","")

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
        k=key.Key(code,keyscript=script,Name=name,render=True)
        key.KeyDict[code]=k
        #text_e.setText(name)

        tk.destroy()
    else:
        messagebox.showerror("Error","Missing Required filds")
def keyEditor(dsdfews=""):
    global move_Enabled,delMode
    if not move_Enabled or not delMode:
        for key_b in key.KeyDict.keys():
            kk = key.KeyDict[key_b].gra_key
            kk.ChangeTexture("resources\editor\key.png", ChangeHitbox=False)
            kk.follower_List[0].lift()
    move_Enabled,delMode=False,False
    tk= tkinter.Tk()
    x, y = pyautogui.position()

    tk.wm_geometry("%dx%d+%d+%d" % (300, 150,x,y))

    #tk.overrideredirect(True)
    t1=Box("Name:",tk,width=15)
    t2=Box("Code:",tk,width=15)
    sp=Box("scriptPath:",tk,width=12)


    b1=ttk.Button(master=tk,text="browse",command=lambda :durchs(sp))
    b1.pack(side="right",anchor="ne")
    #key_b, text = keyElement()
    b2 = ttk.Button(master=tk, text="Save", command=lambda: Save(t1,t2,sp,tk))#,key_b,text))
    b2.pack(side="left",anchor="nw")


def Box(insert, master,width=30,side=None,ancor=None):
    font1 = tkFont.Font(family="Arial", size=3)  # weight="bold")
    f=ttk.Frame(master=master)

    if side!=None:
        f.pack(side=side,anchor=ancor)
    else:
        f.pack()
    l=tkinter.Label(master=f,text=insert)
    l.pack()
    t0 = tkinter.Text(master=f, width=width, height=1, font=font1,fg="#113361")
    t0.pack(side="right")
    l.pack(side="left")

    return t0
    #t0.insert(0.0, insert)

