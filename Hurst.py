__author__ = 'Jojo'
import math
from FkNN import *


# Calculate the Hurst exponent
# *** a list of Hurst ***
def Hurst(Price):
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
    n = len(Price)
    times = int(math.log(n) / math.log(2))
    x = []
    y = []
    price = Price
    for i in range(times):
        if(n > 2):
            x.append(n)
            y.append(RS(price[:n]))
        n = int(n / 2)
        Price_n = np.arange(n, dtype=float)
        for index in range(n):
            Price_n[index] = (price[2 * index] + price[2 * index + 1]) / 2
        price = Price_n
    k = np.polyfit(np.log(x), np.log(y), 1)
    return k[0]


# Transform the Price data into Hurst Data
# *** a list of UTC and a list of Hurstvalue ***
def data2hurst(UTC, Price, prange):
    prange = int(prange)
    p = len(UTC) / prange
    p = int(p)
    Hurstvalue = np.arange(0, p+1, dtype=float)
    for i in range(p):
        Hurstvalue[i] = Hurst(Price[i*prange:(i+1)*prange])
    Hurstvalue[p] = Hurst(Price[p*prange:])
    x = np.arange(p+1)
    HurstUTC = np.arange(len(x))
    for i in range(len(x)):
        HurstUTC[i] = UTC[i * prange]
    return HurstUTC, Hurstvalue


def data2hurst2(UTC, Price, prange):
    Hurstvalue = np.arange(0, len(Price), dtype=float)
    for i in range(len(Price)):
        if i < prange:
            Hurstvalue[i] = 0
        else:
            Hurstvalue[i] = Hurst(Price[i + 1 - prange: i + 1])
    return Hurstvalue


if version == -1:
    # Plot the Price-UTC chart and Hurst-UTC chart
    # *** No return ***
    def plotprice_hurst(type, startime, endtime, prange):
        Time, UTC, Price = input2data("UTC" + type[-6:], startime, endtime)
        HurstTime, Hurstvalue = data2hurst(UTC, Price, prange)
        fp = type[-6:] + "_" + str(Time[0][0:8]) + "_" + str(Time[-1][0:8])

        #**********************************************************
        fig = plt.figure(figsize=(16, 12), dpi=84, facecolor="white")
        axes = plt.subplot(211)
        axes.cla() # Clear all the information in the coordinate
        # Assign the font of the picture
        font = {'family' : 'serif',
                'color'  : 'darkred',
              'weight' : 'normal',
               'size'   : 16,
              }
        #**********************************************************
        plt.plot(UTC, Price)
        # Configurate the scale of the coordinate
        ax1 = plt.gca()
        interval = int(len(Price) / 5)
        ax1.set_xticks(np.linspace(UTC[0], UTC[-1], 5))
        ax1.set_xticklabels((Time[0][0:8], Time[interval][0:8], Time[2*interval][0:8], Time[3*interval][0:8], Time[-1][0:8]))
        ax1.set_yticks(np.linspace(min(Price), max(Price), 8))
        #ax.set_yticklabels( ('500', '800', '1100', '1400', '1700','2000'))
        # Configurate the labels
        ylabel = "The international gold price"
        ax1.set_ylabel(ylabel, fontdict=font)
        ax1.grid(True)

        #**********************************************************
        axes = plt.subplot(212)
        plt.plot(HurstTime, Hurstvalue)
        # Configurate the scale of the coordinate
        ax2 = plt.gca()
        ax2.set_xticks(np.linspace(HurstTime[0], HurstTime[-1], 5))
        ax2.set_xticklabels((Time[0][0:8], Time[interval][0:8], Time[2*interval][0:8], Time[3*interval][0:8], Time[-1][0:8]))
        ax2.set_yticks(np.linspace(min(Hurstvalue), max(Hurstvalue), 8))
        #ax.set_yticklabels( ('500', '800', '1100', '1400', '1700','2000'))
        # Configurate the labels
        xlabel = "The day from " + str(Time[0][0:8]) + " to " + str(Time[-1][0:8])
        ylabel = "The Hurst Value"
        ax2.set_ylabel(ylabel, fontdict=font)
        ax2.set_xlabel(xlabel, fontdict=font)
        ax2.grid(True)

        # Configurate the title
        figname = fp+'.png'
        try:
            os.mkdir('../Pictures/')
            plt.savefig('../Pictures/'+ figname)
        except:
            plt.savefig('../Pictures/'+ figname)
        # savefig('../figures/contour_ex.png',dpi=48)
        #plt.clf() # Clear the chart
        #plt.show()
        print('ALL -> Finished OK')
        plt.show()


    def plotprice_hurst3(type, startime, endtime, prange):
        Time, UTC, Price = input2data("UTC" + type[-6:], startime, endtime)
        Hurstvalue = data2hurst2(UTC, Price, prange)
        Hurstvalue = [(max(Price) -min(Price)) * i + min(Price) for i in Hurstvalue]

        fp = type[-6:] + "_" + str(Time[0][0:8]) + "_" + str(Time[-1][0:8])

        #**********************************************************
        fig = plt.figure(figsize=(16, 12), dpi=84, facecolor="white")
        axes = plt.subplot(211)
        axes.cla() # Clear all the information in the coordinate
        # Assign the font of the picture
        font = {'family' : 'serif',
                'color'  : 'darkred',
              'weight' : 'normal',
               'size'   : 16,
              }
        #**********************************************************
        plt.plot(UTC, Price)
        plt.plot(UTC, Hurstvalue)
        # Configurate the scale of the coordinate
        ax1 = plt.gca()
        interval = int(len(Price) / 5)
        ax1.set_xticks(np.linspace(UTC[0], UTC[-1], 5))
        ax1.set_xticklabels((Time[0][0:8], Time[interval][0:8], Time[2*interval][0:8], Time[3*interval][0:8], Time[-1][0:8]))
        ax1.set_yticks(np.linspace(min(Price), max(Price), 8))
        #ax.set_yticklabels( ('500', '800', '1100', '1400', '1700','2000'))
        # Configurate the labels
        ylabel = "The international gold price"
        ax1.set_ylabel(ylabel, fontdict=font)
        ax1.grid(True)

        # Configurate the title
        figname = fp+'.png'
        try:
            os.mkdir('../Pictures/')
            plt.savefig('../Pictures/'+ figname)
        except:
            plt.savefig('../Pictures/'+ figname)
        # savefig('../figures/contour_ex.png',dpi=48)
        #plt.clf() # Clear the chart
        #plt.show()
        print('ALL -> Finished OK')
        plt.show()


    def plotprice_hurst2(type, startime, endtime, prange):
        Time, UTC, Price = input2data("UTC" + type[-6:], startime, endtime)
        Hurstvalue = data2hurst2(UTC, Price, prange)
        fp = type[-6:] + "_" + str(Time[0][0:8]) + "_" + str(Time[-1][0:8])

        #**********************************************************
        fig = plt.figure(figsize=(16, 12), dpi=84, facecolor="white")
        axes = plt.subplot(211)
        axes.cla() # Clear all the information in the coordinate
        # Assign the font of the picture
        font = {'family' : 'serif',
                'color'  : 'darkred',
              'weight' : 'normal',
               'size'   : 16,
              }
        #**********************************************************
        plt.plot(UTC, Price)
        # Configurate the scale of the coordinate
        ax1 = plt.gca()
        interval = int(len(Price) / 5)
        ax1.set_xticks(np.linspace(UTC[0], UTC[-1], 5))
        ax1.set_xticklabels((Time[0][0:8], Time[interval][0:8], Time[2*interval][0:8], Time[3*interval][0:8], Time[-1][0:8]))
        ax1.set_yticks(np.linspace(min(Price), max(Price), 8))
        #ax.set_yticklabels( ('500', '800', '1100', '1400', '1700','2000'))
        # Configurate the labels
        ylabel = "The international gold price"
        ax1.set_ylabel(ylabel, fontdict=font)
        ax1.grid(True)

        #**********************************************************
        axes = plt.subplot(212)
        plt.plot(UTC, Hurstvalue)
        # Configurate the scale of the coordinate
        ax2 = plt.gca()
        ax2.set_xticks(np.linspace(UTC[0], UTC[-1], 5))
        ax2.set_xticklabels((Time[0][0:8], Time[interval][0:8], Time[2*interval][0:8], Time[3*interval][0:8], Time[-1][0:8]))
        ax2.set_yticks(np.linspace(min(Hurstvalue), max(Hurstvalue), 8))
        #ax.set_yticklabels( ('500', '800', '1100', '1400', '1700','2000'))
        # Configurate the labels
        xlabel = "The day from " + str(Time[0][0:8]) + " to " + str(Time[-1][0:8])
        ylabel = "The Hurst Value"
        ax2.set_ylabel(ylabel, fontdict=font)
        ax2.set_xlabel(xlabel, fontdict=font)
        ax2.grid(True)

        # Configurate the title
        figname = fp+'.png'
        try:
            os.mkdir('../Pictures/')
            plt.savefig('../Pictures/'+ figname)
        except:
            plt.savefig('../Pictures/'+ figname)
        # savefig('../figures/contour_ex.png',dpi=48)
        #plt.clf() # Clear the chart
        #plt.show()
        print('ALL -> Finished OK')
        plt.show()
