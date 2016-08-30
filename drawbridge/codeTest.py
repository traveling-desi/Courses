import random
import sys

def ipAddr (inStr, debug=0):
	i = 0
	## We create possible address values @ each poistion.
	## for example "1234" will jhave 1, 12, 123 at poistion '0'. We add this in dictionary.
	## All the code in the procedure it index manipulation to get it correct.
	patternList = dict()
	while (i < len(inStr)):
		j = 0
		while (j < 2):
			k = 0
			while (k < 3):
				if i+j+k+1 > len(inStr):
					break
				#print inStr[i+j:i+j+k+1] + "," ,
				if not (i+j) in patternList:
					patternList[i+j] = set()

				## if pattern > 255 dont add
				if int(inStr[i+j:i+j+k+1]) < 256:	
					patternList[i+j].add(inStr[i+j:i+j+k+1])
				k += 1
			j += 1
		i += 1

	## Run script as:
	## python codeTest.py 1 
	## if debug needed.
	## will show the dictionary	
	if debug:
		print "\n"
		print "Dictionary Created :"

		for i in sorted(patternList.keys()):
			print i, 
			print ":",
			print patternList[i]

	### Call the next function. This is not needed but tried to keep each functions small.
	formIp(patternList,inStr)


def formIp(patternList, inputStr):
	num = len(patternList.keys())
	print "Working on inputStr " + inputStr

	## we run 100k trials
	itr = 99999
	alreadyFound = [] 	### to save valid pattern already found so we dont print it again and again.
	while itr > 0:
		ipStr = ""
		i = 0
		times = 0	### How many times did we add a pattern. If already 4 times then the previous choices we made were wrong.

		##traverse through each of the keys in the dictionary
		while i < num :
	
			## Pick a pattern from each postion randomly. 
			elem = random.sample(patternList[i],1)[0]
			ipStr += str(elem) + "."
			times += 1
			if times == 4:
				break
			
			## move index by the length of the pattern added.
			i += len(str(elem))
		ipStr = ipStr[0:-1]

		## If the pattern without the "." is the input pattern then we chose a good pattern.
		## Should have at least 3 "."
		if ipStr.replace(".", "") == inputStr and ipStr.count(".") == 3:
			if not inputStr in alreadyFound:	
				print "Found one :" + ipStr
				alreadyFound.append(inputStr)
		itr -= 1
			
										
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

