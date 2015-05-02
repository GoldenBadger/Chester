"""The part of Chester which acts as an IRC bot."""

from twisted.internet import protocol
from twisted.python import log
from twisted.words.protocols import irc

class ChessBotFactory(protocol.ClientFactory):
    """Set up the ChessBot IRC protocol."""
    
    protocol = ChessBot
    
    def __init__(self, channel, nickname, realname):
        """Initialise the bot factory with our settings."""
        
        self.channel = channel
        self.nickname = nickname
        self.realname = realname

class ChessBot(irc.IRCClient):
    """The actual IRC client for Chester."""
    
    def connectionMade(self):
        """Called when a connection is made."""
        
        self.nickname = self.factory.nickname
        self.realname = self.factory.realname
        irc.IRCClient.connectionMade(self)
        log.msg("Connection made.")
    
    def connectionLost(self, reason):
        """Called when a connection is lost."""
        
        irc.IRCClient.connectionLost(self, reason)
        log.msg("Connection lost: {!r}".format(reason))
    
    def signedOn(self):
        """Called when bot has successfully signed on to a channel."""
        
        log.msg("Signed on.")
        if self.nickname != self.factory.nickname:
            log.msg("Desired nickname taken. Actual nick: "
                    "\"{}\"".format(self.nickname))
        self.join(self.factory.channel)
    
    def joined(self, channel):
        """Called when the bot joins the channel."""
        
        log.msg("{nick} has joined {channel}"
                .format(nick=self.nickname, channel=self.factory.channel))
    
    def privmsg(self, user, channel, msg):
        """Called when the bot receives a message or a message is posted to a
        channel the bot is on.
        """
        
        sendTo = None
        senderNick = user.split("!", 1)[0]
        if channel = self.nickname and msg.startswith("version"):
            # If a private message starting with "version" is sent to the bot.
            sendTo = senderNick
        
        if sendTo:
            self.msg(sendTo, VERSION)
            log.msg("Sent version info to {receiver}.".format(receiver=sendTo))
