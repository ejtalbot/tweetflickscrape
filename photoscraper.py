import twitter_functions
import flickr_functions

#twitter API info
twitterConsumerKey = "TwyIU3QwaV7VeDQqeeRemuqLk"
twitterConsumerSecret = "7QwBDEeamGOXFmCwOSFBunoK2PxKHopn8l3joQnAalGsreVmGh"

#twitter authentication
bearerCredentials = twitter_functions.create_bearer_credentials(twitterConsumerKey, twitterConsumerSecret)
bearerToken = twitter_functions.create_bearer_token(bearerCredentials)

#generate all of the tweets with pictures and count
#use the premium search, but if you hit your requests usage limit. Note: the standard search is limited
#
try:
    rankedDictionary = twitter_functions.twitter_search_premium(bearerToken)
except KeyError:
    rankedDictionary = twitter_functions.twitter_search(bearerToken)

#uncomment below to print the twitter dictionary
#print(rankedDictionary)


#generate the dictionary of the flickr pics with the count of comments
additionalFlickrDict = flickr_functions.flickr_photo_ids()

#uncomment below to print the flickr dictionary
#print(additionalFlickrDict)

#combine the two dictionaries
rankedDictionary.update(additionalFlickrDict)

#get a sorted list of the dictionary keys
sortedKeys = sorted(rankedDictionary)
#iterate through the keys in reverse to print out the rank of the lists of tweets/flickr pics from highest to lowest
count = 1
for i in sortedKeys[::-1]:
    print("Rank " + str(count) + " " + str(rankedDictionary[i]) + "\n")
    count += 1