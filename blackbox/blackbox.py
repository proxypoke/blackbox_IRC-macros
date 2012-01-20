# blackbox IRC macros
#
# (c) 2011 Proxy of KOS-MOS Productions
# Offical IRC channel: irc://irc.datnode.net/KOS-MOS
# Offical repository on github: https://github.com/proxypoke/blackbox_IRC-macros
#
# This program, hereafter called "blackbox", 
# is Free Software under the terms of the 
# GNU General Public license, which can be found at 
# http://www.gnu.org/copyleft/gpl.html.

from . import blackbox_core
from .blackbox_core import IRCError

class IRC(blackbox_core.Core):
    '''A package of macros simplifying communication with an IRC server,
    encapsuling most of the commonly used low level functions to handy,
    callable functions.

    IRC class: This class implements composite methods and macros based
    on the basic methods contained in the Core class. 
    It does not contain commands only usable by IRC Operators, these are 
    contained in the Oper class.

    '''
    def __init__(self, **kwargs):
        '''Initializes the blackbox module. Pass on the keyword
        arguments. For documentation see Core's __init__.
        '''
        blackbox_core.Core.__init__(self, **kwargs)


    def voice(self, channel, nick):
        '''Gives voice to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "+v", nick)

    def devoice(self, channel, nick):
        '''Removes voice from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "-v", nick)

    def hop(self, channel, nick):
        '''Gives half operator status to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "+h", nick)

    def dehop(self, channel, nick):
        '''Removes half operator status from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "-h", nick)

    def op(self, channel, nick):
        '''Gives operator status to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "+o", nick)

    def deop(self, channel, nick):
        '''Removes operator status from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "-o", nick)

    def protect(self, channel, nick):
        '''Gives protected status to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "+a", nick)

    def deprotect(self, channel, nick):
        '''Removes protected status from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "-a", nick)

    def owner(self, channel, nick):
        '''Gives owner status to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "+q", nick)

    def deowner(self, channel, nick):
        '''Removes owner status from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            nick -- The targeted user.
        '''
        self.mode(channel, "-q", nick)

    def ban(self, channel, nick):
        '''Sets a ban on a channel against a nickname.

        This method will set a ban on nick!*@*.
        For more precise bans, use banByMask().

        Arguments:
            channel -- The channel on which to set the ban.
            nick -- The user to ban.
        '''
        self.mode(channel, "+b", nick + "!*@*")

    def unban(self, channel, nick):
        '''Removes a ban on a channel against a nickname.

        This method will unset bans on nick!*@*.
        For more precise unbanning, use unbanByMask().

        Arguments:
            channel -- The channel on which to remove the ban.
            nick -- The user to unban.
        '''
        self.mode(channel, "-b", nick + "!*@*")

    def banByMask(self, channel, mask):
        '''Sets a ban on a channel against a mask in the form of
        'nick!user@host'. Wildcards accepted.

        Arguments:
            channel -- The channel on which to set the ban.
            mask -- The mask to ban.
        '''
        self.mode(channel, "+b", mask)

    def unbanByMask(self, channel, mask):
        '''Removes a ban on a channel against a mask in the form of
        'nick!user@host'. Wildcards accepted.

        Arguments:
            channel -- The channel on which to remove the ban.
            mask -- The mask to unban.
        '''
        self.mode(channel, "-b", mask)


    def kickban(self, channel, nick, reason = ""):
        '''Sets a ban on a user, then kicks them from the channel.

        Arguments:
            channel -- The channel from which to kickban.
            nick -- The user to kickban.
            reason -- Optional. A reason for the kickban.
        '''
        self.ban(channel, nick)
        self.kick(channel, nick, reason)





###########################
#   ___  _ __   ___ _ __  #
#  / _ \| '_ \ / _ \ '__| #
# | (_) | |_) |  __/ |    #
#  \___/| .__/ \___|_|    #
#       |_|               #
###########################

class Oper(IRC, blackbox_core.OperCore):
    '''A package of macros simplifying communication with an IRC server,
    encapsuling most of the commonly used low level functions to handy,
    callable functions.
    '''
    
    def __init__(self, logging = False):
        '''Initializes the blackbox module. Pass on the keyword
        arguments. For documentation see Core's __init__.
        '''
        IRC.__init__(self, logging)
        blackbox_core.Core.__init__(self)

