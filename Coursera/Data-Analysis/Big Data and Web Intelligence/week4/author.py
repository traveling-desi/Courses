import mincemeat
import glob
import re


text_files =glob.glob('hw3data/*.txt')




def file_contents(file_name):
	f = open(file_name)
	try:
		return f.read()
	finally:
		f.close()

source = dict((file_name, file_contents(file_name))
	for file_name in text_files)

# Setup map and reduce functions

def mapfn(k, v):
    import re
    author = {}
    allStopWords= {'about':1, 'above':1, 'after':1, 'again':1, 'against':1, 'all':1, 'am':1, 'an':1, 'and':1, 'any':1, 'are':1, 'arent':1, 'as':1, 'at':1, 'be':1, 'because':1, 'been':1, 'before':1, 'being':1, 'below':1, 'between':1, 'both':1, 'but':1, 'by':1, 'cant':1, 'cannot':1, 'could':1, 'couldnt':1, 'did':1, 'didnt':1, 'do':1, 'does':1, 'doesnt':1, 'doing':1, 'dont':1, 'down':1, 'during':1, 'each':1, 'few':1, 'for':1, 'from':1, 'further':1, 'had':1, 'hadnt':1, 'has':1, 'hasnt':1, 'have':1, 'havent':1, 'having':1, 'he':1, 'hed':1, 'hell':1, 'hes':1, 'her':1, 'here':1, 'heres':1, 'hers':1, 'herself':1, 'him':1, 'himself':1, 'his':1, 'how':1, 'hows':1, 'i':1, 'id':1, 'ill':1, 'im':1, 'ive':1, 'if':1, 'in':1, 'into':1, 'is':1, 'isnt':1, 'it':1, 'its':1, 'its':1, 'itself':1, 'lets':1, 'me':1, 'more':1, 'most':1, 'mustnt':1, 'my':1, 'myself':1, 'no':1, 'nor':1, 'not':1, 'of':1, 'off':1, 'on':1, 'once':1, 'only':1, 'or':1, 'other':1, 'ought':1, 'our':1, 'ours ':1, 'ourselves':1, 'out':1, 'over':1, 'own':1, 'same':1, 'shant':1, 'she':1, 'shed':1, 'shell':1, 'shes':1, 'should':1, 'shouldnt':1, 'so':1, 'some':1, 'such':1, 'than':1, 'that':1, 'thats':1, 'the':1, 'their':1, 'theirs':1, 'them':1, 'themselves':1, 'then':1, 'there':1, 'theres':1, 'these':1, 'they':1, 'theyd':1, 'theyll':1, 'theyre':1, 'theyve':1, 'this':1, 'those':1, 'through':1, 'to':1, 'too':1, 'under':1, 'until':1, 'up':1, 'very':1, 'was':1, 'wasnt':1, 'we':1, 'wed':1, 'well':1, 'were':1, 'weve':1, 'were':1, 'werent':1, 'what':1, 'whats':1, 'when':1, 'whens':1, 'where':1, 'wheres':1, 'which':1, 'while':1, 'who':1, 'whos':1, 'whom':1, 'why':1, 'whys':1, 'with':1, 'wont':1, 'would':1, 'wouldnt':1, 'you':1, 'youd':1, 'youll':1, 'youre':1, 'youve':1, 'your':1, 'yours':1, 'yourself':1, 'yourselves':1}
    #print k
    for line in v.splitlines():
            #print line
            w = re.split('\:\:\:', line)
            #print "W"
            #print w
            paper_id = w[0]
            #print "PAPER_ID"
            #print paper_id
            title = w[2]
            #print "TITLE"
            #print title
            regex = re.compile(r"\.|\?|\(|\)")
            title = regex.sub(r"", title)
            #print "TITLE2"
            #print title
            title_new = ""
            for title_words in title.split():
                    if (not(title_words in allStopWords.keys())) and re.match('^\w+-?\w+$', title_words):
                            title_new = title_new + " " + title_words
   	    #print title_new
            for a in w[1].split("::"):
                    #print a
		    #print author.keys()
		    #print len(author.keys())
                    if a.lower() in author.keys():
                            author[a.lower()] = author[a.lower()] + " " + title_new.lower()
			    #print "HERE 1"
                    else:
                            author[a.lower()] = title_new.lower()
			    #print "HERE 2"
    for k in author.keys():
	    #print k
	    #print author[k]
	    #print "-------------------------------------------------------------"
	    yield k, author[k]

	

def reducefn(k, vs):
    #print vs[0]
    word_count = {}
    for line in vs:
    	for word in line.split():
        	if word in word_count.keys():
                        word_count[word.lower()] += 1
                else:
                        word_count[word.lower()] = 1
    return word_count 

##def reducefn(k, vs):
##	print k
##	if k == 'michel raynal':
##		print "GOT ONE"
##		return vs


s = mincemeat.Server()

# The data source can be any dictionary-like object
s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
#print results
for k in results.keys():
	print k
	print results[k]
	print "-------------------------------------------------------------"
