import sys
import re
import pandas 
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep

verbose =0
closefield = "actual_close"
portfolio = {}

cmd_line = sys.argv
portfolio_value = 0
portfolio["cash"] = int(cmd_line[1],10)
ord_file = cmd_line[2]
val_file =cmd_line[3]
#print ord_file
#print val_file

lines = []
f = open(ord_file, "r")
try:
	for line in f:
		lines.append(re.sub('[\n]','',line))
finally:
	f.close()


symbols = []
timeofday=dt.timedelta(hours=16)
dataobj = da.DataAccess('Yahoo')
if verbose:
	print __name__ + " reading data"

for i in range (len(lines)):
	order = lines[i].split(',')
	print lines[i]
	print order[0]
	print order[1]
	print order[2]
	print order[3]
	print order[4]
	print order[5]
	if i == 0:
		startday = dt.date(int(order[0],10),int(order[1],10),int(order[2],10))
		print startday
	if i == len(lines) - 1:
		endday = dt.date(int(order[0],10),int(order[1],10),int(order[2],10))
		print endday
	if (order[3] in symbols) == False:
		symbols.append(order[3])
	print symbols

for sym in symbols:
	portfolio[sym] = 0

timestamps = du.getNYSEdays(startday,endday,timeofday)
#print "TIME"
print timestamps
close = dataobj.get_data(timestamps, symbols, closefield)
#close = (close.fillna(method='ffill')).fillna(method='backfill')

#print close

for sym in symbols:
       for time in timestamps:
		print time
                print close[sym][time]
j = 0
for i in range (len(timestamps)):	
	order = lines[j].split(',')
	day_time = dt.datetime(int(order[0],10),int(order[1],10),int(order[2],10),16,0)
	portfolio_value = 0
	for sym in portfolio:
		if sym == "cash" :
			portfolio_value = portfolio_value + portfolio[sym]
		else:
			portfolio_value = portfolio_value + close[sym][timestamps[i]]*portfolio[sym]
			
	print timestamps[i], day_time, portfolio, portfolio_value
		
	if(timestamps[i] == day_time):
		while (timestamps[i] == day_time):
			price = close[order[3]][day_time]
			cash_change = int(order[5],10)*price
			if (order[4] == "BUY"):
				portfolio["cash"] = portfolio["cash"] - cash_change
				portfolio[order[3]] = portfolio[order[3]] + int(order[5],10)
			else:
				portfolio["cash"] = portfolio["cash"] + cash_change
				portfolio[order[3]] = portfolio[order[3]] - int(order[5],10)
	
			print timestamps[i], day_time, portfolio
			j = j+1
			if j < len(lines):
				order = lines[j].split(',')
				day_time = dt.datetime(int(order[0],10),int(order[1],10),int(order[2],10),16,0)
			else:
				break


	
		
		

# Reading the Data

#print lines[0][0:10]
#line_date = dt.datetime.strptime('2011,01,23','%Y,%m,%d').date()

