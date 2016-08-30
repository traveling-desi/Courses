import sys

def ipAddr (inStr, debug):
	print "Working on Input String " + inStr
	ipStr = ""
	i = 0
	times = 4
	if len(inStr) < 4 or len(inStr) > 12:
		print "Didnt find one"
		return
	while (i < len(inStr) ):
		if times == -1:
			break
		if not int(inStr[i:i+3]) > 255 and not(len(inStr) - (i+3) < times -1):
			ipStr +=  inStr[i:i+3] + "."
			times -= 1
			i += 3
		elif (not(len(inStr) - (i+2) < times -1)):
			ipStr += inStr[i:i+2] + "."
			times -= 1
			i += 2
		else:
			ipStr += inStr[i:i+1] + "."
			times -= 1
			i += 1
				
	if not times == -1:
		print ipStr[:-1]
	else:
		print "Didnt find one"
		
		
			
										
inStr1 = "123456789"
inStr2 = "256255789"
inStr3 = "1234"
inStr4 = "12345"
inStr5 = "123"
inStr6 = "25512552255"
inStr7 = "25512552256"
inStr71 = "25512522256"
inStr8 = "255255255256"
inStr9 = "255255255255"
inStr10 = "2552552552551"
inStr11 = "111111"
inStr12 = "1111111"
inStr13 = "11111111"
inStr14 = "111111111"
inStr15 = "1111111111"
inStr16 = "555555"
inStr17 = "5555555"
inStr18 = "55555555"
inStr19 = "555555555"
inStr20 = "5555555555"


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
ipAddr(inStr6, debug)
ipAddr(inStr7, debug)
ipAddr(inStr71, debug)
ipAddr(inStr8, debug)
ipAddr(inStr9, debug)
ipAddr(inStr10, debug)
ipAddr(inStr11, debug)
ipAddr(inStr12, debug)
ipAddr(inStr13, debug)
ipAddr(inStr14, debug)
ipAddr(inStr15, debug)
ipAddr(inStr16, debug)
ipAddr(inStr17, debug)
ipAddr(inStr18, debug)
ipAddr(inStr19, debug)
ipAddr(inStr20, debug)

