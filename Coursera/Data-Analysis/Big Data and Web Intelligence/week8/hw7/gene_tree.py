import orange, orngTree
data_train = orange.ExampleTable("genestrain_2")
#data_test = orange.ExampleTable("genestest_2")
#data_train = orange.ExampleTable("genestrain")
data_blind = orange.ExampleTable("genesblind")

tree = orngTree.TreeLearner(data_train, sameMajorityPruning=1, mForPruning=5)
print "Possible classes:", data_train.domain.classVar.values
for i in range(len(data_blind)):
    p = tree(data_blind[i], orange.GetProbabilities)
    print p
    q = p.values()
    q_max =max(q)
    eth = q.index(max(q))
    if eth == 0:
	eth_type = "ASW"
    elif eth == 1:
	eth_type = "CEU"
    elif eth == 2:
	eth_type = "GIH"
    elif eth == 3:
	eth_type = "JPT"
    else:
	eth_type = "YRI"
    print "%d: %5.3f, %s (originally %s)" % (i+1, q_max, eth_type, data_blind[i].getclass())

##eth_type_list = list()
##for i in range(15):
##    p = tree(data_blind[i], orange.GetProbabilities)
##    print p
##    q = p.values()
##    q_max =max(q)
##    eth = q.index(max(q))
##    if eth == 0:
##        eth_type = "ASW"
##        eth_type_list.append("ASW")
##    elif eth == 1:
##        eth_type = "CEU"
##        eth_type_list.append("CEU")
##    elif eth == 2:
##        eth_type = "GIH"
##        eth_type_list.append("GIH")
##    elif eth == 3:
##        eth_type = "JPT"
##        eth_type_list.append("JPT")
##    else:
##        eth_type = "YRI"
##        eth_type_list.append("YRI")
##    print "%d: %5.3f, %s (originally %s)" % (i+1, q_max, eth_type, data_blind[i].getclass())
##pprint(eth_type_list)
##
##Possible classes: <ASW, CEU, GIH, JPT, YRI>
##
##
##
##orngTree.printTxt(tree)
