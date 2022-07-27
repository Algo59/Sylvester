import json
import random
import string
import numpy as np
import matplotlib
from datetime import datetime, timedelta
import time
import streamlit as st
from common import *
from telegrab_project import telegram_words_plot, count_words_in_messages, CHANNELS, get_messages, \
    add_channel, get_channels_list, reset_channels, add_tele_word, reset_tele_words, get_tele_word_list, \
    remove_tele_word
from PIL import Image
from twit import fetch_trending, LEBANON_WOEID, get_word_tweet_speed, twitter_word_pace_graph_data, reset_twit_words, \
    get_twit_word_list, add_twit_word, remove_twit_word, add_twitter_words_data_row, word_list_big_line_graph, \
    get_prev_day_twit_data, word_pace_line_graph, get_prev_hour_twit_data
import pandas as pd

def config_page():
    st.set_page_config(
        page_title="prototype dashboard",
        page_icon="🪖",
        layout="wide",
    )
    st.title("Real-Time Data  Dashboard")
    # lets change default colors
    matplotlib.rcParams['text.color'] = TEXT_COLOR
    matplotlib.rcParams['axes.labelcolor'] = TEXT_COLOR
    matplotlib.rcParams['xtick.color'] = TEXT_COLOR
    matplotlib.rcParams['ytick.color'] = TEXT_COLOR
    matplotlib.rcParams['axes.facecolor'] = BACKGROUND_COLOR
    matplotlib.rcParams['legend.facecolor'] = BACKGROUND_COLOR
    matplotlib.rcParams['figure.facecolor'] = BACKGROUND_COLOR


def sidebar_select():
    with st.sidebar:
        selection1 = st.radio(
            "Select a social network: ",
            ("Twitter", "Telegram")
        )
        return selection1



def add_word_search():
    st.text_input("your word", key="search_word")


def twitter_graph():
    fetch_trending(place_woeid=LEBANON_WOEID)




def twitter_word_pace(word_list):
    """
    for every word in list check pace every time interval and show all words graphs on dashboard
    :param word_list: list of words we check pace and show on dashboard
    :return:
    """
    big_graph = st.empty()
    objs = []
    columns = st.columns(3)
    for i, word in enumerate(word_list):
        col = i % 3
        with columns[col]:
            objs.append(st.empty())
    while True:
        # get new data
        current_volume_dict = twitter_word_pace_graph_data(word_list)
        add_twitter_words_data_row(current_volume_dict)  # save to knowledge
        # get 24 hour and 1 hour data
        day_data_df = get_prev_day_twit_data()
        hour_data_df = get_prev_hour_twit_data()
        #lets update the plot with the data we fetched
        with big_graph.container(): #update big graph
            fig = word_list_big_line_graph(data_df=day_data_df, word_list=word_list)
            st.pyplot(fig=fig)
        for i, word in enumerate(word_list): #update small graphs
            with objs[i].container():
                st.pyplot(word_pace_line_graph(data_df=hour_data_df,word=word, index=i))
        time.sleep(10*60)



def telegram_graph(word_list, date_range):
    message_dict = get_messages()
    wdad = count_words_in_messages(all_messages_dict=message_dict, word_list=word_list, date_range=date_range) #word_date_amount_dict
    telegram_words_plot(wdad)


def telegram_channels():
    st.text_input("Add channel: ", key="new_channel")
    st.button(label="add_channel", key="add_button")
    st.button(label="reset_channels", key="reset_channels")
    st.write("Notice! \n channels wil be added only after running telegram_get_messages.py")
    if st.session_state.add_button and st.session_state.new_channel:
        add_channel(st.session_state.new_channel)
    if st.session_state.reset_channels:
        reset_channels()
    st.write("current channels:")
    st.write(" \n".join(["* "+channel for channel in get_channels_list()]))


def telegram_words():
    st.text_input("Add word: ", key="new_word")
    col1, col2, col3= st.columns(3)
    with col1:
        st.button(label="add_word", key="add_word_button")
    with col2:
        st.button(label="remove last word", key="remove_last_tele_word")
    with col3:
        st.button(label="reset telegram words", key="reset_tele_words")
    if st.session_state.add_word_button and st.session_state.new_word:
        add_tele_word(st.session_state.new_word)
    if st.session_state.remove_last_tele_word:
        remove_tele_word()
    if st.session_state.reset_tele_words:
        reset_tele_words()
    st.write("current words:")
    st.write(" \n".join(["* "+word for word in get_tele_word_list()]))


def twitter_words():
    st.text_input("Add word: ", key="new_word")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button(label="add_word", key="add_word_button")
    with col2:
        st.button(label="remove last word", key="remove_last_twit_word")
    with col3:
        st.button(label="reset twitter words", key="reset_twit_words")
    if st.session_state.add_word_button and st.session_state.new_word:
        add_twit_word(st.session_state.new_word)
    if st.session_state.remove_last_twit_word:
        remove_twit_word()
    if st.session_state.reset_twit_words:
        reset_twit_words()
    st.write("current words:")
    st.write(" \n".join(["* "+word for word in get_twit_word_list()]))


def telegram_dates():
    st.subheader("Choose Date Range")
    end_day, start_day = st.select_slider(label ='Days Back From Today', value= (0,7), options=range(31))
    start_date = datetime.now() - timedelta(days=start_day)
    end_date = datetime.now() - timedelta(days=end_day)
    st.subheader(f"{start_date.strftime('%d/%m/%Y')}  -  {end_date.strftime('%d/%m/%Y')}")
    return [start_date, end_date]


def full_page():
    config_page()
    selection1 = sidebar_select()
    if selection1 == "Twitter":
        twit_selection2 = st.sidebar.radio(
            "Select a option: ",
            ("Live Word Graph", "Trending Now")
        )
        if twit_selection2 == "Live Word Graph":
            twitter_words()
            st.button(label="Plot Graphs", key="twit_plot_graphs_button")
            if st.session_state.twit_plot_graphs_button:
                twit_word_list = get_twit_word_list()
                twitter_word_pace(twit_word_list)
        if twit_selection2 == "Trending Now":
            st.subheader("Most Trending Hashtags Graph")
            twitter_graph()

    elif selection1 == "Telegram":
        tele_selection2 = st.sidebar.radio(
            "Select an option: ",
            ("add channels", "graph")
        )
        if tele_selection2 == "add channels":
            telegram_channels()
        if tele_selection2 == "graph":
            telegram_words()
            date_range = telegram_dates()
            st.button(label="plot graph", key="plot_graph_button")
            if st.session_state.plot_graph_button:
                tele_word_list = get_tele_word_list()
                telegram_graph(word_list=tele_word_list, date_range=date_range)

