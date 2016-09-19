import orange, orngTree
data_train = orange.ExampleTable("genestrain_2")
#data_test = orange.ExampleTable("genestest_2")
#data_train = orange.ExampleTable("genestrain")
data_blind = orange.ExampleTable("genesblind")


# setting up the classifiers
majority = orange.MajorityLearner(data_train)
bayes = orange.BayesLearner(data_train)
tree = orngTree.TreeLearner(data_train, sameMajorityPruning=1, mForPruning=5)
knn = orange.kNNLearner(data_train, k=21)

majority.name="Majority"; bayes.name="Naive Bayes";
tree.name="Tree"; knn.name="kNN"

classifiers = [majority, bayes, tree, knn]


# print the head
print "Possible classes:", data_train.domain.classVar.values
print "Original Class",
for l in classifiers:
    print "%-13s" % (l.name),
print

# classify first 10 instances and print probabilities
for example in data_blind:
    print "(%-10s)  " % (example.getclass()),
    for c in classifiers:
        p = apply(c, [example, orange.GetProbabilities])
	#print p,
        #print "%5.3f        " % (p[0]),
    	q = p.values()
    	q_max =max(q)
    	eth = q.index(max(q))
    	if eth == 0:
        	eth_type = "ASW"
		eth_num = 3
    	elif eth == 1:
        	eth_type = "CEU"
		eth_num = 0
    	elif eth == 2:
        	eth_type = "GIH"
		eth_num = 1
    	elif eth == 3:
        	eth_type = "JPT"
		eth_num = 2
    	else:
        	eth_type = "YRI"
		eth_num = 4
    	print "%-10s, %d" % (eth_type, eth_num),
    print

