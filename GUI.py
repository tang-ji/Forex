# -*- coding:utf-8 -*-
__author__ = 'Jojo'

from Tkinter import *
from Forex import *

def Drawchart():
    charttype = Lb.get(Lb.curselection())
    try:
        forextype = str(typeentry.get())
    except:
        forextype = "XAUUSD"
    try:
        startime = str(startimeentry.get())
    except:
        startime = "20020101"
    try:
        endtime = str(endtimeentry.get())
    except:
        endtime = "20150501"
    try:
        Period = Periodentry.get()
    except:
        Period = "30"
    plotchart(charttype, forextype, startime, endtime, Period)

root = Tk()
root.geometry('270x350')
# Set the title of the frame
root.title("Plot Forex Chart")
Label(root, text="Plot Place Holder").grid(row=0, columnspan=3)

Label(root, text="Forex Type").grid(row=1, column=0)
typeentry = Entry(root)
typeentry.grid(row=1, column=1)
typeentry.insert(0, 'XAUUSD')


Label(root, text="startime").grid(row=2, column=0)
startimeentry = Entry(root)
startimeentry.grid(row=2, column=1)
startimeentry.insert(0, '20020101')


Label(root, text="endtime").grid(row=3, column=0)
endtimeentry = Entry(root)
endtimeentry.grid(row=3, column=1)
endtimeentry.insert(0, '20150501')


Label(root, text="Period").grid(row=4, column=0)
Periodentry = Entry(root)
Periodentry.grid(row=4, column=1)
Periodentry.insert(0, '30')


Button(root, text="Draw", command=Drawchart).grid(row=1, column=2, rowspan=3)
var = StringVar()
var.set(("Price", "Hurst", "MVA", "BOLL"))
Lb = Listbox(root, listvariable=var)
Lb.grid(row=5, column=0, rowspan=10, columnspan=3)

root.mainloop()