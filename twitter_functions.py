import requests
from base64 import urlsafe_b64encode

#twitterConsumerKey = "TwyIU3QwaV7VeDQqeeRemuqLk"
#twitterConsumerSecret = "7QwBDEeamGOXFmCwOSFBunoK2PxKHopn8l3joQnAalGsreVmGh"

#twitter app only authentication
#creating bearer credentials
def create_bearer_credentials(key, secret):
    concatKeySecret = key + ':' + secret
    bearerCredentialsBytes = urlsafe_b64encode(bytes(concatKeySecret, 'utf-8'))
    bearerCredentialsString = str(bearerCredentialsBytes)[2:-1]
    return bearerCredentialsString


#create the bearer token to use in twitter api calls
def create_bearer_token(bearerCredentials):
    bearerHeaders = {
        "Authorization": "Basic " + bearerCredentials,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }
    bearerParams = {
        "grant_type": "client_credentials"
    }

    access_token = requests.post("https://api.twitter.com/oauth2/token", headers=bearerHeaders, data=bearerParams).json()['access_token']
    return access_token


#function to search for all tweets - a fallback in case the premium rate limit has been reached
def twitter_search(bearerToken):
    baseUrl = "https://api.twitter.com/1.1/search/tweets.json"
    params = {
        "q": {
            "#dctech filter:twimg",
        },
        "count": "100"
    }
    stockHeader = {
    "Authorization": "Bearer " + bearerToken
    }
    #
    tweets = requests.get(baseUrl, headers=stockHeader, params=params).json()
    tweetsInfo = tweets["statuses"]
    tweetDict = {}
    #call the retweet_count function (below) to add the tweets to a dictionary where the keys are the number of retweets and the values for each key is the source url
    retweet_count(tweetsInfo, tweetDict)
    #iterate through the pages to get all of the results from the query and add them to the dictionary
    while('next_results' in tweets['search_metadata']):
        nextUrl = baseUrl + tweets['search_metadata']['next_results']
        tweets = requests.get(nextUrl, headers=stockHeader).json()
        tweetsInfo = tweets["statuses"]
        retweet_count(tweetsInfo, tweetDict)
    return tweetDict

#premium search to return a dictionary where the keys are the number of retweets and the values for each key is the source url
def twitter_search_premium(bearerToken):
    baseUrl = "https://api.twitter.com/1.1/tweets/search/fullarchive/fulldev.json"
    params = {
        "query": {
            "#dctech has:images"
        },
    }
    stockHeader = {
    "Authorization": "Bearer " + bearerToken
    }
    #return a list of tweets that match the above criteria of parameters
    tweets = requests.get(baseUrl, headers=stockHeader, params=params).json()
    #add the results into a dictionary with retweet_counts function
    tweetDict = {}
    retweet_count(tweets['results'], tweetDict)
    #while additional results are available, go to the next oage of results to add to the dictionary
    #the count for the loop is an artificial limit, otherwise I would quickly hit the requests usage limit
    count = 1
    while('next' in tweets and count <= 2):
        #update the parameters with the next key to make the request for the next page
        count += 1
        params['next'] = tweets['next']
        tweets = requests.get(baseUrl, headers=stockHeader, params=params).json()
        retweet_count(tweets['results'], tweetDict)
    #print(tweetDict)
    return tweetDict

#add the tweets from a search api call to add to a dictionary, keys=number of retweets and values=url of the tweet
def retweet_count(tweetList, tweetDict):
    for tweet in tweetList:
        tweetUrl = create_source_url(tweet['id_str'])
        #add the key and value to the dictionary if the key does not exist for the retweet count
        if tweet["retweet_count"] not in tweetDict:
            tweetDict[tweet["retweet_count"]] = [tweetUrl]
        #append the value to the list associated with the key if the key already exists
        else:
            tweetDict[tweet["retweet_count"]].append(tweetUrl)

#create the source url to put in the dictionary
def create_source_url(tweetId):
    return "https://twitter.com/statuses/" + str(tweetId)