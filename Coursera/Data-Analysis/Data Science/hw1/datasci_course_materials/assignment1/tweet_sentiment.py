import sys
import json
#from pprint import pprint

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = {} # initialize an empty dictionary
    for line in sent_file:
  	term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  	scores[term] = int(score)  # Convert the score to an integer.

    #print scores.items()

    tweets = []
    for line in tweet_file:
     	tweets.append(json.loads(line))
    
    #pprint(tweets)
    #print len(tweets)
    for i in range(len(tweets)):
	#print type(tweets[i])
        if "text" in tweets[i]:
                tweet_text = tweets[i]["text"].encode("utf-8")
        else:
                tweet_text = ""
	#print tweet_text
	sent_score = 0.0
	tweet_words = tweet_text.split()
	#print tweet_words
	for j in range(len(tweet_words)):
		#print tweet_words[j]
		if tweet_words[j] in scores:
			#print "----------------------------------->"
			#print scores[tweet_words[j]]
			sent_score += scores[tweet_words[j]]
	print sent_score
	
    tweet_file.close()
    sent_file.close()


    #hw()
    #lines(sent_file)
    #lines(tweet_file)

if __name__ == '__main__':
    main()

