__author__ = 'Jojo'
import numpy as np
import math


def RS(Price):
    if len(Price) < 2:
        return 0
    Price = np.array(Price)
    n = len(Price)
    m = np.mean(Price)
    Y = Price - m
    Z = np.arange(n, dtype=float)
    for i in range(n):
        Z[i] = sum(Y[:i])
    R = max(Z) - min(Z)
    S = np.sqrt(np.var(Price))
    return R / S

def Hurst(Price):
    n = len(Price)
    times = int(math.log(n))
    x = []
    y = []
    price = Price
    for i in range(times):
        if(n > 4):
            x.append(n)
            y.append(RS(price[:n]))
        n = int(n / 2)
        Price_n = np.arange(n, dtype=float)
        for index in range(n):
            Price_n[index] = (price[2 * index] + price[2 * index + 1]) / 2
        price = Price_n
    print x, y
    k = np.polyfit(np.log(x), np.log(y), 1)
    return k[0]