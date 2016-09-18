import sys
import json
#from pprint import pprint
from types import *



def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    states = {"AL" :0, "AK" :0, "AZ" :0, "AR" :0, "CA" :0, "CO" :0, "CT" :0, "DE" :0,
              "FL" :0, "GA" :0, "HI" :0, "ID" :0, "IL" :0, "IN" :0, "IA" :0, "KS" :0,
	      "KY" :0, "LA" :0, "ME" :0, "MD" :0, "MA" :0, "MI" :0, "MN" :0, "MS" :0,
	      "MO" :0, "MT" :0, "NE" :0, "NV" :0, "NH" :0, "NJ" :0, "NM" :0, "NY" :0,
	      "NC" :0, "ND" :0, "OH" :0, "OK" :0, "OR" :0, "PA" :0, "RI" :0, "SC" :0,
	      "SD" :0, "TN" :0, "TX" :0, "UT" :0, "VT" :0, "VA" :0, "WA" :0, "WV" :0,
	      "WI" :0, "WY" :0} 


    scores = {} # initialize an empty dictionary
    for line in sent_file:
  	term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
  	scores[term] = int(score)  # Convert the score to an integer.

    #print scores.items()

    tweets = []
    for line in tweet_file:
     	tweets.append(json.loads(line))

    tweet_file.close()
    sent_file.close()
    
    #pprint(tweets)
    #print len(tweets)
    for i in range(len(tweets)):
	#print type(tweets[i])
	state = "undefined"
        if "text" in tweets[i]:
                tweet_text = tweets[i]["text"].encode("utf-8")
        else:
                tweet_text = ""
	#print tweet_text
	sent_score = 0.0
	if "place" in  tweets[i]:
		if type(tweets[i]["place"]) is not  NoneType:
			#print "here"
			if "full_name" in tweets[i]["place"]:
				state_text = tweets[i]["place"]["full_name"]
				#print state_text
				state_words = state_text.split()
				for j in range(len(state_words)):
					if state_words[j] in states:
						state = state_words[j]
						#print state
	tweet_words = tweet_text.split()
	#print tweet_words
	for j in range(len(tweet_words)):
		#print tweet_words[j]
		if tweet_words[j] in scores:
			#print "----------------------------------->"
			#print scores[tweet_words[j]]
			sent_score += scores[tweet_words[j]]
	#print sent_score
	if state != "undefined":
		states[state] += sent_score

	
    #for w in sorted(states, key=states.get, reverse=True):
    for w in sorted(states, key=states.get, reverse=True)[0:1]:
        #print w, states[w]
        print w



if __name__ == '__main__':
    main()

