# -*- coding:utf-8 -*-
__author__ = 'Jojo'

from Tkinter import *
from Indicator import *

def Draw():
    plotchart(type, startime, endtime)

root = Tk()
Label(root, text="Plot Place Holder").grid(row=0, columnspan=3)

Label(root, text="Forex Type").grid(row=1, column=0)
typeentry = Entry(root)
typeentry.grid(row=1, column=1)
typeentry.insert(0, 'XAUUSD')
try:
    type = typeentry.get()
except:
    type = "XAUUSD"

Label(root, text="startime").grid(row=2, column=0)
startimeentry = Entry(root)
startimeentry.grid(row=2, column=1)
startimeentry.insert(0, '20020101')
try:
    startime = str(startimeentry.get())
except:
    startime = "20020101"

Label(root, text="endtime").grid(row=3, column=0)
endtimeentry = Entry(root)
endtimeentry.grid(row=3, column=1)
endtimeentry.insert(0, '20150501')
try:
    endtime = str(endtimeentry.get())
except:
    endtime = "20150501"

Button(root, text="Draw", command=Draw).grid(row=1, column=2, rowspan=3)
chkBtnVar = IntVar()
chkBtn = Checkbutton(root, text="Model Tree", variable=chkBtnVar)
chkBtn.grid(row=4, column=0, columnspan=2)
root.mainloop()