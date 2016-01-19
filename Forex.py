#code: UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'Jojo'
import FkNN



type = "XAUUSD"
startime = "20070703"
endtime = "20070720"

FkNN.plotprice_hurst("UTC" + type[-6:], "20080730", "20080803", 16)



# import changetime
# for year in range(2001,2016):
#     Date, Time, Price = changetime.file2data("XAUUSD_" + str(year) + ".txt")
#     changetime.writeUTC(Date, Time ,Price , "XAUUSD_" + str(year) + ".txt")
