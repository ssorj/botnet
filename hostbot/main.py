#!/usr/bin/python

from irc.bot import SingleServerIRCBot

import getpass
import os
import sys
import thingid
import time

# import logging
# logging.basicConfig(level=logging.DEBUG)

class HostBot(SingleServerIRCBot):
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

        conn.privmsg(self.channel, f"{event.source.nick}: Hostname: {get_hostname()}")
        conn.privmsg(self.channel, f"{event.source.nick}: Uptime:   {get_uptime()} days")
        conn.privmsg(self.channel, f"{event.source.nick}: OS:       {get_os()}")
        conn.privmsg(self.channel, f"{event.source.nick}: CPU:      {get_cpu()}")

def make_nick():
    return thingid.generate_thing_id()[:31]

def get_hostname():
    return os.uname().nodename

def get_uptime():
    return round(time.clock_gettime(time.CLOCK_BOOTTIME) / 86400, 1)

def get_os():
    os_ = os.uname().sysname.lower()

    if os.path.exists("/etc/os-release"):
        fields = dict([line.strip().split("=", 1) for line in open("/etc/os-release")])
        os_ = f"{fields['ID']}-{fields['VERSION_ID']}"

    return os_

def get_cpu():
    for line in open("/proc/cpuinfo"):
        if line.startswith("model name"):
            return line.split(":")[1].strip()

def main():
    try:
        address, channel = sys.argv[1:3]
    except ValueError:
        exit("Usage: main.py HOST[:PORT] CHANNEL [NICK]")

    try:
        nick = sys.argv[3]
    except IndexError:
        nick = make_nick()

    try:
        host, port = address.split(":", 1)
    except ValueError:
        host, port = address, 6667

    port = int(port)

    print(f"Connecting to {host}:{port} and joining {channel} as {nick}")

    HostBot(host, port, channel, nick).start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
