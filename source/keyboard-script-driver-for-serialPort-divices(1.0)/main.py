import threading
import time
import tkinter.messagebox

import gridlessEngine
import os, winshell
from win32com.client import Dispatch


ProgramName="Adukey"
import keyboard
import key

from key import MAIN_THREAD_OPERATION,DoOperaration

from ConfigMenue import open_Editor as op_en
from PIL import Image
import pystray
#######import tets
import serial
from Vsvpack import vsvpack
#tkinter threading exis block
import ConfigMenue


####
from Vsvpack import absoluteScriptFolderPath
####
adfw=absoluteScriptFolderPath()
pa=adfw.get(__file__)
def autostart_q():


    startup = winshell.startup()
    print(startup)


    path = os.path.join(startup, "serial_key_driver.lnk")
    target = pa+r"\serial_key_driver.exe"
    wDir = pa
    icon = pa+r"\resources/tray_image.ico"

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()








GLB_RUNTIME_TRUE=True
setings=vsvpack("resources","Settings")
setings.new(False)

if setings.read("firstRun")=="1":
    pass
    #gridlessEngine.openScreen()

if (setings.read("q_ask_startup")=="1"):
    if (tkinter.messagebox.askquestion("Serial_key_driver", "do you want to start the drivcer on startup ?",icon="question") == "yes"):
        autostart_q()
        setings.add("q_ask_startup","0")
    
    
    #restprogram
def noFunc():
    print("NF")
    pass

def KillProcesses():
    global c
    c.stop()
    GLB_RUNTIME_TRUE=False

    #raise KeyboardInterrupt
    exit(0)

tray_image=Image.open("resources/tray_image.png")
r=Image.open("resources/img/status_r.png")

g=Image.open("resources/img/status_g.png")
c=pystray.Icon("Neutral",tray_image,menu=pystray.Menu(
    pystray.MenuItem("OpenInterface",op_en),
    pystray.MenuItem("Exit",KillProcesses)
))


status=False  #False -> NoConection , True -> Conection
keySet=vsvpack("resources","KeySave")
keySet.new(False)
serial_channel=None

def addKey(Name=None,Key="0",Value=0):
    global keySet
    ##KeyGraficGenearation
    allKeys=keySet.read("all").split(":")
    keySet.add()

def runIcon():
    global c
    print("r>::")
    c.run()
runcount=0
set_port=setings.read("Serial_Port")
set_baudrate=setings.read("baudrate")
def PortKomunication():

    global runcount, c, r, g, status, serial_channel,setings,GLB_RUNTIME_TRUE
    cou = 0
    while True:#GLB_RUNTIME_TRUE:

        #print(f"{status=}")
        try:

            if not status:

                serial_channel= serial.Serial(port=set_port, baudrate=set_baudrate, timeout=.01)#float(setings.read("pull_delay")))


                c.icon = g


                status=True



        except Exception:#Exception:

            serial_Chanel=None
            if status:

                status=False
                print("error")
            time.sleep(2)
            continue

        l=serial_channel.readline()

        cou+=1
        #print(f"{cou}:{l=}")

        if l==b"":
           pass
        else:
            l=str(l)
            l=l.replace("b'","").replace("'","")
            tkinter.messagebox.Message("pressed",l)
            key.runKey(l)
        time.sleep(0.1)









t,t2=None,None
def main():
    global t,t2,DoOperaration,MAIN_THREAD_OPERATION
    t=threading.Thread(target=PortKomunication)



    #t2 = threading.Thread(target=runIcon)
    t.daemon = True
    t.start()


    #t2.start()
    runIcon()

if __name__ == '__main__':
    main()







