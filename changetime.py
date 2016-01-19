# code: UTF-8
import re
import string
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
datapath = "C:/Documents/ForexData/"

#This function will read the file and translate it to data
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


def str2UTC(timestr):
    return str(int(time.mktime(time.strptime(timestr, "%Y%m%d%H%M%S"))))


def writeUTC(Date, Time ,Price , filename):
    returnfile = open(datapath + "UTC"+filename, "w")
    for index in range(len(Date)):
        returnfile.write(str2UTC((Date[index])+str(Time[index])) + "," + str(returnUTC[index]) + "," + str(Price[index]) + "\n")
    returnfile.close()
