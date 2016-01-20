# -*- coding:utf-8 -*-
__author__ = 'Jojo'

import sys
import os
import re
import math
import string
import datetime
import time
import numpy as np
version = sys.version.find("Red Hat")
if version == -1:
    import matplotlib.pyplot as plt

datapath = os.getcwd() + "Data/"

# This function will read the file and translate it to data
# *** the lists of Date, Time, Price ***
def file2data(filename):
    Date = []
    Time = []
    Price = []
    fr = open(datapath + filename)  # Load the data
    for line in fr.readlines():
        lines = line.strip()  # Strip the beginning and the end blank
        listFromLine = lines.split(',')  # Separate each line by '\t'
        Datelist = re.findall('\d', listFromLine[0])  # Find out the useful number data
        Dateint = int(string.join(Datelist, ''))  # Rejoin the characters
        Date.append(Dateint)  # Get the evaluate of each person
        Time.append(listFromLine[1])
        Price.append(float(listFromLine[2]))
    return Date, Time, Price


# To calculate the numbers of days between two dates
# *** an int ***
def datediff(beginDate, endDate):
    format = "%Y%m%d"
    # Translate the string to time form
    bd = time.strptime(beginDate, format)
    ed = time.strptime(endDate, format)
    # Translate the time form to date form
    bd = datetime.datetime(bd[0], bd[1], bd[2], bd[3], bd[4], bd[5])
    ed = datetime.datetime(ed[0], ed[1], ed[2], ed[3], ed[4], ed[5])
    oneday = datetime.timedelta(days=1)
    count = 0
    while bd != ed:
        ed = ed-oneday
        count += 1
    return count


#This function will set the first data time as the "0" time and format the following data based on this time
# *** a float array ***
def time2number(Date, Time):
    NumbersOfLines = len(Date) # Get the number of the lines
    index1 = 0
    index2 = 0
    day = np.zeros(NumbersOfLines)
    hourp = np.zeros(NumbersOfLines)
    #Set the "0" moment
    Date0 = str(Date[0])
    number0 = Time[0]
    hour0 = float(number0[0: 2]) + float(number0[2: 4]) / 60
    for date in Date:
        datestring = str(date)
        day[index1] = datediff(Date0, datestring)
        index1 += 1
    for days in Time:
        hour = float(days[0: 1]) + float(days[2: 3]) / 60 +float(days[4:5]) / 3600
        hourp = float(hour - hour0) / 24
        index2 += 1
    day = np.array(day)
    return (day + hourp)


if version == -1:
    # Plot the Data
    # *** No return ***
    def plotforexdata(Date, Time, Price, name):
        Day = time2number(Date, Time)
        fp = name + "_" + str(Date[0]) + "_" + str(Date[-1])

        #**********************************************************
        fig = plt.figure(figsize=(8, 6), dpi=84, facecolor="white")
        axes = plt.subplot(111)
        axes.cla() # Clear all the information in the coordinate
        # Assign the font of the picture
        font = {'family' : 'serif',
                'color'  : 'darkred',
              'weight' : 'normal',
               'size'   : 16,
              }
        #**********************************************************
        plt.plot(Day, Price)
        # Configurate the scale of the coordinate
        ax=plt.gca()
        ax.set_xticks(np.linspace(0, Day[-1], 10))
        #ax.set_xticklabels( ('0', '500', '1000', '1500', '2000'))
        ax.set_yticks(np.linspace(min(Price), max(Price), 10))
        #ax.set_yticklabels( ('500', '800', '1100', '1400', '1700','2000'))
        # Configurate the labels
        xlabel = "The day from " + str(Date[0]) + " to " + str(Date[-1])
        ylabel = "The price of the international gold"
        ax.set_ylabel(ylabel, fontdict = font)
        ax.set_xlabel(xlabel, fontdict = font)
        # Configurate the title
        titleStr = 'The Price of Gold '
        plt.title(titleStr)
        figname = fp+'.png'
        plt.savefig(figname)
        #plt.clf() # Clear the chart

        #plt.show()
        print('ALL -> Finished OK')

        plt.show()

    # Plot the txt by calling the plotforexdata function
    # *** No return ***
    def plotforextxt(filename):
        Date, Time, Price = file2data(datapath + filename)
        Day = time2number(Date, Time)
        fp = filename[0: 6] + "_" + str(Date[0]) + "_" + str(Date[-1])

        #**********************************************************
        fig = plt.figure(figsize=(8, 6), dpi=84, facecolor="white")
        axes = plt.subplot(111)
        axes.cla() # Clear all the information in the coordinate
        # Assign the font of the picture
        font = {'family' : 'serif',
                'color'  : 'darkred',
              'weight' : 'normal',
               'size'   : 16,
              }
        #**********************************************************
        plt.plot(Day, Price)
        # Configurate the scale of the coordinate
        ax=plt.gca()
        ax.set_xticks(np.linspace(0, Day[-1], 10))
        #ax.set_xticklabels( ('0', '500', '1000', '1500', '2000'))
        ax.set_yticks(np.linspace(min(Price), max(Price), 10))
        #ax.set_yticklabels( ('500', '800', '1100', '1400', '1700','2000'))
        # Configurate the labels
        xlabel = "The day from "+str(Date[0])
        ylabel = "The price of the international gold"
        ax.set_ylabel(ylabel, fontdict = font)
        ax.set_xlabel(xlabel, fontdict = font)
        # Configurate the title
        titleStr = 'The Price of Gold '
        plt.title(titleStr)
        figname = fp+'.png'
        plt.savefig(figname)
        #plt.clf() # Clear the chart

        #plt.show()
        print('ALL -> Finished OK')

        plt.show()


# To transform the UTC txt to data
# *** the lists of Time, UTC, Price ***
def UTCfile2data(filename):
    Time = []
    UTC = []
    Price = []
    fr = open(datapath + filename)  # Load the data
    for line in fr.readlines():
        lines = line.strip()  # Strip the beginning and the end blank
        listFromLine = lines.split(',')  # Separate each line by '\t'
        Time.append(listFromLine[0])
        UTC.append(float(listFromLine[1]))
        Price.append(float(listFromLine[2]))
    return Time, UTC, Price


# To transform the UTC txt to data in the giving periode
# *** the lists of Time, UTC, Price ***
def input2data(forextype, startdate, enddate):
    if forextype[0:3] != "UTC":
        startyear = startdate[0: 4]
        startmonth = startdate[4: 8]
        endyear = enddate[0: 4]
        endmonth = enddate[4: 8]
        startfilename = forextype + "_" + startyear + ".txt"
        endfilename = forextype + "_" + endyear + ".txt"
        returndate = []
        returntime = []
        returnprice = []
        date1, time1, price1 = UTCfile2data(startfilename)
        date2, time2, price2 = UTCfile2data(endfilename)

        startyear = int(startyear)
        endyear = int(endyear)
        starttime = int(str(startyear) + str(startmonth))
        endtime = int(str(endyear) + str(endmonth))

        startindex = -1
        endindex = -1
        while (startindex == -1):
            try:
                startindex = date1.index(starttime)
            except:
                starttime += 1
        while (endindex == -1):
            try:
                endindex = date2.index(endtime)
            except:
                endtime -= 1

        # startindex = date1.index(int(str(startyear) + str(startmonth)))
        # endindex = date2.index(int(str(endyear) + str(endmonth)))

        if (startyear == endyear):
            for index in range(startindex, endindex):
                returndate.append(date1[index])
                returntime.append(time1[index])
                returnprice.append(price1[index])
        elif (startyear < endyear):
            for index in range(startindex, len(date1)):
                returndate.append(date1[index])
                returntime.append(time1[index])
                returnprice.append(price1[index])
            startyear += 1
            while (startyear < endyear):
                startfilename = forextype + "_" + str(startyear) + ".txt"
                datewhole, timewhole, pricewhole = file2data(startfilename)
                for index in range(0, len(datewhole)):
                    returndate.append(index)
                    returntime.append(index)
                    returnprice.append(index)
                startyear += 1
            for index in range(0, endindex):
                returndate.append(date2[index])
                returntime.append(time2[index])
                returnprice.append(price2[index])
        return returndate, returntime, returnprice

    if forextype[0:3] == "UTC":
        if len(startdate) == 8:
            startyear = startdate[0: 4]
            startmonth = startdate[4: 8]
            endyear = enddate[0: 4]
            endmonth = enddate[4: 8]
            startfilename = forextype + "_" + startyear + ".txt"
            endfilename = forextype + "_" + endyear + ".txt"
            returntime = []
            returnUTC = []
            returnprice = []
            time1, UTC1, price1 = UTCfile2data(startfilename)
            time2, UTC2, price2 = UTCfile2data(endfilename)

            startyear = int(startyear)
            endyear = int(endyear)
            starttime = int(str(startyear) + str(startmonth))
            endtime = int(str(endyear) + str(endmonth))

            startindex = -1
            endindex = -1
            for index in range(len(time1)):
                if (str(time1[index])[0:8] == str(starttime)):
                    startindex = index
                    break
            for index in range(len(time2)):
                if (str(time2[index])[0:8] == str(endtime)):
                    endindex = index
                    break

            if (startyear == endyear):
                for index in range(startindex, endindex):
                    returntime.append(time1[index])
                    returnUTC.append(UTC1[index])
                    returnprice.append(price1[index])
            elif (startyear < endyear):
                for index in range(startindex, len(UTC1)):
                    returntime.append(time1[index])
                    returnUTC.append(UTC1[index])
                    returnprice.append(price1[index])
                startyear += 1
                while (startyear < endyear):
                    startfilename = forextype + "_" + str(startyear) + ".txt"
                    timewhole, UTCwhole, pricewhole = UTCfile2data(startfilename)
                    for index in range(0, len(timewhole)):
                        returntime.append(timewhole[index])
                        returnUTC.append(UTCwhole[index])
                        returnprice.append(pricewhole[index])
                    startyear += 1
                for index in range(0, endindex):
                    returntime.append(time2[index])
                    returnUTC.append(UTC2[index])
                    returnprice.append(price2[index])
            return returntime, returnUTC, returnprice


if version == -1:
    # To plot the UTC data with a name
    # *** No return ***
    def plotUTCforexdata(Time, UTC, Price, name):
        fp = name + "_" + str(Time[0][0:8]) + "_" + str(Time[-1][0:8])

        #**********************************************************
        fig = plt.figure(figsize=(8, 6), dpi=84, facecolor="white")
        axes = plt.subplot(111)
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
        ax = plt.gca()
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


    # To plot the chart in the giving time for the giving type
    # *** No return ***
    def plotchart(type, startime, endtime):
        Time, UTC, Price = input2data("UTC" + type[-6:], startime, endtime)
        plotUTCforexdata(Time, UTC, Price, type[-6:])



