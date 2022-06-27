from telegrab_project import *
import os
import json
import streamlit as st

def main():
    # amount_dict = get_temp_dict()
    amount_dict = None
    if not amount_dict:
        amount_dict = count_words_in_messages()
        save_temp_dict(amount_dict)
    wdad_trans = {TOPICS[key] : amount_dict[key] for key in amount_dict}
    # cdad_trans = {(TOPICS[word] for word in key) : amount_dict[key] for key in amount_dict}
    print(f"\n\n hebrew dict: {wdad_trans}")
    date = datetime.now().strftime("%d-%m-%Y")
    graph_name = f"{DAYS}_days_back_from_{date}.png"
    week_plot(wdad_trans, graph_name=graph_name)
    # send_file(to="me", path=os.path.join(DATA_FOLDER_PATH, graph_name))
    

if __name__ == '__main__':
    main()
