# code: UTF-8

from FkNN import *

# This function will read the file and translate it into data
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


# To transform the time str into string
# *** a string ***
def str2UTC(timestr):
    return str(int(time.mktime(time.strptime(timestr, "%Y%m%d%H%M%S"))))


# To creat a series of UTC data in the harddisk
# *** No return ***
def writeUTC(Date, Time, Price, filename):
    returnfile = open(filename, "w")
    for index in range(len(Date)):
        Timestr = str(Date[index]) + str(Time[index])
        returnfile.write(Timestr + "," + str2UTC(Timestr) + "," + str(Price[index]) + "\n")
    returnfile.close()
