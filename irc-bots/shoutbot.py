#!/usr/bin/python

# pip install irc
from irc.bot import SingleServerIRCBot

import sys

# import logging
# logging.basicConfig(level=logging.DEBUG)

class ShoutBot(SingleServerIRCBot):
    def __init__(self, host, port, channel, nick):
        super().__init__([(host, port)], nick, nick)

        self.channel = channel
        self.nick = nick

    def on_welcome(self, conn, event):
        print(f"Event: {event}")

        conn.join(self.channel)

    def on_privmsg(self, conn, event):
        print(f"Event: {event}")

    def on_pubmsg(self, conn, event):
        print(f"Event: {event}")

        text = event.arguments[0]

        if text.startswith(self.nick + ":") or text.startswith(self.nick + ","):
            self.handle_command(conn, event)

    def handle_command(self, conn, event):
        text = event.arguments[0][len(self.nick) + 1:]

        conn.privmsg(self.channel, f"{event.source.nick}, {text.lstrip().upper()}")

def main():
    try:
        address, channel = sys.argv[1:3]
    except ValueError:
        exit("Usage: shoutbot.py HOST[:PORT] CHANNEL [NICK]")

    try:
        nick = sys.argv[3]
    except IndexError:
        nick = "shoutbot"

    try:
        host, port = address.split(":", 1)
    except ValueError:
        host, port = address, 6667

    port = int(port)

    ShoutBot(host, port, channel, nick).start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
