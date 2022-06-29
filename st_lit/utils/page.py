import json
import random
import string
import time
import streamlit as st
from common import *
from telegrab_project import week_plot, count_words_in_messages, PATH_TO_ALL_MESSAGES, CHANNELS, get_messages, \
    add_channel, get_channels_list, reset_channels
from twit import fetch_trending, LEBANON_WOEID, get_tweet_speed


def config_page():
    st.set_page_config(
        page_title="prototype dashboard",
        page_icon="🪖",
        layout="wide",
    )
    st.title("Real-Time / Live Data  Dashboard")


def sidebar_select():
    with st.sidebar:
        selection1 = st.radio(
            "Select a social network: ",
            ("Telegram", "Twitter", "Facebook", "TikTok")
        )
        return selection1



def add_word_search():
    if "your_word" not in st.session_state:
        st.text_input("your_word", key="search_word")


def twitter_graph():
    word = st.session_state.search_word
    WORD_LIST.append(word)
    fetch_trending(WORD_LIST, place_woeid=LEBANON_WOEID, word=word)


def twitter_word_pace():
    word = st.session_state.search_word
    volume_list = []
    with st.empty():
        for second in range(40):
            volume = get_tweet_speed(word)
            volume_list.append(volume)
            st.line_chart(data=volume_list, width=0, height=0, use_container_width=True)
            time.sleep(3)


def telegram_graph():
    word = st.session_state.search_word
    if word:
        word_list = WORD_LIST + [word]
        message_dict = get_messages()
        wdad = count_words_in_messages(message_dict, word_list) #word_date_amount_dict
        week_plot(wdad)


def telegram_channels():
    st.text_input("Add channel: ", key="new_channel")
    st.button(label="add_channel", key="add_button")
    st.button(label="reset_channels", key="reset_channels")
    st.write("Notice! \n channels wil be added only after running telegram_get_messages.py")
    if st.session_state.add_button and st.session_state.new_channel:
        add_channel(st.session_state.new_channel)
    if st.session_state.reset_channels:
        reset_channels()
        pass
    st.write("current channels:")
    st.write(" \n".join(["* "+channel for channel in get_channels_list()]))




def full_page():
    config_page()
    selection1 = sidebar_select()
    if selection1 == "Twitter":
        selection2 = st.sidebar.radio(
            "Select a graph: ",
            ("tweets per hour", "most trending hashtags")
        )
        if selection2 == "most trending hashtags":
            st.write("most trending hashtags graph")
            twitter_graph()
        if selection2 == "tweets per hour":
            st.write("tweets per hour graph")
            add_word_search()
            if st.session_state.search_word:
                twitter_word_pace()

    elif selection1 == "Telegram":
        selection2 = st.sidebar.radio(
            "Select a option: ",
            ("add channels", "graph")
        )
        if selection2 == "add channels":
            telegram_channels()
        if selection2 == "graph":
            add_word_search()
            telegram_graph()


    elif selection1 == "Facebook":
        st.write("coming soon...")

    elif selection1 == "TikTok":
        st.write("coming soon...")
