
################################### Question 1

### Search for an Anagram of a substring in a super-string


def question1(super, sub):

	### Take Care of the corner Cases upfront

	if type(super) != str or type(sub) != str:
		return False
	if sub == super:
		return True
	if sub == "":
		return True
	len_super = len(super)
	len_sub = len(sub)

	if len_sub > len_super:
		return False

	## Sort the substring
	sub_sort = ''.join(sorted(sub))

	for i in range(len_super - len_sub + 1):
		
		### Find every substring of length len_sub, sort it and see if it is the same.
		super_sort = ''.join(sorted(super[i:i+len_sub]))
		if super_sort == sub_sort:
			return True
	return False



## Test Cases
				
print (question1("udacaity", "cada"))
assert (question1("udacaity", "cada")) == True

print(question1("udacaity", "xyzg"))
assert (question1("udacaity", "xyzg")) == False

print(question1("__123_Chitty_chitty_ban_bang_abc", "ban_bang"))
assert (question1("__123_Chitty_chitty_ban_bang_abc", "ban_bang")) == True

print(question1("__123_Chitty_chitty_ban_bang_abc", "Chitty_chitty_ban_bang_abc"))
assert (question1("__123_Chitty_chitty_ban_bang_abc", "Chitty_chitty_ban_bang_abc")) == True

print(question1("__123_Chitty_chitty_ban_bang_abc", "__123_Chitty_chitty_ban_bang_abc"))
assert (question1("__123_Chitty_chitty_ban_bang_abc", "__123_Chitty_chitty_ban_bang_abc")) == True

print(question1("__123_Chitty_chitty_ban_bang_abc", "__123_Chitty_chitty_ban_bang_abc_defg"))
assert (question1("__123_Chitty_chitty_ban_bang_abc", "__123_Chitty_chitty_ban_bang_abc_defg")) == False

print(question1("__123_Chitty_chitty_ban_bang_abc", ""))
assert (question1("__123_Chitty_chitty_ban_bang_abc", "")) == True

print(question1("__123_Chitty_chitty_ban_bang_abc", None))
assert (question1("__123_Chitty_chitty_ban_bang_abc", None)) == False





#################### Question 2  ################

## Find the longest Palindrome substring in a string 's'

def question2(s):
	
	if type(s) != str:
		return s
	
	s_len = len(s)

	longestPallindrome = ""
	
	## for every character in s search on either side of the character to see if you can find a 
	## Palindrome. Keep track of the longest palindrome and return it.
	## The special case is when the palindrome is an even length string.Some nifty index manipulation catches those cases.
	## In either case pick the one that is longer.
	
	## Pretty straightforward algorithm so not discussed further.
	
	for i in range(s_len):
		for j in range(1, min(i +1, s_len - i) ):
			tempPallindrome = ""
			if not (s[i-j:i] == s[i+j:i:-1]) and not (s[i-j:i+1] == s[i+j+1:i:-1]):
				break
			if (s[i-j:i] == s[i+j:i:-1]):
				tempPallindrome = s[i-j:i+j+1]
			if len(tempPallindrome) > len(longestPallindrome):
				longestPallindrome = tempPallindrome
			if (s[i-j:i+1] == s[i+j+1:i:-1]):	
				tempPallindrome = s[i-j:i+j+2]
			if len(tempPallindrome) > len(longestPallindrome):
				longestPallindrome = tempPallindrome
	return longestPallindrome
			

## Test Cases

print question2("bcdcbaaaaaaaaaaa") 
assert question2("bcdcbaaaaaaaaaaa") == "aaaaaaaaaaa"

print question2("abcdefgfedcba")
assert question2("abcdefgfedcba") == "abcdefgfedcba"

print question2("abcdefggfedcba")
assert question2("abcdefggfedcba") == "abcdefggfedcba"

print question2("bcdcbaaaaa") 
assert question2("bcdcbaaaaa") == "bcdcb"

print question2('rrrr')
assert question2('rrrr') == "rrrr"

print question2('rrrraxyzzyxat')
assert question2('rrrraxyzzyxat') == "axyzzyxa"

print question2('rrrraxyzyxat')
assert  question2('rrrraxyzyxat') == "axyzyxa"

print question2('cdaba')
assert question2('cdaba') == "aba"

print question2('aba')
assert question2('aba') == "aba"

print question2('abba')
assert question2('abba') == "abba"

print question2('')
assert question2('') == ""

print question2(None)
assert question2(None) == None


###########################   Question 3 

### Find the minimum spanning tree in a Graph


### This graph code is not required anymore but I just kept it since I already had it.
##### Setup the graph that we can use to test Question 3 

import numpy as np
class Node(object):
    def __init__(self, value):
        self.value = value
        self.edges = []


class Edge(object):
    def __init__(self, value, node_from, node_to):
        self.value = value
        self.node_from = node_from
        self.node_to = node_to


class Graph(object):
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges

    def insert_node(self, new_node_val):
        new_node = Node(new_node_val)
        self.nodes.append(new_node)
        
    def insert_edge(self, new_edge_val, node_from_val, node_to_val):
        from_found = None
        to_found = None
        for node in self.nodes:
            if node_from_val == node.value:
                from_found = node
            if node_to_val == node.value:
                to_found = node
        if from_found == None:
            from_found = Node(node_from_val)
            self.nodes.append(from_found)
        if to_found == None:
            to_found = Node(node_to_val)
            self.nodes.append(to_found)
        new_edge = Edge(new_edge_val, from_found, to_found)
        from_found.edges.append(new_edge)
        to_found.edges.append(new_edge)
        self.edges.append(new_edge)

    def get_edge_list(self):
        """Don't return a list of edge objects!
        Return a list of triples that looks like this:
        (Edge Value, From Node Value, To Node Value)"""
        edgeList = []
        for edge in self.edges:
             edgeList.append((edge.value, edge.node_from.value, edge.node_to.value))
        return edgeList

    def get_adjacency_list(self):
        """Don't return any Node or Edge objects!
        You'll return a list of lists.
        The indices of the outer list represent
        "from" nodes.
        Each section in the list will store a list
        of tuples that looks like this:
        (To Node, Edge Value)"""
        edgeList = [None] * (len(self.nodes) + 1)
        for edge in self.edges:
                #print edge.node_from.value -100
                if edgeList[edge.node_from.value] == None:
                    edgeList[edge.node_from.value] = []
                edgeList[edge.node_from.value].append( (edge.node_to.value, edge.value) ) 
        return edgeList
 

    def get_adjacency_matrix(self):
        """Return a matrix, or 2D list.
        Row numbers represent from nodes,
        column numbers represent to nodes.
        Store the edge values in each spot,
        and a 0 if no edge exists."""
        l = len(self.nodes) + 1
        edgeArray =  np.zeros( (l,l), dtype=np.int)
        #print edgeArray
        for edge in self.edges:
              edgeArray[edge.node_from.value][edge.node_to.value] = edge.value
        return edgeArray.tolist()


   

#### End of graph setup.

## We use a sorted list of edges in the form (edge_wt, node from, node to) and then traverse the list and pick up edges
## along the way in which at least one node has not been seen before (which we keep track of using dict() )
## This guarantees we pick up only the lightest weight edges.


def question3(graph):
	mst = dict()
	nodesV = dict()
	edgeList = []
	nodeList = set()

	## The input is provided as an adjacency list. But since I had already written my algorithm
	## in terms of edgeList I just massaged the adjacency list to edgeList. 
	## I wont do it in production code. :)
	for key in graph:
		for edge in graph[key]:
			if len(edge) < 2:
				print "Something wrong with edge " + str(edge) + " for node " + str(key)
				return None
			if edge[1] == edge[0]:
				print "Warning: Graph has a self edge on node edge[0]"
			edgeList.append( (edge[1], key, edge[0] ) )
			nodeList.add(key)
			nodeList.add(edge[0])

	numV = len(nodeList)

	## Our algorithm assumes edges are sorted in ascending order. So sort the edgelist here.
	edgeList.sort(key=lambda x: x[0])
	#print edgeList
	while True:	
		for (wt, vf, vt) in edgeList:

			#print mst
			#print (wt, vf, vt)

			if len(mst.keys()) == 0:
				mst[vf] = []
				mst[vf] = [(vt, wt)]
				nodesV[vt] = 1
				nodesV[vf] = 1
				break
	
			#go to next edge if both nodes have already been seen
			if ((vf in nodesV) and (vt in nodesV)) or (not (vf in nodesV) and not (vt in nodesV)):
			#if ((vf in mst) and (vt in mst)) or (not (vf in mst) and not (vt in mst)):
				continue
			else:
				## Create a list for which nodes we haven't seen before.
				## Both Vf and Vt nodes have been touched so both should be added to the dict()
				if not vf in nodesV:
					mst[vf] = []
					mst[vf] = [(vt, wt)]
					nodesV[vf] = 1
				else:
					mst[vt] = []
					mst[vt] = [(vf, wt)]
					nodesV[vt] = 1
				break
	
		if len(nodesV.keys()) == numV:
			return mst

## graph1 = Graph()
## graph1.insert_edge(101, 1, 3)
## graph1.insert_edge(103, 3, 4)
## graph1.insert_edge(102, 1, 4)
## graph1.insert_edge(104, 4, 5)
## graph1.insert_edge(100, 1, 2)
## graph1.insert_edge(108, 7, 5)
## graph1.insert_edge(105, 5, 6)
## graph1.insert_edge(107, 2, 7)
## graph1.insert_edge(109, 7, 8)
## graph1.insert_edge(106, 1, 6)
## graph1.insert_edge(110, 8, 6)


graph1 = {1: [(3, 101), (4, 102), (2, 100), (6, 106)], 2: [(7, 107)], 3: [(4, 103)], 4: [(5, 104)], 5: [(6, 105)], 7: [(5, 108), (8, 109)], 8: [(6, 110)]}
print question3(graph1)	
assert question3(graph1) == {1: [(2, 100)], 3: [(1, 101)], 4: [(1, 102)], 5: [(4, 104)], 6: [(5, 105)], 7: [(2, 107)], 8: [(7, 109)]}

## Graph2 = graph1.__class__
## graph2 = Graph2()
## graph2.insert_edge(100, 1, 2)
## graph2.insert_edge(100, 2, 3)
## graph2.insert_edge(100, 3, 1)
## 

graph2 = {1: [(2, 100)], 2: [(3, 100)], 3 : [(1, 100)]}
print question3(graph2)
assert question3(graph2) == {1: [(2, 100)], 3: [(2, 100)]}

graph3 = {1: [(2, 100)]}
print question3(graph3)
assert question3(graph3) == {1: [(2, 100)]}

graph4 = {1: [(2, 101)], 2: [(3, 102)], 3 : [(1, 100)]}
print question3(graph4)
assert question3(graph4) == {2: [(1, 101)], 3: [(1, 100)]}

graph5 = {1: [(2, 100)], 2: [(3, 100)], 3: [(4, 100)], 4: [(5, 100)], 5: [(6, 100)], 6: [(7, 100)], 7: [(1, 100)]}
print question3(graph5)
assert question3(graph5) == {1: [(2, 100)], 3: [(2, 100)], 4: [(3, 100)], 5: [(4, 100)], 6: [(5, 100)], 7: [(6, 100)]}

graph6 = {1: [(2, )]}
print question3(graph6)
assert question3(graph6) == None

graph7 = {0: [(1, 4), (7, 8)], 1: [(2, 8), (7, 11)], 2: [(8, 2), (5, 4), (3, 7)], 3: [(5, 14), (4, 9)], 4: [(5, 10)], 5: [(6 ,2)], 6: [(8, 6), (7, 1)]}
print question3(graph7)
assert question3(graph7) == {0: [(7, 8)], 1: [(0, 4)], 2: [(5, 4)], 3: [(2, 7)], 4: [(3, 9)], 5: [(6, 2)], 6: [(7, 1)], 8: [(2, 2)]}



######################### Question 4 #########


## Finding common ancestor of two nodes in a tree.

### Helper function we wrote
### if the two values n1,n2 are on either side of the current node value then the current node value is the lowest common anscestor
def found_ca(n1,n2,r):
        if (n1 >= r and n2 <= r) or (n1 <= r and n2 >= r):
                return r
	else:
		return -1


def question4(T, r, n1, n2):

	num_nodes = len(T[0])

	if r > num_nodes or n1 > num_nodes or n2 > num_nodes or r < 0  or n1 < 0 or n2 < 0:
		print "One of the given node is outside the range of the tree. Please check"
		return None
	
	curr_node = r
	while 1:
	
		### if the two values n1,n2 are on either side of the current node value then the current node value is the lowest common anscestor
		t = found_ca(n1, n2, curr_node)
		if t > 0:
			return t

		## Find children of the current node. Note this algorithm should work even if 
		## the current node has only one leaf.
		childList = T[curr_node]
		edgeList = [i for i, num in enumerate(childList) if num  == 1]
		if len(edgeList) > 2:
			print "Something wrong with the tree at node " + str(curr_node) + " it has more than two edges"
			return None
		
		if n1 > edgeList[0] and n2 > edgeList[0]:
			curr_node = edgeList[1]
		else:
			curr_node = edgeList[0]

print question4([[0,1,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,0,0,0,0]],3,4,1)
assert question4([[0,1,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,0,0,0,0]],3,4,1) == 3

print question4([[0,0,0,0,0,0],[1,0,0,0,0,0],[0,1,0,0,1,0],[0,0,0,0,0,0],[0,0,0,1,0,1],[0,0,0,0,0]],2,5,3)
assert question4([[0,0,0,0,0,0],[1,0,0,0,0,0],[0,1,0,0,1,0],[0,0,0,0,0,0],[0,0,0,1,0,1],[0,0,0,0,0]],2,5,3) == 4

print question4([[0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0]],5,6,7)
assert question4([[0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0]],5,6,7) == 6

print question4([[0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0]],15,-1,0)
assert question4([[0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0]],15,-1,0) == None

print question4([[0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,1,0,0,1,0,0,1],[0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0]],5,6,7)
assert question4([[0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,1,0,0,1,0,0,1],[0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0]],5,6,7) == None



#################### question 5 ######################

### Setup the linkedlist that we can use to test for question 5

class Element(object):
    def __init__(self, value):
        self.value = value
        self.next = None
        
class LinkedList(object):
    def __init__(self, head=None):
        self.head = head
        
    def append(self, new_element):
        current = self.head
        if self.head:
            while current.next:
                current = current.next
            current.next = new_element
        else:
            self.head = new_element
            
    def get_position(self, position):
        """Get an element from a particular position.
        Assume the first position is "1".
        Return "None" if position is not in the list."""
        if not self.head:
            return None
        else:
            if position == 1:
                return self.head
            current = self.head
            while current.next and (position > 2):
                #print current.value
                current = current.next
                position = position - 1
            #print position
            #print current.value
            if position > 1:
                return current.next
            else:
                return None
    
    def insert(self, new_element, position):
        """Insert a new node at the given position.
        Assume the first position is "1".
        Inserting at position 3 means between
        the 2nd and 3rd elements."""
        if not self.head:
            return None
        current = self.head
        while current.next and (position > 2):
            current = current.next
            position = position - 1
        new_element.next = current.next
        current.next = new_element
    
    def delete(self, value):
        """Delete the first node with a given value."""
        if not self.head:
            return None
        current = self.head
        previous = self.head
        #print current.value
        while current.value != value:
           print current.value
           previous = current
           current = current.next
        
        if current == self.head:
            #print "here"
            self.head = current.next
            #print self.head.value
        else:
            previous.next = current.next
        
### End of linked list setup

##### Queue Based Implementation


## We use a queue to keep track of the # of the elements we need. For example if
## asked for 10th element from the end, we keep a list of last 10 elements we had seen
##  in a queue. We keep pushing new elements in the queue (and pushing out elements older than 10 elements old)
## Do this till end of linked list, then the first element in the queue is the element we want.


from Queue import Queue
def question5(ll, m):
	## Is the linked list valid? Are the inputs correct?
	if not ll.head:
		return None
	if m < 1:
		return None

	## Create a queue
	my_q = Queue(maxsize=0)
	q_size = m

	current = ll.head

	## while we haven't reached the end of the linked list
	while current.next:
		## Add the next element to the queue
		my_q.put(current)
		q_size = q_size - 1
		
		#if the queue is full (i.e we have added 'm' elements already)
		#make space using FIFO
		if q_size < 1:
			my_q.get()

		current = current.next

	## Put in the final element
	my_q.put(current)
	if q_size >  0:
		print "m was longer than the length of the linked list. Nothing to return"
		return None
	else:
		## Once end of the linked list is reached return the first element.
		return my_q.get().value


# Test cases
# Start setting up a LinkedList
ll1 = LinkedList(Element(1))
for i in range(2, 21):
	ll1.append(Element(i))
 
## for i in range(1, 21):
## 	print ll1.get_position(i).value


print question5(ll1, 10)
assert question5(ll1, 10) == 11

print question5(ll1, 5)
assert question5(ll1, 5) == 16

print question5(ll1, 19)
assert question5(ll1, 19) == 2

print question5(ll1, 100)
assert question5(ll1, 100) == None

print question5(ll1, None)
assert question5(ll1, None) == None

print question5(ll1, -1)
assert question5(ll1, -1) == None

print question5(ll1, 0)
assert question5(ll1, 0) == None

print question5(ll1, 1)
assert question5(ll1, 1) == 20


##### pointer Based Implementation



def question5(ll, m):
	## Is the linked list valid? Are the inputs correct?
	if not ll.head:
		return None
	if m < 1:
		return None
	gap = m
	
	ld_ptr = ll.head
	lg_ptr = ll.head

	## while we haven't reached the end of the linked list
	while ld_ptr.next:
		## Add the next element to the queue
		ld_ptr = ld_ptr.next
		gap  = gap - 1
		if gap < 1:
			lg_ptr = lg_ptr.next
			
	if lg_ptr == ll.head:
		print "m was longer than the length of the linked list. Nothing to return"
		return None
	else:
		## Once end of the linked list is reached return the first element.
		return lg_ptr.value


# Test cases
# Start setting up a LinkedList
ll2 = LinkedList(Element(1))
for i in range(2, 21):
	ll2.append(Element(i))
 
## for i in range(1, 21):
## 	print ll2.get_position(i).value


print question5(ll2, 10)
assert question5(ll2, 10) == 11

print question5(ll2, 5)
assert question5(ll2, 5) == 16

print question5(ll2, 19)
assert question5(ll2, 19) == 2

print question5(ll2, 100)
assert question5(ll2, 100) == None

print question5(ll2, None)
assert question5(ll2, None) == None

print question5(ll2, -1)
assert question5(ll2, -1) == None

print question5(ll2, 0)
assert question5(ll2, 0) == None

print question5(ll2, 1)
assert question5(ll2, 1) == 20
