from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
from twit.config import DATA_FOLDER_PATH, TOPICS
import seaborn
import streamlit as st

def trend_bar_graph(amount_dict_hebrew: dict, word):
    """
    :param amount_dict_hebrew: trend-volume dict
    :param date: date of trends fetch
    :param place: name(string) or woeid
    :return: path to graph ready
    """
    labels = []
    sizes = []
    tup = amount_dict_hebrew.items()
    counter, nums_to_bold = 0, None
    for key, value in sorted(tup, key= lambda x: x[1])[-23:]:
        if word in key:
            labels.append(key)
            nums_to_bold = counter
        else:
            labels.append(key[::-1] if key.upper() == key else key)
        sizes.append(value/24)
        counter += 1
    print(amount_dict_hebrew)
    y_pos = np.arange(len(labels))
    fig, ax = plt.subplots()
    plt.barh(y_pos, sizes, align='center', alpha=0.5, color=seaborn.color_palette("rocket"))
    plt.yticks(y_pos, labels)
    plt.xticks(size=10)
    if nums_to_bold:
        ax.get_yticklabels()[nums_to_bold].set_color("red")
    plt.yticks(size=10)
    plt.xlabel("average tweets/hour speed")
    now = datetime.now().strftime('%d-%m-%y_%H:%M')
    plt.title(f"Most Trending Topics In Lebanon (as of {now})")
    graph_name = f"Trends_in_Lebanon_{now}.png"
    path = os.path.join(DATA_FOLDER_PATH, graph_name)
    plt.savefig(path, bbox_inches='tight', pad_inches=0.3)
    st.pyplot(fig=plt.gcf())
    return path


def tweets_speed_bar_graph(amount_dict: dict) -> None:
    """
    :param amount_dict: word-tweet_speed dict
    :return: show graph
    """
    labels = []
    sizes = []
    tup = amount_dict.items()
    for key, value in sorted(tup, key= lambda x: x[1]):
        labels.append(TOPICS[key][::-1])
        sizes.append(value)
    y_pos = np.arange(len(labels))
    plt.barh(y_pos, sizes, align='center', alpha=0.5, color=seaborn.color_palette("summer"))
    plt.yticks(y_pos, labels)
    plt.xticks(size=10)
    plt.yticks(size=10)
    now = datetime.now().strftime('%d-%m-%y %H:%M')
    plt.title(f"word tweets-speed (as of {now})", size=15)
    plt.xlabel('average tweets/hour speed')
    graph_name = f"word_tweets-speed_as_of_{now}.png"
    path = os.path.join(DATA_FOLDER_PATH, graph_name)
    plt.savefig(path, bbox_inches='tight', pad_inches=0.3)
    return path




