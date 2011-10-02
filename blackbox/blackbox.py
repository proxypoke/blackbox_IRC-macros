#       _   _______ _____       ___  ________ _____ 
#      | | / /  _  /  ___|      |  \/  |  _  /  ___|
#      | |/ /| | | \ `--. ______| .  . | | | \ `--. 
#      |    \| | | |`--. \______| |\/| | | | |`--. \
#      | |\  \ \_/ /\__/ /      | |  | \ \_/ /\__/ /
#      \_| \_/\___/\____/       \_|  |_/\___/\____/ 
#      ______              _            _   _                 
#      | ___ \            | |          | | (_)                
#      | |_/ / __ ___   __| |_   _  ___| |_ _  ___  _ __  ___ 
#      |  __/ '__/ _ \ / _` | | | |/ __| __| |/ _ \| '_ \/ __|
#      | |  | | | (_) | (_| | |_| | (__| |_| | (_) | | | \__ \
#      \_|  |_|  \___/ \__,_|\__,_|\___|\__|_|\___/|_| |_|___/

# blackbox IRC macros

# (c) 2011 Proxy of KOS-MOS Productions
# Offical IRC channel: irc://irc.datnode.net/KOS-MOS
# Offical repository on github: https://github.com/proxypoke/blackbox_IRC-macros

# This program, hereafter called "blackbox", 
# is Free Software under the terms of the 
# GNU General Public license, which can be found at 
# http://www.gnu.org/copyleft/gpl.html.

import blackbox_core

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


    def voice(self, channel, user):
        '''Give voice to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "+v", user)

    def devoice(self, channel, user):
        '''Remove voice from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "-v", user)

    def hop(self, channel, user):
        '''Give half operator status to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "+h", user)

    def dehop(self, channel, user):
        '''Remove half operator status from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "-h", user)

    def op(self, channel, user):
        '''Give operator status to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "+o", user)

    def deop(self, channel, user):
        '''Remove operator status from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "-o", user)

    def protect(self, channel, user):
        '''Give protected status to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "+a", user)

    def deprotect(self, channel, user):
        '''Remove protected status from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "-a", user)

    def owner(self, channel, user):
        '''Give owner status to someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "+q", user)

    def deowner(self, channel, user):
        '''Remove owner status from someone on a channel.

        Arguments:
            channel -- The channel on which to set the mode.
            user -- The targeted user.
        '''
        self.mode(channel, "-q", user)





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

