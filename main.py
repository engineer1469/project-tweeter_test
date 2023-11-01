import neca
from neca.events import *
from neca.generators import generate_data
from neca.events import emit

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
    emit("tweet_stream", data)

    text_to_search = data['text'].lower()
    sport = identify_sport(text_to_search)

    if sport != 'none':
        emit("piechart", {"action": "add", "value": [sport, 1]})


@event("search")
def searh(keyword):
    print(keyword)
    return "testmessage"

neca.start()