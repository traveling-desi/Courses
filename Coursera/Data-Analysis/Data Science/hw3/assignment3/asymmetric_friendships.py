import MapReduce
import sys
import os

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()
friends_hash = {}

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    global friends_hash
    key = record[0]
    value = record[1]
    #print key + "_" + value
    friends_hash[key + "_" + value] = 0
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    #print list_of_values
    #print type(list_of_values)
    for v in list_of_values:
      #print key, v
      if not (v + "_" + key) in friends_hash:
	#print "HERE1"
    	mr.emit((key, v))
    	mr.emit((v, key))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
