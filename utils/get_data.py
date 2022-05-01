import requests
import os
import json
import pprint
import jq
# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "AAAAAAAAAAAAAAAAAAAAABrLbwEAAAAAjtpxBEPr02j6RkRHJPJYjmq1K9s%3Dst6vsfOsIJm0PGxgxGArLdoDHO1sY2FocLzTtjFOFlaEk3X8fc"


def tweet_contain_word_url(search_word: str) -> str:
    """
    :param hashtag: string you want tweets to contain
    :return: returns url to searh for tweets containing the string
    """
    url = f"https://api.twitter.com/1.1/search/tweets.json?q={search_word}"
    return url


def tweet_contain_hasgtag_url(hashtag: str) -> str:
    """
    :param hashtag: string of the wanted hashtag (without the # the func adds it)
    :return: returns url to searh for tweets containing the hashtahg
    """
    url = f"https://api.twitter.com/1.1/search/tweets.json?q=%23{hashtag}"
    return url


def trends_in_place_url(place_woid):
    """
    :param place_woid: search web for woid for the wanted place
    :return: url to get first 50 trending in this place
    """
    url = f"https://api.twitter.com/1.1/trends/place.json?id={place_woid}"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
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


def do():
    url = tweet_contain_hasgtag_url("انتخابات")
    json_response = connect_to_endpoint(url)
    print(len(json_response['statuses']))

