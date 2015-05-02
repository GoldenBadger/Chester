"""Main module for Chester. Sets up an IRC bot according to the options
specified in config.ini.
"""

from ConfigParser import ConfigParser

from twisted.internet import reactor

from chester.bot import ChessBotFactory

if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")
    host = config.get("irc", "host")
    port = int(config.get("irc", "port"))
    nickname = config.get("irc", "nickname")
    realname = config.get("irc", "realname")
    channel = config.get("irc", "channel")
    
    reactor.connectTCP(host, port, ChessBotFactory(channel, nickname, realname))
    reactor.run()
