import random
import sys

def ipAddr (inStr, debug=0):
	i = -1
	ipStr = []
	print recurIp(inStr, ipStr, i, k =1, times = -1)



def recurIp(inStr, ipStr, i, k, times):
	i += k
	if i >= len(inStr):
		return ""
	elif times == 4:
		return False
	else:
		ipStr.append(inStr[i:i+k])
		times += 1
		elem = recurIp(inStr, ipStr, i, k, times)
		if not elem:
			k += 1
			recurIp(inStr, ipStr, i, k, times)
		else:
			ipStr.append(elem)
		print "i = " + str(i)
		print "ipStr 2 " ,
		print ipStr	
		return ipStr
			
										
inStr1 = "123456789"
inStr2 = "256255789"
inStr3 = "1234"
inStr4 = "12345"
inStr5 = "25512552255"

debug = 0
try:
	debug = sys.argv[1]
except:
	pass
	
ipAddr(inStr1, debug)
ipAddr(inStr2, debug)
ipAddr(inStr3, debug)
ipAddr(inStr4, debug)
ipAddr(inStr5, debug)

