import matplotlib.pyplot as plt
import numpy as np

from common import TOPICS
from telegrab_project.telegram.config import *
import os
from scipy.interpolate import make_interp_spline, BSpline
import streamlit as st


def pie(amount_dict_hebrew):
    labels = [word[::-1] for word in amount_dict_hebrew.keys()]
    sizes = list(amount_dict_hebrew.values())
    max_value = max(sizes)
    max_value_index = sizes.index(max_value)
    explode = [0.1 if x == max_value_index else 0 for x in range(len(sizes))]      # only "explode" the biggest slice
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


def bar_graph(amount_dict_hebrew):
    labels = [word[::-1] for word in amount_dict_hebrew.keys()]
    sizes = list(amount_dict_hebrew.values())
    y_pos = np.arange(len(labels))
    plt.barh(y_pos, sizes, align='center', alpha=0.5)
    plt.yticks(y_pos, labels)
    plt.xlabel('amount')
    plt.title('how much did the word appear?')
    plt.savefig(os.path.join(DATA_FOLDER_PATH, 'my_graph.png'), bbox_inches='tight', pad_inches=0.3)


def spline(x_values: list, y_values: list):
    """
    Description:
        make the plot curvey
    :return: x_smooth, y_smooth
    """
    y_values = np.array(list(y_values))
    range_x = np.array(range(len(x_values)))
    x_smooth = np.linspace(range_x.min(), range_x.max(), 100)
    spl = make_interp_spline(range_x, y_values, k=2)
    y_smooth = spl(x_smooth)
    return x_smooth, y_smooth

def week_plot(word_date_amount_dict: dict):
    wdad_trans = {TOPICS.get(key, key): word_date_amount_dict.get(key, "error") for key in word_date_amount_dict}
    date = datetime.now().strftime("%d-%m-%Y")
    graph_name = f"{DAYS}_days_back_from_{date}.png"
    fig, ax = plt.subplots()  # Create a figure and an axes.
    final_amounts_list = []
    index = 0
    for word in wdad_trans.keys():
        amount_used_sum = sum(wdad_trans[word].values())
        if amount_used_sum > 0: #remove words we did not use
            x_values, y_values = wdad_trans[word].keys(), wdad_trans[word].values()
            x_smooth, y_smooth = spline(x_values, y_values)
            ax.plot(x_smooth, y_smooth, label=str(word)[::-1],linewidth=3)
            plt.xticks(np.arange(len(x_values)), x_values, size=18, rotation=30)
            plt.yticks(size=20)
            final_amounts_list.append((index, amount_used_sum))
            index += 1
    ax.set_ylabel('מופעים'[::-1], size=30) # Add a y-label to the axes.
    ax.set_xlabel('תאריך'[::-1], size=30)
    ax.set_title(date + f"הופעות מילים בשבוע האחרון בלבנון תאריך-"[::-1], size=40)
    # plt.xticks(rotation=30)
    handles, labels = plt.gca().get_legend_handles_labels() # get handles and labels
    order = [element[0] for element in sorted(final_amounts_list, key=lambda tup: tup[1])][::-1] # specify order of items in legend
    ax.legend([handles[i] for i in order], [labels[i] for i in order], bbox_to_anchor=(1,1), loc="upper left", fontsize=20) # add legend to plot
    plt.subplots_adjust(right=0.8)
    fig = plt.gcf()
    fig.set_size_inches((15, 10), forward=False)
    fig.savefig(os.path.join(DATA_FOLDER_PATH, graph_name), dpi=500, bbox_inches='tight', pad_inches=0.1)
    st.pyplot(fig)
    
