from telegrab_project.telegram import *


def main():
    if get_channels_list():
        channels = get_channels_list()
    else:
        save_channels_list(CHANNELS)
        channels = CHANNELS
    channels = set(channels)
    save_all_messages(channels)

if __name__ == '__main__':
    main()
