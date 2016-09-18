import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    matrix = record[0]
    i = record[1] 
    j = record[2]
    matrix_value = record[3]
    if matrix == "a":
	for k in range(5):
    		mr.emit_intermediate((i,k), record)
		#print "HERE1"
		i#print (i,k), record
    elif matrix == "b":
	for k in range(5):
    		mr.emit_intermediate((k,j), record)
		#print "HERE2"
		#print (k,j), record

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    #print list_of_values
    #print key
    c_i = key[0]
    c_j = key[1]
    total = 0
    a ={}
    b ={}
    for v in list_of_values:
	#print v
	if v[0] == "a":
		a[str(v[1]) + "_" + str(v[2])] = v[3]
	else:
		b[str(v[1]) + "_" + str(v[2])] = v[3]

    for i in range(5):
	a_value = 0 
	b_value = 0
	if (str(c_i) + "_" + str(i)) in a:
		a_value = a[str(c_i) + "_" + str(i)]
	if (str(i) + "_" + str(c_j)) in b:
		b_value = b[str(i) + "_" + str(c_j)]
	#print a_value
	#print b_value
	total += a_value * b_value
    mr.emit((c_i, c_j, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
