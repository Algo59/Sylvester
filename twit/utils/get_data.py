import requests
import json
from twit.config.get_data import *
from dateutil import parser
from .show_data import *
from datetime import datetime, timezone

def all_tweets_contain_word_url(search_word: str, limit: int, is_hashtag:bool =False) -> str:
    """
    :param search_word: string to search in tweets
    :param limit: number of tweets
    :param since_id: id of tweet to fetch from its date
    :param is_hashtag: search string as hashtag
    :return: returns url to search for tweets containing the string
    """
    if is_hashtag:
        q = f"%23{search_word}"
    else:
        q = search_word
    url = f"https://api.twitter.com/1.1/search/tweets.json?q={q}&count={limit}"
    return url


def trends_in_place_url(place_woid):
    """
    :param place_woeid: search web for woeid for the wanted place
    :return: url to get first 50 trending in this place
    """
    url = f"https://api.twitter.com/1.1/trends/place.json?id={place_woid}"
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url: str) -> json:
    """
    :param url: url to request
    :return: the response json (or error code)
    """
    response = requests.request("GET", url, auth=bearer_oauth)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def print_tweets(json_response: dict):
    """
    :param json_response: response of tweets
    :return: print tweets nice
    """
    tweets = json_response['statuses']
    print(len(tweets))
    for index, tweet in enumerate(tweets):
        print(f"id = {tweet['id']}")
        print(f"date = {tweet['created_at']}")
        print(f"text = {tweet['text']} \n\n")


def fetch_trending(place_woeid: int) -> None:
    """
    check if one of the words in wordlist is trending in place
    :param place_woeid: get from web the place woeid
    :return: none but sends to me in telegrab_project the trending graph and alert if one of the words is trending
    """
    url = trends_in_place_url(place_woeid)
    res = connect_to_endpoint(url)[0]
    trendict = {}
    for trend in res['trends']:
        trend_name_clean = trend['name'].replace('#', '')
        if trend['tweet_volume'] != None:
            trendict[trend['name']] = trend['tweet_volume']
        else:
            # we multiply by 24 because other values in dictionary are tweet/day and this value is tweet/hour
            trendict[trend['name']] = get_tweet_speed(trend_name_clean, is_hashtag=(trend_name_clean != trend['name']))*24
        # for word in word_list:
        #     if word in trend_name_clean or trend_name_clean in word:
        #         text = f"ALERT: \n {TOPICS[word]} is trending in {place_woeid} as '{trend['name']}' in volume of {trend['tweet_volume']}" \
        #                f"the last 24 hours (check time is {res['as_of']})"
        #         # send_message(to="me", text="Good morning, here are the trends for today:")
    graph_path = trend_bar_graph(trendict)
    # send_file(to="me", path=graph_path)


def get_tweet_speed(word: str, is_hashtag: bool = False) -> float:
    """
    Description:
        we can only fetch 100 tweets so we check the time delta between now and the oldest tweet (from the
        100) as td and then the speed is 100 tweets in td. to convert to tweets/hour we divide by amount of hors in td.
    :param word: word to search tweet speed for
    :return: float of average tweet speed (tweets/hour) in moment of search
    """
    url = all_tweets_contain_word_url(search_word=word, limit=100, is_hashtag=is_hashtag)
    json_response = connect_to_endpoint(url)
    tweets = json_response['statuses']
    tweets_amount = len(tweets)
    date_list = []
    for index, tweet in enumerate(tweets):
        date = parser.parse(tweet['created_at'])
        date_list.append(date)
    date_list = sorted(date_list)
    if len(date_list) > 1:
        oldest_date = date_list[0]
        newest_date = date_list[-1]
        td = datetime.now(timezone.utc) - oldest_date
        #todo check sec amount if true
        speed = tweets_amount / (td.total_seconds()/60/60)
        return speed
    else:
        return 0


def twitter_word_pace_graph_data(word_list):
    """
    Description:
    get the data for one frame all words you want to show in twiter word-pace graph- that shows the word volume (twits per hour)
    live.
    :param word_list: list of words to check volume
    :return: volume_dict: a dictionary of words as keys and dict of hour and volume as values
    """
    volume_dict = {word: 0 for word in word_list}
    for i, word in enumerate(word_list):
        volume = get_tweet_speed(word)
        hour = datetime.now().strftime("%H:%M:%S")
        volume_dict[word] = {"hour" : hour, word : volume}
    return volume_dict

def create_word_speed_dict(word_list: list) -> dict:
    """
    :param word_list: list of wordsd to check tweet speed for
    :return: dictionary where words are keys and tweet speeds are values
    """
    word_speed_dict = {word : get_tweet_speed(word) for word in word_list}
    return word_speed_dict


