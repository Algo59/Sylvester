import time
from twit.utils import *
from twit.config import *
import streamlit as st
import random
import string
from telegrab_project import PATH_TO_ALL_MESSAGES, count_words_in_messages, week_plot, WORD_LIST



def add_new_row():
    key = random.choice(string.ascii_uppercase) + str(random.randint(0, 999999))
    st.text_input("channel link:", key=key)
    return key


def main():
    if "your_word" not in st.session_state:
        st.text_input("your_word", key="search_word")
    button = st.button("do")
    if button:
        word = st.session_state.search_word
        WORD_LIST.append(word)
        fetch_trending(WORD_LIST, place_woeid=LEBANON_WOEID, word=word)
        volume_list = []
        with open(PATH_TO_ALL_MESSAGES, "r", encoding="utf-8") as dict_file:
            all_messages_dict = json.load(dict_file)
            word_date_amount_dict = count_words_in_messages(all_messages_dict)
            week_plot(word_date_amount_dict)
        with st.empty():
            for second in range(40):
                volume = get_tweet_speed(word)
                volume_list.append(volume)
                st.line_chart(data=volume_list, width=0, height=0, use_container_width=True)
                time.sleep(0.5)

    if 'count' not in st.session_state:
        st.session_state.count = 0
    key_list = []
    if st.button("Add new channel"):
        st.session_state.count += 1
        new_key = add_new_row()
        key_list.append(new_key)
        if st.session_state.count > 1:
            for i in range(st.session_state.count - 1):
                add_new_row()




    # You can access the value at any point with:
    # my_dict = create_word_speed_dict(word_list=WORD_LIST)
    # path = tweets_speed_bar_graph(my_dict)
    # send_file(to="me", path=path)

if __name__ == '__main__':
    main()



