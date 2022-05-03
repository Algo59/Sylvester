from utils import *
from config import *



def main():
    my_dict = create_word_speed_dict(word_list=WORD_LIST)
    path = tweets_speed_bar_graph(my_dict)
    send_file(to="me", path=path)



if __name__ == '__main__':
    main()


