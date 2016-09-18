import sys
import json
from pprint import pprint


def main():
    tweet_file = open(sys.argv[1])


    tweets = []
    for line in tweet_file:
     	tweets.append(json.loads(line))
    tweet_file.close()


    
    #pprint(tweets)
    hashtag = {}
    #print len(tweets)
    for i in range(len(tweets)):
	#print type(tweets[i])
	hashtag_text = ""
	if "entities" in tweets[i]:
		#print "here1"
		#print len(tweets[i]["entities"]["hashtags"])
		#print tweets[i]["entities"]["hashtags"]
		if len(tweets[i]["entities"]["hashtags"]) > 0:
			for j in range(len(tweets[i]["entities"]["hashtags"])):
				if "text" in tweets[i]["entities"]["hashtags"][j]:
					#print "here2"
					hashtag_text = tweets[i]["entities"]["hashtags"][j]["text"].encode("utf-8")
					#print hashtag_text
		
					if hashtag_text in hashtag:
						hashtag[hashtag_text] += 1.0
					else:
						if hashtag_text != "":
							hashtag[hashtag_text] = 1.0

 
    #print sorted(hashtag, key=lambda key: hashtag[key])[0:9]
	
    for w in sorted(hashtag, key=hashtag.get, reverse=True)[0:10]:
  	print w, hashtag[w]


if __name__ == '__main__':
    main()

