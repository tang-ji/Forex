#code: UTF-8
__author__ = 'Jojo'
from Hurst import *
from MVA import *
import changetime


type = "XAUUSD"
startime = "20070703"
endtime = "20070720"

# for year in range(2001, 2016):
#     filename = type + "_" + str(year) + ".txt"
#     if os.path.exists(datapath + "UTC" + filename):
#         continue
#     Date, Time, Price = changetime.file2data(filename)
#     changetime.writeUTC(Date, Time, Price, datapath + "UTC" + filename)
#
# plotprice_hurst("UTC" + type[-6:], "20080730", "20080803", 50)

plotMVA("UTCXAUUSD", "20080304", "20080309", "300,500,1000")


