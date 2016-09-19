import orange, orngTree
data = orange.ExampleTable("voting")

tree = orngTree.TreeLearner(data, sameMajorityPruning=1, mForPruning=2)
print "Possible classes:", data.domain.classVar.values
print "Probabilities for democrats:"
for i in range(5):
    p = tree(data[i], orange.GetProbabilities)
    print "%d: %5.3f (originally %s)" % (i+1, p[1], data[i].getclass())

orngTree.printTxt(tree)
