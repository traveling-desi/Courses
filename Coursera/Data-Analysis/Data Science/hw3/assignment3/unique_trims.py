import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()
dna = {}

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    global dna
    key = record[0]
    value = record[1]
    value_list = list(value)
    #print type(value_list)
    #print value_list
    del value_list[-10:]
    #print value_list
    value = "".join(value_list)
    #print value
    if not value in dna:
	dna[value] = 1
    	mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    for v in list_of_values:
    	mr.emit((v))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
