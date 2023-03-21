#!/usr/bin/python

# pip install irc
# pip install requests

from irc.bot import SingleServerIRCBot

import requests
import sys

# import logging
# logging.basicConfig(level=logging.DEBUG)

class UrlBot(SingleServerIRCBot):
    def __init__(self, host, port, channel, nick):
        super().__init__([(host, port)], nick, nick)

        self.nick = nick
        self.channel = channel

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

        response_lines = self.send_request(text)

        for line in response_lines:
            conn.privmsg(self.channel, f"{event.source.nick}: {line}")

    def send_request(self, text):
        args = text.strip().split()
        response = None

        try:
            if not args:
                raise Exception("Empty request")

            operation = args[0].lower()

            if operation == "help":
                raise Exception("Usage: <method> <url> [<json>]")

            if operation == "get":
                response = requests.get(args[1], timeout=2)
            elif operation == "post":
                response = requests.post(args[1], json=" ".join(args[2:]), timeout=2)
            elif operation == "put":
                response = requests.put(args[1], json=" ".join(args[2:]), timeout=2)
            else:
                raise Exception(f"I don't understand the request: {args}")
        except Exception as e:
            message = str(e).replace("\n", "\\n")
        else:
            message = f"{response.status_code} {response.reason}"

        lines = [message]

        if response is not None:
            for i, line in enumerate(response.text.rstrip().split("\n")):
                if i > 20:
                    lines.append("[...]")
                    break

                lines.append(line)

        return lines

def main():
    try:
        address, channel = sys.argv[1:3]
    except ValueError:
        exit("Usage: main.py HOST[:PORT] CHANNEL [NICK]")

    try:
        nick = sys.argv[3]
    except IndexError:
        nick = "urlbot"

    try:
        host, port = address.split(":", 1)
    except ValueError:
        host, port = address, 6667

    port = int(port)

    print(f"Connecting to {host}:{port} and joining {channel} as {nick}")

    UrlBot(host, port, channel, nick).start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
