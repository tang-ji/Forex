# code: UTF-8
__author__ = 'Jojo'
from FkNN import *
from changetime import *


datapath = os.getcwd() + "BuildData\\"

# Calculate the moving average line of each period
# *** a matrix of MVA and a list of Period ***
def MVA(UTC, Price, Period):
    period = [int(i) for i in Period.split(',')]
    number = len(period)
    MVAPrice = []
    for i in range(number):
        MVAi = []
        for j in range(len(UTC)):
            if j + 1 < period[i]:
                MVAi.append(np.mean(Price[:j + 1]))
            else:
                MVAi.append(np.mean(Price[j + 1 - period[i]:j + 1]))
        MVAPrice.append(MVAi)
    return MVAPrice, period


# Calculate the moving average line of each period
# *** a matrix of MVA, a 3D-matrix of BOLL and a list of Period ***
def BOLL(UTC, Price, Period):
    MVAPrice, period = MVA(UTC, Price, Period)
    number = len(period)
    BOLLline = []
    for i in range(number):
        BOLLclass = []
        for j in range(len(UTC)):
            line = []
            if j + 1 < period[i]:
                MVAi = np.mean(Price[:j + 1])
                VARi = np.var(Price[:j + 1])
            else:
                MVAi = np.mean(Price[j + 1 - period[i]:j + 1])
                VARi = np.var(Price[j + 1 - period[i]:j + 1])
            line.append(MVAi + 2 * math.sqrt(VARi))
            line.append(MVAi - 2 * math.sqrt(VARi))
            BOLLclass.append(line)
        BOLLline.append(BOLLclass)
    return MVAPrice, BOLLline, period


# To calculate the moving average value and BOLL values and store it to the "datapath"
# *** No return ***
def saveBOLL(type, startime, endtime, Period):
    if Period[0] == "D":
        Period = str(int(Period[1:]) * 864000)
    if Period[0] == "H":
        Period = str(int(Period[1:] * 3600))
    startime = int(time.mktime(time.strptime(startime, "%Y%m%d"))) - max([int(i) for i in Period.split(',')])
    startime = time.strftime("%Y%m%d", time.localtime(startime))
    Time, UTC, Price = input2data("UTC" + type[-6:], startime, endtime)
    MVAPrice, BOLLline, period = BOLL(UTC, Price, Period)
    UTC = UTC[max(period):]
    Time = Time[max(period):]
    Price = Price[max(period):]
    MVAPrice = np.array(MVAPrice)[:, max(period):]
    BOLLline = np.array(BOLLline)[:, max(period):]
    filename = type[-6:] + startime + "_" + endtime + "_BOLL" + Period + ".txt"
    returnfile = open(datapath + filename, "w")
    for index in range(len(UTC)):
        returnfile.write(str(Time[index]) + "," + str(UTC[index]) + "," + str(Price[index]) + ","\
                         + str(MVAPrice[0][index]) + "," + str(BOLLline[0][index, 0]) + "," +\
                         str(BOLLline[0][index, 1]) + "\n")
    returnfile.close()


if version == -1:
    # Plot the MVA line
    # *** No return ***
    def plotMVAdata(Time, UTC, Price, MVAPrice, period, name):
        fp = name + "_" + str(Time[0][0:8]) + "_" + str(Time[-1][0:8])
        number = len(MVAPrice)

        # **********************************************************
        fig = plt.figure(figsize=(16, 12), dpi=84, facecolor="white")
        axes = plt.subplot(111)
        axes.cla()  # Clear all the information in the coordinate
        # Assign the font of the picture
        font = {'family' : 'serif',
                'color'  : 'darkred',
              'weight' : 'normal',
               'size'   : 18,
              }
        # **********************************************************
        ax = plt.gca()
        # Set the figure legend labels
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)

        plt.plot(UTC, Price, "k", label="Price")

        for i in range(number):
            plt.plot(UTC, MVAPrice[i], label="MVA" + str(period[i]))

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        # Configurate the scale of the coordinate
        interval = int(len(Price) / 5)
        ax.set_xticks(np.linspace(UTC[0], UTC[-1], 5))
        ax.set_xticklabels((Time[0][0:8], Time[interval][0:8], Time[2*interval][0:8], Time[3*interval][0:8], Time[-1][0:8]))
        ax.set_yticks(np.linspace(min(Price), max(Price), 8))
        #ax.set_yticklabels(('500', '800', '1100', '1400', '1700','2000'))
        # Configurate the labels
        xlabel = "The day from " + str(Time[0][0:8]) + " to " + str(Time[-1][0:8])
        ylabel = "The price of the international gold"
        ax.set_ylabel(ylabel, fontdict=font)
        ax.set_xlabel(xlabel, fontdict=font)
        ax.grid(True)
        # Configurate the title
        titleStr = 'The Price of Gold '
        plt.title(titleStr)
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


    # To plot the MVA chart in the giving time for the giving type
    # *** No return ***
    def plotMVA(type, startime, endtime, Period):
        startime = int(time.mktime(time.strptime(startime, "%Y%m%d"))) - max([int(i) for i in Period.split(',')])
        startime = time.strftime("%Y%m%d", time.localtime(startime))
        Time, UTC, Price = input2data("UTC" + type[-6:], startime, endtime)
        MVAPrice, period = MVA(UTC, Price, Period)
        UTC = UTC[max(period):]
        Time = Time[max(period):]
        Price = Price[max(period):]
        MVAPrice = np.array(MVAPrice)[:, max(period):]
        plotMVAdata(Time, UTC, Price, MVAPrice, period, type[-6:])


    # Plot the BOLL line
    # *** No return ***
    def plotBOLLdata(Time, UTC, Price, MVAPrice, BOLLline, period, name):
        fp = name + "_" + str(Time[0][0:8]) + "_" + str(Time[-1][0:8])
        number = len(MVAPrice)

        # **********************************************************
        fig = plt.figure(figsize=(16, 12), dpi=84, facecolor="white")
        axes = plt.subplot(111)
        axes.cla()  # Clear all the information in the coordinate
        # Assign the font of the picture
        font = {'family' : 'serif',
                'color'  : 'darkred',
              'weight' : 'normal',
               'size'   : 18,
              }
        # **********************************************************
        ax = plt.gca()
        # Set the figure legend labels
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        plt.plot(UTC, Price, "k", label="Price")
        for i in range(number):
            plt.plot(UTC, MVAPrice[i], label="MVA" + str(period[i]))

        BOLLline = np.array(BOLLline)
        for i in range(number):
            plt.plot(UTC, BOLLline[i][:, 0], UTC, BOLLline[i][:, 1], label="BOLL" + str(period[i]))

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        # Configurate the scale of the coordinate
        interval = int(len(Price) / 5)
        ax.set_xticks(np.linspace(UTC[0], UTC[-1], 5))
        ax.set_xticklabels((Time[0][0:8], Time[interval][0:8], Time[2*interval][0:8], Time[3*interval][0:8], Time[-1][0:8]))
        ax.set_yticks(np.linspace(min(Price), max(Price), 8))
        #ax.set_yticklabels(('500', '800', '1100', '1400', '1700','2000'))
        # Configurate the labels
        xlabel = "The day from " + str(Time[0][0:8]) + " to " + str(Time[-1][0:8])
        ylabel = "The price of the international gold"
        ax.set_ylabel(ylabel, fontdict=font)
        ax.set_xlabel(xlabel, fontdict=font)
        ax.grid(True)
        # Configurate the title
        titleStr = 'The Price of Gold '
        plt.title(titleStr)
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


    # To plot the BOLL chart in the giving time for the giving type
    # *** No return ***
    def plotBOLL(type, startime, endtime, Period):
        startime = int(time.mktime(time.strptime(startime, "%Y%m%d"))) - max([int(i) for i in Period.split(',')])
        startime = time.strftime("%Y%m%d", time.localtime(startime))
        Time, UTC, Price = input2data("UTC" + type[-6:], startime, endtime)
        MVAPrice, BOLLline, period = BOLL(UTC, Price, Period)
        UTC = UTC[max(period):]
        Time = Time[max(period):]
        Price = Price[max(period):]
        MVAPrice = np.array(MVAPrice)[:, max(period):]
        BOLLline = np.array(BOLLline)[:, max(period):]
        plotBOLLdata(Time, UTC, Price, MVAPrice, BOLLline, period, type[-6:])