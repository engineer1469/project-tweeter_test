import neca
from neca.events import *
from neca.generators import generate_data
from neca.events import emit
import json

tweet_history = []

@event("init")
def init(context, data):
    # Calls events based on parameters
    generate_data(
        data_file = "sports-20191117.txt",
        time_scale = 1,
        event_name = 'tweet',
        limit = 100000
    )

def identify_sport(text):
    if "soccer" in text:
        return 'Soccer'
    elif "football" in text:
        return 'Football'
    elif "basketball" in text:
        return 'Basketball'
    elif "cricket" in text:
        return 'Cricket'
    elif "volleyball" in text:
        return 'Volleyball'
    elif "rugby" in text:
        return 'Rugby'
    elif "baseball" in text:
        return 'Baseball'
    elif "tennis" in text:
        return 'Tennis'
    
    return 'none'


@event("tweet")
def my_event_handler(context, data):
    #emit("tweet_stream", data)

    tweet_history.append(data)

    # Save the tweet_history list to a JSON file
    with open('tweet_history.json', 'w') as f:
        json.dump(tweet_history, f)

    text_to_search = data['text'].lower()
    sport = identify_sport(text_to_search)

    if sport != 'none':
        emit("piechart", {"action": "add", "value": [sport, 1]})


@event("search")
def search(context, keyword):
    print("search triggered")
    # Read the tweet_history.json file
    with open('tweet_history.json', 'r') as f:
        tweet_history = json.load(f)

    # Search for the keyword in the tweets
    found_tweets = [tweet for tweet in tweet_history if keyword.lower() in tweet['text'].lower()]
    print(found_tweets)
    # Emit the found tweets
    for tweet in found_tweets:
        emit("tweet_stream", tweet)

neca.start()