from datetime import datetime
import arabic_reshaper
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import pandas as pd
from common import *
import seaborn
import streamlit as st
from bidi.algorithm import get_display

def trend_bar_graph(amount_dict_hebrew: dict):
    """
    :param amount_dict_hebrew: trend-volume dict
    :param date: date of trends fetch
    :param place: name(string) or woeid
    :return: path to graph ready
    """
    labels = []
    sizes = []
    tup = amount_dict_hebrew.items()
    for key, value in sorted(tup, key= lambda x: x[1])[-23:]:
        labels.append(key[::-1] if key.upper() == key else key)
        sizes.append(value/24)
    print(amount_dict_hebrew)
    y_pos = np.arange(len(labels))
    fig, ax = plt.subplots()
    plt.barh(y_pos, sizes, align='center', alpha=0.5, color=seaborn.color_palette("rocket"))
    plt.yticks(y_pos, labels)
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.xlabel("average tweets/hour speed")
    now = datetime.now().strftime('%d-%m-%y_%H:%M')
    plt.title(f"Most Trending Topics In Lebanon (as of {now})")
    graph_name = f"Trends_in_Lebanon_{now}.png"
    path = os.path.join(TWIT_DATA_FOLDER_PATH, graph_name)
    # plt.savefig(path, bbox_inches='tight', pad_inches=0.3)
    fig.set_size_inches((12, 7), forward=False)
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
    path = os.path.join(TWIT_DATA_FOLDER_PATH, graph_name)
    plt.savefig(path, bbox_inches='tight', pad_inches=0.3)
    return path


def word_list_big_line_graph(data_df: pd.DataFrame, word_list: list) :
    """
    :param data_df: twitter data df of all word knowledge we have
    :param word_list: words we want to show on dashboard
    :return: a fig of line plot of all volume forwords for last 24 hours
    """
    big_graph_df = data_df.copy() #not editing the real df
    big_graph_df['date'] = big_graph_df['date'].apply(lambda date: datetime.strftime(date, "%H:%M")) #change date to str
    fig, ax = plt.subplots()  # Create a figure and an axes.
    # add line plot for every word
    for i, word in enumerate(word_list):
        word_data = big_graph_df[[word, 'date']].dropna(subset=[word])
        x_values, y_values = word_data['date'].tolist(), word_data[word].tolist()
        ax.plot(x_values, y_values, label=get_display(arabic_reshaper.reshape(word)), linewidth=3, color=COLOR_LIST[i])
        plt.xticks(np.arange(len(x_values)), x_values, rotation=30, size=10)  # add all date ticks
    plt.yticks() #add yticks
    #add lables and header
    ax.set_ylabel('טוויטים לשעה'[::-1], size=10)
    # ax.set_xlabel('תאריך'[::-1], size=10)
    ax.set_title(f"מגמות מילים בטוויטר"[::-1], size=15)
    handles, labels = plt.gca().get_legend_handles_labels()  # get handles and labels for legend
    ax.legend(handles, labels, bbox_to_anchor=(1, 1), loc="upper left", fontsize=10)  # add legend to plot
    plt.subplots_adjust(right=0.8)
    fig = plt.gcf()
    fig.set_size_inches((12, 3), forward=False)
    return fig


def word_pace_line_graph(data_df: pd.DataFrame, word: str, index: int):
    """
    :param index: index of word for color match
    :param data_df: twitter data df of all word knowledge we have
    :param word: word we want to show on graph
    :return: fig of word pace graph
    """
    fig = plt.figure()
    ax = plt.axes()
    ax.set_title(get_display(arabic_reshaper.reshape(word)), size=14, fontdict=None)
    line_df = data_df.copy()
    line_df['date'] = line_df['date'].apply(lambda date: datetime.strftime(date, "%H:%M"))
    word_data = line_df[[word, 'date']].dropna(subset=[word])
    x_values, y_values = word_data['date'].tolist(), word_data[word].tolist()
    ax.plot(x_values, y_values, color=COLOR_LIST[index])
    plt.xticks(rotation=30, size=8)
    # add half of date ticks to add clearness
    # x_values = [x if i % 2 == 0 else ' ' for i, x in enumerate(x_values)]
    # plt.xticks(np.arange(len(x_values)), x_values, size=8, rotation=30)
    plt.yticks(size=8)
    ax.set_ylabel('טוויטים לשעה'[::-1], size=10)
    fig.set_size_inches((5, 2), forward=False)
    return fig


