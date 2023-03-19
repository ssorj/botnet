#!/usr/bin/python

from irc.bot import SingleServerIRCBot

from psycopg_pool import ConnectionPool
import sys

database_password = "c66efc1638e111eca22300d861c8e364"
database_url = f"postgresql://postgres:{database_password}@localhost:5432/dvdrental"

class SqlBot(SingleServerIRCBot):
    def __init__(self, host, port, channel, nick):
        super().__init__([(host, port)], nick, nick)

        self.channel = channel
        self.nick = nick

        # XXX
        # async def configure(conn):
        #     await conn.set_autocommit(True)

        self.connection_pool = ConnectionPool(database_url)

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

                message = "\n".join([str(x) for x in rows])

            for line in message.split("\n"):
                conn.privmsg(self.channel, f"{event.source.nick}, {line}")

def main():
    try:
        address, channel = sys.argv[1:3]
    except ValueError:
        exit("Usage: sqlbot.py HOST[:PORT] CHANNEL [NICK]")

    try:
        nick = sys.argv[3]
    except IndexError:
        nick = "sqlbot"

    try:
        host, port = address.split(":", 1)
    except ValueError:
        host, port = address, 6667

    port = int(port)

    SqlBot(host, port, channel, nick).start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
