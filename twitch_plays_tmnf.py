import sys
import getopt
from threading import Thread
from twitch_irc import TwitchIRC
import py_direct_input
import di_keyboard_scan_codes


def handle(message):
    if "up" == message.lower():
        Thread(target=py_direct_input.PressAndReleaseKey,
               args=(di_keyboard_scan_codes.DIK_UP, 1)).start()
    if "down" == message.lower():
        Thread(target=py_direct_input.PressAndReleaseKey,
               args=(di_keyboard_scan_codes.DIK_DOWN, 1)).start()
    if "left" == message.lower():
        Thread(target=py_direct_input.PressAndReleaseKey,
               args=(di_keyboard_scan_codes.DIK_LEFT, 0.5)).start()
    if "right" == message.lower():
        Thread(target=py_direct_input.PressAndReleaseKey,
               args=(di_keyboard_scan_codes.DIK_RIGHT, 0.5)).start()


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
        twitch_irc = TwitchIRC(password, username, channel, handle)
        twitch_irc.connect()
        twitch_irc.run()
    else:
        print(usage)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
