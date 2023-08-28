from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import filedialog
import numpy as np
file=0
window = Tk()
window.title("Paulina Czerska  GI")
window.geometry('1425x800')
notebook = ttk.Notebook(window)
tab1 = Frame(notebook, bg= "pink")
tab2 = Frame(notebook, bg="#a7ccf6")
tab3 = Frame(notebook, bg='#b7d5ac')
notebook.add(tab1, text="Współczynnik załamania")
notebook.add(tab2, text="Liczenie")
notebook.add(tab3, text="Wpływ zakrzywienia fali elektromagnetycznej")
notebook.pack(expand=True, fill= "both")



#Zakładka 1
#Tworzenie listy z długościami fal
lam=[]
for i in range(400,1101,10):
    lam.append(i)
    i=i+10
#print(lam)
N=[]
n=[]
for ev in lam:
    temp=287.6155 + (4.8866/((ev/1000)**2)) + (0.0680/((ev/1000)**4))
    N.append(temp)
    n.append((temp/1000000)+1)

frame1= Canvas(tab1,width=800, height= 600)
frame1.pack()

#Pierwszy wykres
fig=plt.figure(figsize=(7, 5))
canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.get_tk_widget().pack(side=LEFT)
plt.title("Wykres zależnośći Ng od długości fali w atmosferze normalnej")
plt.xlabel("Długość fali w nanometrach:")
plt.ylabel("Wartość współczynnika:")
plt.plot(lam,N,color='#DC143C')
canvas.draw()

#Drugi wykres
fig1=plt.figure(figsize=(7, 5))
canvas = FigureCanvasTkAgg(fig1, master=frame1)
canvas.get_tk_widget().pack(side=RIGHT)
plt.title("Wykres zależności ng od długości fali w watmosferze normalnej\n")
plt.xlabel("Długość fali w nanometrach:")
plt.ylabel("Wartość współczynnika:")
plt.plot(lam,n,color='#7FFFD4')
canvas.draw()


ar=[]
for a in range(0,len(lam)):

    ar.append([lam[a], N[a], n[a]])

def table1():
    tbl = ttk.Frame(tab1)
    tbl.pack(anchor='nw', side='left', ipadx=10, ipady=10, padx=10, pady=10)


    wnd = ttk.Treeview(tbl)

    # scrollbar

    game_scroll = Scrollbar(tbl)
    game_scroll.pack(side='right', fill='y')

    wnd = ttk.Treeview(tbl, yscrollcommand=game_scroll.set)
    wnd.pack()

    game_scroll.config(command=wnd.yview)

    # define columns
    wnd['columns'] = ('dl_fali', 'Ng', 'ng')

    # formating columns
    wnd.column("#0", width=0, stretch= NO)
    wnd.column("dl_fali", anchor='center', width=500)
    wnd.column("Ng", anchor='center', width=500)
    wnd.column("ng", anchor='center', width=500)

    # create headings
    wnd.heading("#0", text="", anchor='center')
    wnd.heading("dl_fali", text="Długość fali w nanometrach", anchor='center')
    wnd.heading("Ng", text="Ng", anchor='center')
    wnd.heading("ng", text="ng", anchor='center')

    # adding data
    Ng, ng, rn= N,n,lam
    for i in range(len(Ng)):
        wnd.insert(parent='', index='end', text='', values=(rn[i], Ng[i], ng[i]))

    wnd.pack()

table1()


#Druga zakładka
ramka=LabelFrame(tab2, width=400,height=200)
ramka.pack(side=LEFT, anchor='nw')
lbl1= Label(ramka, text='Długość fali w nanometrach:',font='10')
lbl1.pack()
txt1= Entry(ramka)
txt1.pack()

lbl2=Label(ramka, text='Temperatura sucha w Celsjuszach:',font='10')
lbl2.pack()
txt2=Entry(ramka)
txt2.pack()

lbl3=Label(ramka, text='Temperatura mokra w Celsjuszach:',font='10')
lbl3.pack()
txt3=Entry(ramka)
txt3.pack()

lbl4=Label(ramka, text='Ciśnienie w hPa:',font='10')
lbl4.pack()
txt4=Entry(ramka)
txt4.pack()

lbl5=Label(ramka, text='Pomierzona długość w metrach:',font='10')
lbl5.pack()
txt5=Entry(ramka)
txt5.pack()

lbl6=Label(ramka, text='',font='10')
lbl6.pack()
lbl7=Label(ramka, text='',font='10')
lbl7.pack()

lbl8=Label(ramka, text='Poprawka na km',font='10')
lbl8.pack()
txt8=Entry(ramka,font='10')
txt8.pack()

lbl9=Label(ramka, text='Poprawiony wynik',font='10')
lbl9.pack()
txt9=Entry(ramka,font='10')
txt9.pack()



#Obliczenia
def wczytaj_dane():
    if(float(txt1.get())>0):
        dlfal=float(txt1.get())
    Ts=float(txt2.get())
    Tm=float(txt3.get())
    if(float(txt4.get())>0):
        p= float(txt4.get())
    if(float(txt5.get())>0):
        d= float(txt5.get())
    return dlfal,Ts,Tm,p,d

def obliczenia():
    dlfal,Ts,Tm,p,d=wczytaj_dane()
    dlfal=dlfal/1000

    ps=1013.25
    es=10.87
    T=288.15

    Ewp=6.1078*(2.71828182845904**((17.269*Tm)/(237.30+Tm)))
    e= Ewp - 0.000662*p*(Ts-Tm)

    Ts=Ts+273.15

    Ng0= 287.6155 + (4.8866/(dlfal**2)) + (0.0680/(dlfal**4))
    Ng_r= (Ng0 * 0.269578 * (p/Ts)) - (11.27*e/Ts)
    Ng_s= (Ng0 * 0.269578 * (ps/T)) - (11.27*es/T)
    poprawka= Ng_s -Ng_r
    nowa_poprawka= d/1000000 * poprawka
    wynik=(d+nowa_poprawka)
    wynik=round(wynik,4)
    poprawka=round(poprawka,4)
    txt8.insert(0,str(poprawka))
    txt9.insert(0,str(wynik))

def wczytywanie_pliku():
    global file
    x=filedialog.askopenfilename()
    file=x
    txt10.insert(0, "Plik został wczytany pomyśłnie.")
    return file
def table2(index,poprawka,wyniki):
    tbl = ttk.Frame(tab2)
    tbl.pack(anchor='nw', ipadx=10, ipady=10, padx=100, pady=10)


    wnd = ttk.Treeview(tbl)

    # scrollbar

    game_scroll = Scrollbar(tbl)
    game_scroll.pack(side='right', fill='y')

    wnd = ttk.Treeview(tbl, yscrollcommand=game_scroll.set)
    wnd.pack()

    game_scroll.config(command=wnd.yview)

    # define columns
    wnd['columns'] = ('L_p', 'pop', 'wp')

    # formating columns
    wnd.column("#0", width=0, stretch= NO)
    wnd.column("L_p", anchor='center', width=300)
    wnd.column("pop", anchor='center', width=300,)
    wnd.column("wp", anchor='center', width=300)

    # create headings
    wnd.heading("#0", text="", anchor='center')
    wnd.heading("L_p", text="L.p", anchor='center')
    wnd.heading("pop", text="Poprawka w mm/km", anchor='center')
    wnd.heading("wp", text="Wynik Poprawiony", anchor='center')

    # adding data
    for i in range(len(index)):
        wnd.insert(parent='', index='end', text='', values=(index[i], poprawka[i], wyniki[i]))

    wnd.pack()
def obliczenia_dla_pliku():
    with open(file, 'r') as f:
        i = 0
        size = []
        index = []; Sucha = []; Mokra = []; Cisnienie = []; Dlugosc = []

        for linia in f:
            if linia[0:1] != 'T':
                splited_line = linia.split(';')
                size.append(len(splited_line))
                i += 1
                index.append(int(splited_line[0]))
                Sucha.append(float(splited_line[1]))
                Mokra.append(float(splited_line[2]))
                Cisnienie.append(float(splited_line[3]))
                Dlugosc.append(float(splited_line[4]))

        all_data = np.column_stack((np.array(index),np.array(Sucha),np.array(Mokra),np.array(Cisnienie),np.array(Dlugosc)))
        #print(len(all_data))

    ps = 1013.25
    es = 10.87
    T = 288.15
    poprawka=[]
    wyniki=[]
    for k in range(0,len(all_data)):
        Ewp = 6.1078 * (2.71828182845904 ** ((17.269 * Mokra[k]) / (237.30 + Mokra[k])))
        e = Ewp - 0.000662 * Cisnienie[k] * (Sucha[k] - Mokra[k])
        Sucha[k] = Sucha[k] + 273.15
        Ng0 = 287.6155 + (4.8866 / (Dlugosc[k] ** 2)) + (0.0680 / (Dlugosc[k] ** 4))
        Ng_r = (Ng0 * 0.269578 * (Cisnienie[k] / Sucha[k])) - (11.27 * e / Sucha[k])
        Ng_s = (Ng0 * 0.269578 * (ps / T)) - (11.27 * es / T)
        pop = Ng_s - Ng_r

        nowa_poprawka = Dlugosc[k] / 1000000 * pop
        wynik = Dlugosc[k] + nowa_poprawka
        wynik= round(wynik, 4)
        pop = round(pop, 4)
        poprawka.append(pop)
        wyniki.append(wynik)
    do_tabelki=[('L.p','Poprawka mm/km','Wynik poprawiony')]
    for el in range(0,len(wyniki)):
        do_tabelki.append((index[el],poprawka[el],wyniki[el]))
    table2(index,poprawka,wyniki)

wczytaj= Button(ramka,command=obliczenia, text='Oblicz',width=30,height=3)
wczytaj.pack()


wczytaj_z= Button(tab2, text='Wczytaj z pliku',width=30,height=3,padx=50,command=wczytywanie_pliku)
wczytaj_z.pack(anchor='center')

oblicz_dla_pliku= Button(tab2, text='Oblicz dla pliku',width=30,height=3,padx=50, command= obliczenia_dla_pliku)
oblicz_dla_pliku.pack(padx=50,anchor='center')

txt10= Entry(tab2, width=100)
txt10.pack(anchor='n',pady=50)

#Zakładka 3
r= 8*6372.00
dlugosci=[]
for dll in range(1,101):
    dlugosci.append(dll)
ostw=[]
for ev in dlugosci:
    ost= (-(ev)**3)/(24*(r**2))

    ostw.append(ost*1000000)

fig3=plt.figure(figsize=(8,5))
canvas3 = FigureCanvasTkAgg(fig3, master=tab3)
canvas3.get_tk_widget().pack(anchor='n')
plt.title('Wykres wpływu zakrzywienia fali elektromagnetycznej w zależności od długości łuku:\n')
plt.plot(dlugosci,ostw, color='green')
plt.xlabel('Długość łuku w kilometrach:')
plt.ylabel('Różnica między łukiem a cięciwą w mm:')

def table3(ostw,dl):
    tbl = ttk.Frame(tab3)
    tbl.pack(anchor='center', pady=50)


    wnd = ttk.Treeview(tbl)

    # scrollbar

    game_scroll = Scrollbar(tbl)
    game_scroll.pack(side='right', fill='y')

    wnd = ttk.Treeview(tbl, yscrollcommand=game_scroll.set)
    wnd.pack()

    game_scroll.config(command=wnd.yview)

    # define columns
    wnd['columns'] = ('Dl', 'wp')

    # formating columns
    wnd.column("#0", width=0, stretch= NO)
    wnd.column("Dl", anchor='center', width=600)
    wnd.column("wp", anchor='center', width=600)


    # create headings
    wnd.heading("#0", text="", anchor='center')
    wnd.heading("Dl", text="Długość łuku w km", anchor='center')
    wnd.heading("wp", text="Wpływ zakrzywienia w mm", anchor='center')


    # adding data
    for i in range(len(ostw)):
        wnd.insert(parent='', index='end', text='', values=(dl[i],ostw[i]))

    wnd.pack()

table3(ostw,dlugosci)
window.mainloop()
