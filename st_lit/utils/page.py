import json
import random
import string
from datetime import datetime, timedelta
import time
import streamlit as st
from common import *
from telegrab_project import telegram_words_plot, count_words_in_messages, PATH_TO_ALL_MESSAGES, CHANNELS, get_messages, \
    add_channel, get_channels_list, reset_channels, add_word, reset_words, get_tele_word_list
from twit import fetch_trending, LEBANON_WOEID, get_tweet_speed


def config_page():
    st.set_page_config(
        page_title="prototype dashboard",
        page_icon="🪖",
        # layout="wide",
    )
    st.title("Real-Time Data  Dashboard")


def sidebar_select():
    with st.sidebar:
        selection1 = st.radio(
            "Select a social network: ",
            ("Telegram", "Twitter", "Facebook", "TikTok")
        )
        return selection1



def add_word_search():
    st.text_input("your word", key="search_word")


def twitter_graph():
    word = st.session_state.search_word
    word_list = WORD_LIST + [word]
    fetch_trending(word_list, place_woeid=LEBANON_WOEID, word=word)


def twitter_word_pace():
    word = st.session_state.search_word
    volume_list = []
    with st.empty():
        while True:
            volume = get_tweet_speed(word)
            volume_list.append(volume)
            st.line_chart(data=volume_list, width=0, height=0, use_container_width=True)
            time.sleep(1)


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
    col1, col2= st.columns(2)
    with col1:
        st.button(label="add_word", key="add_word_button")
    with col2:
        st.button(label="reset telegram words", key="reset_tele_words")
    if st.session_state.add_word_button and st.session_state.new_word:
        add_word(st.session_state.new_word)
    if st.session_state.reset_tele_words:
        reset_words()
    st.write("current words:")
    st.write(" \n".join(["* "+word for word in get_tele_word_list()]))


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
        add_word_search()
        st.write("most trending hashtags graph")
        twitter_graph()
        st.write("tweets per hour graph")
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
            telegram_words()
            date_range = telegram_dates()
            st.button(label="plot graph", key="plot_graph_button")
            if st.session_state.plot_graph_button:
                tele_word_list = get_tele_word_list()
                telegram_graph(word_list=tele_word_list, date_range=date_range)


    elif selection1 == "Facebook":
        st.write("coming soon...")

    elif selection1 == "TikTok":
        st.write("coming soon...")
