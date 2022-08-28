# keyboard-script-driver-for-serialPort-divices
this is a driver software with a visual interface to use serial port divices like Aduino-Uno as a macro-keybord

How to install :
    -put the exe file found in keyboard-script-driver-for-serialPort-divices/exe/
     into any folder on your computer and right klick the file .
     Now select if you want to start the driver at statup.

How to use :

    The Driver comunicates via Serial with the aduino.

    use the following code inside the AduinoProgram:
    '
    void setup() {
    Serial.begin(115200);
    }

    '
    info: the baudrate can be chanced in the setings.pack file (location: <roodFolder>/resources/setings.pack)


    Now you can send codes via 'Serial.print();'
    in the main loop.


Modifiing keys:


    To modify keys,
    click into the trace menu in the Taskbar and Right-klick the icon.
    Then klick 'OpenInterface'

    Now you are inside the software.
    - use the 'adkey'-Buton to add  a new key now select the displayName,the via serialPrint sendet code and the path for a key-script.
    - to deaktivate the delete or Move mode ,just press the button again
    - to save the config just close the window
    - you can also edit existing keys by clicking on them and pressing save in the conf menu

Key-Scripts:

    Manual(via Text-editor):
        - use one of the given signals ("r","p","b","w")
        info: the wait value is given in ms
        - an '#'+Space can be used to leve empty or comment-like lines

        meaning:
            w=wait  Usage:['wait <delay in ms>' ]
            p=keyPress only (No key release)  Usage:['p <key>' ]
            r=keyRelease   Usage:['r <key>' ]
            b=Normal key-press (press and release) Usage:['b <key>' ]
        usage example:
            '
            p v
            w 1000
            r l
            b i
            '
    Automatic (via intertace )(in beta):
        -klick the .ksh icon in the right upper corner and select an option,enter the key/delay value
        -type in a Name and save


Posible Errors:

    The Software doesn't conect to the aduino:
        - try closing the Serial-Monitor of the Aduino-IDE if it is open ir other programs that might try to the aduino via serial.
        - the software is also unable to conect to the aduino while a IDE is uploading a Sketch
        - if none of the things works try wait a bit and restart the software

    The Aduino Software(IDE) is unable to Upload a Sketch to the aduino :
        - close the software using the tray-icon and click exit to exit the software
        ,restart it after the Sketch has been uploadet


