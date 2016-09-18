import sys
import json
from pprint import pprint

def main():
    tweet_file = open(sys.argv[1])

    tweet_scores = {} # initialize an empty dictionary
    total_scores = 0.0
    tweets = []
    for line in tweet_file:
     	tweets.append(json.loads(line))
    tweet_file.close()
    
    #pprint(tweets)
    #print len(tweets)
    for i in range(len(tweets)):
	#print type(tweets[i])
	#pprint(tweets[i])
	if "text" in tweets[i]:
		tweet_text = tweets[i]["text"].encode("utf-8")
	else:
		tweet_text = ""
	#print tweet_text
	tweet_words = tweet_text.split()
	#print tweet_words
	total_scores += len(tweet_words)
	for j in range(len(tweet_words)):
		#print tweet_words[j]
		temp = tweet_words[j]
		if temp in tweet_scores:
			tweet_scores[temp] += 1.0
		else:
			tweet_scores[temp] = 1.0
			
	

    total_scores_inv = 1/total_scores

    #print tweet_scores.items()
    for (i,j) in tweet_scores.items():
	temp = j*total_scores_inv
	print i,
	print temp

if __name__ == '__main__':
    main()

