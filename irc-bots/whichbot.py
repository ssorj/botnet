#!/usr/bin/python

from irc.bot import SingleServerIRCBot

import getpass
import os
import sys
import time

class WhichBot(SingleServerIRCBot):
    def __init__(self, host, port, channel, nick):
        super().__init__([(host, port)], nick, nick)

        self.nick = nick
        self.channel = channel

    def on_welcome(self, conn, event):
        print(f"on_welcome {event}")

        conn.join(self.channel)

    def on_privmsg(self, conn, event):
        print(f"on_privmsg {event}")

    def on_pubmsg(self, conn, event):
        print(f"on_pubmsg {event}")

        text = event.arguments[0]

        if text.startswith(self.nick + ":") or text.startswith(self.nick + ","):
            self.handle_command(conn, event)

    def handle_command(self, conn, event):
        text = event.arguments[0][len(self.nick) + 1:]

        conn.privmsg(self.channel, f"{event.source.nick}, uptime: {get_uptime()}")

def make_nick():
    return f"{get_user()}-{get_host()}-{get_os()}"[:31]

def get_user():
    return getpass.getuser()

def get_host():
    return os.uname().nodename

def get_os():
    os_ = os.uname().sysname.lower()

    if os.path.exists("/etc/os-release"):
        fields = dict([line.strip().split("=", 1) for line in open("/etc/os-release")])
        os_ = f"{fields['ID']}-{fields['VERSION_ID']}"

    return os_

def get_uptime():
    return round(time.clock_gettime(time.CLOCK_BOOTTIME) / 86400, 1)

def main():
    try:
        address, channel = sys.argv[1:3]
    except ValueError:
        exit("Usage: whichbot.py HOST[:PORT] CHANNEL [NICK]")

    try:
        nick = sys.argv[3]
    except IndexError:
        nick = make_nick()

    try:
        host, port = address.split(":", 1)
    except ValueError:
        host, port = address, 6667

    port = int(port)

    WhichBot(host, port, channel, nick).start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
