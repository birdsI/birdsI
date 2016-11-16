import tweepy
import requests
import json

def getQuery(search):
    auth = tweepy.OAuthHandler("twNhhecIepDYG96kskAz9BGkN", "2R1MlphQLHoTiewP4Pr44G7ciq9w1fqn655gFMDaCukdzJ0wIn")
    auth.set_access_token("256809537-cnBfkQoODpw4k1Vm1oR5MIkRqVLfgNSGJBDkkYZG", "M1NTBK24VJSRKhtTgIBoaKxAc3RpxTRdesmqGQ8gOxPui") #Ignore my secrets lol
    api = tweepy.API(auth)
    searchresults = api.search(q=search, count = 10, lang="en")
    presentiment = []
    negcount = 0
    negcountn = 0
    poscount = 0
    poscountn = 0
    neutcount = 0
    neutcountn = 0
    url = "http://sentiment.vivekn.com/api/text/"
    for tweet in searchresults:
        payload = {'txt': tweet.text}
        respraw = requests.post(url, data=payload)
        resp = json.loads(respraw.text)
        presentiment.append((resp['result']['sentiment'], resp['result']['confidence']))
    for element in presentiment:
        if element[0] == 'Negative':
            negcount += float(element[1])
            negcountn += 1
        elif element[0] == 'Neutral':
            neutcount += float(element[1])
            neutcountn += 1
        elif element[0] == 'Positive':
            poscount += float(element[1])
            poscountn += 1

    sentdict = [poscount, neutcount, negcount, poscountn, negcountn, neutcountn ]
    return json.dumps(sentdict)
