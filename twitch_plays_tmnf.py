import sys
import getopt
from threading import Thread
from twitch_irc import TwitchIRC
import py_direct_input
import di_keyboard_scan_codes


class TwitchPlaysTMNF:
    def __init__(self):
        self.__up_thread = None
        self.__down_thread = None
        self.__left_thread = None
        self.__right_thread = None
        self.__enter_thread = None
        self.__honk_thread = None

    def handle(self, message):
        if "up" == message.lower() and (self.__up_thread == None or not self.__up_thread.is_alive()):
            self.__up_thread = Thread(target=py_direct_input.PressAndReleaseKey,
                                      args=(di_keyboard_scan_codes.DIK_UP, 1))
            self.__up_thread.start()

        if "down" == message.lower() and (self.__down_thread == None or not self.__down_thread.is_alive()):
            self.__down_thread = Thread(target=py_direct_input.PressAndReleaseKey,
                                        args=(di_keyboard_scan_codes.DIK_DOWN, 1))
            self.__down_thread.start()

        if "left" == message.lower() and (self.__left_thread == None or not self.__left_thread.is_alive()):
            self.__left_thread = Thread(target=py_direct_input.PressAndReleaseKey,
                                        args=(di_keyboard_scan_codes.DIK_LEFT, 0.5))
            self.__left_thread.start()

        if "right" == message.lower() and (self.__right_thread == None or not self.__right_thread.is_alive()):
            self.__right_thread = Thread(target=py_direct_input.PressAndReleaseKey,
                                         args=(di_keyboard_scan_codes.DIK_RIGHT, 0.5))
            self.__right_thread.start()

        if "enter" == message.lower() and (self.__enter_thread == None or not self.__enter_thread.is_alive()):
            self.__enter_thread = Thread(target=py_direct_input.PressAndReleaseKey,
                                         args=(di_keyboard_scan_codes.DIK_RETURN, 1))
            self.__enter_thread.start()

        if "honk" == message.lower() and (self.__honk_thread == None or not self.__honk_thread.is_alive()):
            self.__honk_thread = Thread(target=py_direct_input.PressAndReleaseKey,
                                        args=(di_keyboard_scan_codes.DIK_NUMPAD0, 1))
            self.__honk_thread.start()


def main(argv):
    usage = "twitch_plays_tmnf.py -p <password> -u <username> [-c <channel>]"
    password = None
    username = None
    channel = None

    try:
        opts, args = getopt.getopt(
            argv, "hp:u:c:", ["password=", "username=", "channel="]
        )
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        if opt in ("-p", "--password"):
            password = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-c", "--channel"):
            channel = arg

        if not channel:
            channel = username

    if password and username and channel:
        twitch_irc = TwitchIRC(password, username, channel, TwitchPlaysTMNF())
        twitch_irc.connect()
        twitch_irc.run()
    else:
        print(usage)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
