from tkinter import *
from tkinter import ttk
import serial
import pandas as pd
import time
import subprocess
import threading
from tkinter import colorchooser
from tkinter import filedialog
import tkinter.scrolledtext as tkst
window = Tk()
window.title("Paulina Czerska I Iwo Adamowicz GI")
window.geometry('700x765')
window.configure(background='#FFFAF0')
stop = False
ser= None
color='black'
filename=''
def run_program():
    subprocess.Popen(["main.exe"])
def colors():
    global color
    x = colorchooser.askcolor()[1]
    color = x
    if color!= None:
        console.tag_configure("color_text",foreground=color)
        kolorek.config(bg=color)
    return color
def stops():
    global stop
    global ser
    stop = True
    if ser is not None:
        ser.close()
        print("Połączenie z portem szeregowym zostało zamknięte")

dane=''
def serial_read_thread(ser):
    global dane
    while not stop:
        # Odczytaj linie danych z portu szeregowego
        line = ser.readline()

        # Wydrukuj otrzymane dane na konsoli
        print(line)
        line = line.decode()
        line.replace("str(b'')", "''")
        dane = dane + str(line)

        console.insert("end", str(line),"color_text")
        console.see("end")
        window.update_idletasks()



def serialf():
    global stop
    global ser
    port= cb['values'][cb.current()]
    baudrate= cb1['values'][cb1.current()]
    byte_size= cb2['values'][cb2.current()]
    if byte_size=='5':
        byte_size = serial.FIVEBITS
    if byte_size=='6':
        byte_size = serial.SIXBITS
    if byte_size=='7':
        byte_size = serial.SEVENBITS
    if byte_size=='8':
        byte_size = serial.EIGHTBITS
    stop_bits = cb3['values'][cb3.current()]
    if stop_bits=='1':
        stop_bits = serial.STOPBITS_ONE
    if stop_bits=='2':
        stop_bits= serial.STOPBITS_TWO
    timeout = cb4['values'][cb4.current()]
    parity= cb5['values'][cb5.current()]
    if parity == 'Brak':
        parity = serial.PARITY_NONE
    if parity == 'Tak':
        parity = serial.PARITY_EVEN
    if parity == 'Nie':
        parity = serial.PARITY_ODD
    if timeout== 'Brak':
        timeout= None


    print(port)

    ser = serial.Serial(port, baudrate=float(baudrate), timeout=float(timeout), bytesize=float(byte_size),stopbits=float(stop_bits), parity= parity)
    t = threading.Thread(target=serial_read_thread, args=(ser,))
    t.start()

def zapis():
    global filename
    f= filedialog.asksaveasfile(initialfile='Bez tytulu.txt', mode= 'w', defaultextension=".txt")
    filename= f.name
    if f is None:
        return
    global dane
    f.write(dane)
    f.close()
    zestawienie()
def zestawienie():
    global filename

    results = []
    sequence_name = None
    with open(filename, 'r') as file:
        previous_line = ""
        last_line = ""
        for line in file:
            if not line.strip():
                continue
            if sequence_name is None and "Poczatek ciagu" in line:
                next_line = file.readline()
                if not next_line.strip():
                    next_line = file.readline()
                sequence_name = next_line.split()[2]
                rep_pocz= next_line.split()[1]
            elif "Koniec ciagu" in line:
                rep_kon = last_line.split()[-9]
                elevation = float(previous_line.split()[-5])
                length = float(last_line.split()[-5]) + float(last_line.split()[-3])
                results.append([sequence_name, rep_pocz, rep_kon, elevation, length])
                sequence_name = None
                data= len(results)
            previous_line = last_line
            last_line = line
        lista=[]

        for k in range(0,data):
            lista.append(k+1)
        df = pd.DataFrame(results, columns=["Odcinek:","Reper Początkowy:", "Reper Końcowy:", "Przewyższenie: ", "Długość: "], index=lista)
        console.insert("end", str(df), "color_text")
        console.see("end")


#Frames
frame=LabelFrame(window)
frame.grid(row=0,column=2)




#Labels
label= Label(frame, text='Odbieranie danych z instrumentu',font = ("Times New Roman", 20), width=40)
label.grid(row=0, columnspan=2,sticky='N')
label1= Label(frame,text='Wybierz port:', font = ("Times New Roman", 10))
label1.grid(row=1,column=0)
label2= Label(frame,text='Szybkość transmisji:', font = ("Times New Roman", 10))
label2.grid(row=2,column=0)
label3= Label(frame,text='Bity danych:', font = ("Times New Roman", 10))
label3.grid(row=3,column=0)
label4= Label(frame,text='Bity stopu:', font = ("Times New Roman", 10))
label4.grid(row=4,column=0)
label5= Label(frame,text='Timeout:', font = ("Times New Roman", 10))
label5.grid(row=5,column=0)
label6= Label(frame,text='Kontrola parzystości', font = ("Times New Roman", 10))
label6.grid(row=6,column=0)


#Text
console = tkst.ScrolledText(frame, height=28, width=85)
console.grid(row=7,columnspan=2, column=0, pady=5)
console.tag_configure("color_text", foreground=color)

#Comboboxes
var= StringVar()
wart=['COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10','COM11','COM12','COM13','COM14','COM15','COM16','COM17','COM18','COM19','COM20','COM21','COM22','COM23','COM24','COM25']
cb= ttk.Combobox(frame, textvariable=var)
cb['values']= wart
cb['state']= 'readonly'
cb.current(0)
cb.grid(column=1, row=1, pady=5)


var1= StringVar()
wart1=['1200','2400','4800','9600','14400','19200','28800','38400','57600','115200','230400']
cb1= ttk.Combobox(frame, textvariable=var1)
cb1['values']= wart1
cb1['state']= 'readonly'
cb1.current(3)
cb1.grid(column=1, row=2, pady=5)

var2= StringVar()
wart2=['5','6','7','8']
cb2= ttk.Combobox(frame, textvariable=var2)
cb2['values']= wart2
cb2['state']= 'readonly'
cb2.current(3)
cb2.grid(column=1, row=3, pady=5)

var3= StringVar()
wart3=['1','2']
cb3= ttk.Combobox(frame, textvariable=var3)
cb3['values']= wart3
cb3['state']= 'readonly'
cb3.current(0)
cb3.grid(column=1, row=4, pady=5)


var4= StringVar()
wart4=['Brak','0.5','0.75','1','2']
cb4= ttk.Combobox(frame, textvariable=var4)
cb4['values']= wart4
cb4['state']= 'readonly'
cb4.current(3)
cb4.grid(column=1, row=5, pady=5)

var5= StringVar()
wart5=['Brak','Tak','Nie']
cb5= ttk.Combobox(frame, textvariable=var5)
cb5['values']= wart5
cb5['state']= 'readonly'
cb5.current(0)
cb5.grid(column=1, row=6, pady=5)
#Buttons
zacznij= Button(frame, text='Rozpocznij:', width= 20,command=serialf)
zacznij.grid(row=8,column=0)

zakoncz=Button(frame, text="Zakończ: ", width=20,command=stops)
zakoncz.grid(row=8,column=1)

color=Button(frame, text='Wybierz kolor', width=20,command=colors)
color.grid(row=9,column=0)


Zapisz=Button(frame,text='Pokaż zestawienie', width=20, command=zapis)
Zapisz.grid(row=10,column=0)

Wyslij=Button(frame,text='Wyślij dane', width=20, command=run_program)
Wyslij.grid(row=10,column=1)




#Entries
kolorek= Entry(frame, width=20)
kolorek.grid(row=9, column=1)
kolorek.config(bg='black')


window.mainloop()