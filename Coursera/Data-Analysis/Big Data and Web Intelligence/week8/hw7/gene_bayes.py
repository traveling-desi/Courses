import orange
#data_train = orange.ExampleTable("genestrain_2")
#data_test = orange.ExampleTable("genestest_2")
data_train = orange.ExampleTable("genestrain")
data_blind = orange.ExampleTable("genesblind")


classifier = orange.BayesLearner(data_train)

for i in range(len(data_blind)):
	c = classifier(data_blind[i])
	print c
