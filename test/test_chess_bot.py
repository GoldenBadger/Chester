"""Test suites for chester.ChessBot and chester.ChessBotFactory."""

from twisted.test import proto_helpers
from twisted.trial import unittest

from chester import VERSION
from chester.bot import ChessBotFactory

class TestChessBot(unittest.SynchronousTestCase):
    """Test suite for chester.ChessBot."""
    
    _channel = "#testchannel"
    _nick = "chessbot"
    _other_nick = "tester"
    
    def setUp(self):
        """Set up the test suite."""
        factory = ChessBotFactory(
            self._channel,
            self._nick,
            "Chester")
        self.bot = factory.buildProtocol(("127.0.0.1", 0))
        self.fake_transport = proto_helpers.StringTransport()
        self.bot.makeConnection(self.fake_transport)
        self.bot.signedOn()
        self.bot.joined(self._channel)
        self.fake_transport.clear()
    
    def test_do_not_send_version(self):
        """If "version" is not PM'd to the bot, it should not reply at all."""
        
        self.bot.privmsg(self._other_nick, self._nick, "hi")
        self.assertEqual("", self.fake_transport.value())
    
    def test_do_send_version(self):
        """If "version is PM'd to the bot, it should reply with the current 
        version.
        """
        
        self.bot.privmsg(self._other_nick, self._nick, "version")
        self.assertEqual(
            "PRIVMSG {username} :{version}\r\n".format(
                username=self._other_nick, version=VERSION
            ),
            self.fake_transport.value())
