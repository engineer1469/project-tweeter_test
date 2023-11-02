import neca
from neca.events import *
from neca.generators import generate_data
from neca.events import create_context, Ruleset
from neca.events import emit
from neca.settings import app, socket
from flask import Flask, request, send_file, jsonify
from wordcloud import WordCloud
import json

import random

filter = create_context("Filter")
text_data = create_context("Texts")
tweet_history = []

# Words to ingnore in the wordcloud
ignore_words = [
    "https", "http", "RT", "co", "t", "v", "and", "the", "a", "CO",
    "with", "to", "in", "of", "by", "at", "you", "she", "he", "than", "from",
    "then", "not", "for", "It", "it", "I", "was", "your", "are", "is", "on",
    "the", "an", "is", "that", "on", "as", "an", "in", "or", "at", "who", "which",
    "our", "by", "this", "these", "those", "with", "when", "where", "why", "how",
    "can", "will", "should", "could", "would", "did", "does", "do", "am", "were",
    "be", "has", "have", "had", "up", "down", "out", "over", "under", "off", "on",
    "above", "below", "between", "among", "beside", "before", "after", "during",
    "while", "since", "against", "through", "into", "onto", "upon", "about", "towards"
]

# Color for the word cloud
colors = [
    "#FF6384",
    "#36A2EB",
    "#4BC0C0",
    "#BC3A4E",
    "#701FBF",
    "#E4E533",
    "#ECAF14",
    "#3B344E" 
]

def specific_colors(word, font_size, position, orientation, random_state=None, **kwargs):
    return random.choice(colors)

@app.route('/generate_wordcloud')
def generate_wordcloud():
    wordcloud = WordCloud(width=300, height=200, background_color='white', collocations=False,
        color_func=specific_colors, max_words=1000, stopwords=ignore_words).generate(text_data['texts'])

    wordcloud.to_file("wordcloud.png")

    return send_file("wordcloud.png", mimetype='image/png')

@event("init")
def init(context, data):
    generate_data(
        data_file = "sports-20191117.txt",
        time_scale = .5,
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

@app.route('/buttons', methods=['POST'])
def route():
    data = request.json 
    filter['filter'] = data['id']
    return 'caught response', 200

@event("tweet")
def my_event_handler(context, data):
    if 'tennis' in data['text'].lower():
        emit("tennisTweetStream", data)

    current_filter = filter['filter']
    if current_filter == 'none':
        emit("tweet_stream", data)
    elif current_filter in data['text'].lower():
        emit("tweet_stream", data)
    else:
        return None

    text_to_search = data['text'].lower()
    sport = identify_sport(text_to_search)

    if sport != 'none':
        emit("piechart", {"action": "add", "value": [sport, 1]})
        text_data['texts'] += data['text']
        
       
@app.route('/search', methods=['POST'])
def search():
    print("search triggered")
    try:
        keyword = request.json.get('keyword')
        with open('tweet_history.json', 'r') as f:
            tweet_history = json.load(f)
        
        data = request.json
        keyword = data['keyword']
        found_tweets = [tweet for tweet in tweet_history if keyword.lower() in tweet['text'].lower()]
        print(found_tweets)
            # Emit the found tweets
        for tweet in found_tweets:
            emit("tweet_stream", tweet)

        return jsonify(found_tweets)
    except json.JSONDecodeError as e:
        app.logger.error(f'JSON decode error in tweet_history.json: {e}')
        return jsonify({'error': 'Invalid JSON format in tweet_history.json'}), 500
    except Exception as e:
        app.logger.error(f'Unexpected error: {e}')
        return jsonify({'error': 'An unexpected error occurred'}), 500
        
filter['filter'] = 'none'
text_data['texts'] = 'sport'

neca.start()