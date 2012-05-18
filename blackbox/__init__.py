# blackbox IRC macros
#
# (c) slowpoke (Proxy) < proxypoke at lavabit dot com >
# Offical IRC channel: irc://irc.datnode.net/hacking
# Offical repository on github: https://github.com/proxypoke/blackbox_IRC-macros
#
# This program, hereafter called "blackbox", 
# is Free Software under the terms of the 
# GNU General Public license, which can be found at 
# http://www.gnu.org/copyleft/gpl.html.

'''blackbox IRC macros - A python module to abstract the IRC protocol

A package of macros simplifying communication with an IRC server, encapsuling
most of the commonly used low level functions to handy, callable methods of an
IRC objects which contains the socket object. It's main intended usage is for
IRC bots, but it can of course be used for any other application intending to
interface with an IRC server.

This package directly exports the following classes:

   IRC -- universal IRC objects, minus operator only methods. 
   Oper -- same as above, but with said operator methods.
   Parser -- a simple, but complete IRC parser.
'''

from .core import IRCError

from .blackbox import \
        ( IRC
        , Oper
        )

from .parser import Parser
