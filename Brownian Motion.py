# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

step = 0
numInMin = 60
p0 = 100.00  # Set the initial price
p = p0
pE = p0
percent = 0.1
T = numInMin * 100  #Total steps
uOrD = 0
rand = 0
crit = 0
ERROR = 0.001
memory = 10
history = np.tile(p0, (1, memory))
oneDay = numInMin * 240
recordFreq = numInMin * 1000
price = []
priceTemp = step / 60
printTemp = 0
totalstep = []

while(step < T):
    step += 1
    totalstep.append(step)
    price.append(p)
    crit = p / (2 * pE)
    rand = np.random.rand()
    if(rand < crit):
        uOrD = -1
    else:
        uOrD = 1
    p = p + uOrD * percent

    pE = np.mean(history)
    history = np.delete(history, 0)
    history = np.append(history, p)

fig = plt.figure(figsize=(8, 6), dpi=84, facecolor="white")
plt.plot(totalstep, price)
plt.show()
