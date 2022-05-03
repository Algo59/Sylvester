import matplotlib.pyplot as plt
import numpy as np
import os
from config import DATA_FOLDER_PATH, TOPICS
import re

def trend_bar_graph(amount_dict_hebrew, date, place):
    labels = [word[::-1] if not word.replace("#",'')[1].isalpha() else word for word in amount_dict_hebrew.keys()]
    sizes = list(amount_dict_hebrew.values())
    print(amount_dict_hebrew)
    y_pos = np.arange(len(labels))
    plt.barh(y_pos, sizes, align='center', alpha=0.5)
    plt.yticks(y_pos, labels)
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.xlabel('amount')
    plt.title(f"trend volume last 24 hours in {place} (as of {date})")
    graph_name = f"trends_in_{place}_{date}.png"
    path = os.path.join(DATA_FOLDER_PATH, graph_name)
    plt.savefig(path, bbox_inches='tight', pad_inches=0.3)
    return path


def bar_graph(amount_dict, title):
    labels = [TOPICS[word][::-1] for word in amount_dict.keys()]
    sizes = list(amount_dict.values())
    y_pos = np.arange(len(labels))
    plt.barh(y_pos, sizes, align='center', alpha=0.5)
    plt.yticks(y_pos, labels)
    plt.xticks(size=10)
    plt.yticks(size=10)
    plt.xlabel('tweets in hour')
    plt.ylabel('word')
    plt.title(title)
    plt.show()