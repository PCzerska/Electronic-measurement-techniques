from tkinter import *
from tkinter import ttk
import serial
import csv
import time
import threading
from tkinter import colorchooser
from tkinter import filedialog
import tkinter.scrolledtext as tkst
window = Tk()
window.title("Paulina Czerska GI")
window.geometry('600x407')
window.configure(background='#FFFAF0')
color='black'
ser=None
k=[]
def colors():
    global color
    x = colorchooser.askcolor()[1]
    color = x
    if color!= None:
        kolorek.config(bg=color)
        tks.configure(fg=color)
    return color

def wybierz():
    global k
    plik = filedialog.askopenfilename()
    with open(plik, "r", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=";")
        for line in reader:
            if line != '':
                k.append(','.join(line))
    print(k)

def port():
    global ser
    port = cb['values'][cb.current()]
    baudrate = cb1['values'][cb1.current()]
    byte_size = cb2['values'][cb2.current()]
    if byte_size == '5':
        byte_size = serial.FIVEBITS
    if byte_size == '6':
        byte_size = serial.SIXBITS
    if byte_size == '7':
        byte_size = serial.SEVENBITS
    if byte_size == '8':
        byte_size = serial.EIGHTBITS
    stop_bits = cb3['values'][cb3.current()]
    if stop_bits == '1':
        stop_bits = serial.STOPBITS_ONE
    if stop_bits == '2':
        stop_bits = serial.STOPBITS_TWO
    timeout = cb4['values'][cb4.current()]
    parity = cb5['values'][cb5.current()]
    if parity == 'Brak':
        parity = serial.PARITY_NONE
    if parity == 'Tak':
        parity = serial.PARITY_EVEN
    if parity == 'Nie':
        parity = serial.PARITY_ODD
    if timeout== 'Brak':
        timeout= None
    ser = serial.Serial(port, baudrate=float(baudrate), timeout=float(timeout), bytesize=int(byte_size), stopbits=float(stop_bits), parity=parity)
def wyslij():
    global ser
    text = tks.get() + '\n'
    text_bytes = text.encode()
    ser.write(text_bytes)

def wyslij2():
    global ser
    for ev in k:
        ev.split(';')
        for i in ev:
            text_bytes = str(i).encode()
            ser.write(text_bytes)


#Frames
frame=LabelFrame(window)
frame.grid(row=0,column=2)




#Labels
label= Label(frame, text='Wysyłanie danych do instrumentu',font = ("Times New Roman", 20), width=40)
label.grid(row=0, columnspan=2,sticky='N')
label1= Label(frame,text='Wybierz port:', font = ("Times New Roman", 10))
label1.grid(row=1,column=0)
label3= Label(frame,text='Wpisz dane do wysłania:', font = ("Times New Roman", 15))
label3.grid(row=9,column=0, columnspan=2,pady=10)

label4= Label(frame,text='Szybkość transmisji:', font = ("Times New Roman", 10))
label4.grid(row=3,column=0)
label5= Label(frame,text='Bity danych:', font = ("Times New Roman", 10))
label5.grid(row=4,column=0)
label6= Label(frame,text='Bity stopu:', font = ("Times New Roman", 10))
label6.grid(row=5,column=0)
label7= Label(frame,text='Timeout:', font = ("Times New Roman", 10))
label7.grid(row=6,column=0)
label8= Label(frame,text='Kontrola parzystości', font = ("Times New Roman", 10))
label8.grid(row=7,column=0)




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
cb1.grid(column=1, row=3, pady=5)

var2= StringVar()
wart2=['5','6','7','8']
cb2= ttk.Combobox(frame, textvariable=var2)
cb2['values']= wart2
cb2['state']= 'readonly'
cb2.current(3)
cb2.grid(column=1, row=4, pady=5)

var3= StringVar()
wart3=['1','2']
cb3= ttk.Combobox(frame, textvariable=var3)
cb3['values']= wart3
cb3['state']= 'readonly'
cb3.current(0)
cb3.grid(column=1, row=5, pady=5)


var4= StringVar()
wart4=['Brak','0.5','0.75','1','2']
cb4= ttk.Combobox(frame, textvariable=var4)
cb4['values']= wart4
cb4['state']= 'readonly'
cb4.current(3)
cb4.grid(column=1, row=6, pady=5)

var5= StringVar()
wart5=['Brak','Tak','Nie']
cb5= ttk.Combobox(frame, textvariable=var5)
cb5['values']= wart5
cb5['state']= 'readonly'
cb5.current(0)
cb5.grid(column=1, row=7, pady=5)

#Entries
kolorek= Entry(frame, width=20)
kolorek.grid(row=2,column=1)
kolorek.config(bg='black')

tks= Entry(frame, width=50)
tks.grid(row=10,column=0,pady=5)

#Buttons
color= Button(frame,text='Wybierz kolor',command=colors)
color.grid(row=2,column=0)

otworz= Button(frame,text='Otwórz port', command=port)
otworz.grid(row=10,column=1)

wyslij= Button(frame,text='Wyślij',command=wyslij)
wyslij.grid(row=11,column=1)

wyslijplik= Button(frame, text='Wyślij plik csv', command=wyslij2)
wyslijplik.grid(row=12, column=1)

wybierz= Button(frame,text='Wybierz plik csv do wysłania', command=wybierz)
wybierz.grid(row=13,column=0)
window.mainloop()

