#!/usr/bin/python

# pip install irc
# pip install psycopg psycopg_pool

from irc.bot import SingleServerIRCBot
from psycopg_pool import ConnectionPool

import sys

# import logging
# logging.basicConfig(level=logging.DEBUG)

database_password = "c66efc1638e111eca22300d861c8e364"
database_url = f"postgresql://postgres:{database_password}@sql-database:5432/dvdrental"

class SqlBot(SingleServerIRCBot):
    def __init__(self, host, port, channel, nick):
        super().__init__([(host, port)], nick, nick)

        self.nick = nick
        self.channel = channel

        # XXX
        # async def configure(conn):
        #     await conn.set_autocommit(True)

        self.connection_pool = ConnectionPool(database_url)

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

        response_lines = self.send_query(text)

        for line in response_lines:
            conn.privmsg(self.channel, f"{event.source.nick}: {line}")

    def send_query(self, text):
        rows = []

        with self.connection_pool.connection() as dbconn:
            try:
                cursor = dbconn.execute(text)
            except Exception as e:
                message = str(e)
            else:
                rows = [list()]

                for description in cursor.description:
                    rows[0].append(description[0])

                for row in cursor.fetchall():
                    rows.append(row)

        return rows

def main():
    try:
        address, channel = sys.argv[1:3]
    except ValueError:
        exit("Usage: main.py HOST[:PORT] CHANNEL [NICK]")

    try:
        nick = sys.argv[3]
    except IndexError:
        nick = "sqlbot"

    try:
        host, port = address.split(":", 1)
    except ValueError:
        host, port = address, 6667

    port = int(port)

    print(f"Connecting to {host}:{port} and joining {channel} as {nick}")

    SqlBot(host, port, channel, nick).start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
