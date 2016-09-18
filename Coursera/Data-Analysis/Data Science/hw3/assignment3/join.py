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
    key = record[1]
    #del record[1]
    mr.emit_intermediate(key, record)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    #print list_of_values
    list_of_values_bak = list_of_values
    v = [(i, list_of_values.index("order"))
 	for i, list_of_values in enumerate(list_of_values)
 	if "order" in list_of_values][0][0]
    #print type(v)
    order = list_of_values_bak.pop(v)
    #del order[0]
    #print order
    #print list_of_values_bak

    for v in list_of_values_bak:
	#del v[0]
	#print v
	string = order + v
	#print type(string)
	#print len(string)
	#print string
    	mr.emit((string))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
