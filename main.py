from utils import *
from config import *



def main():
    my_dict = create_word_speed_dict(word_list=WORD_LIST)
    bar_graph(my_dict, "try")



if __name__ == '__main__':
    main()


