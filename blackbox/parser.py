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

'''blackbox.parser - a small, but complete IRC parser

This module provides a parser for IRC messages, which generates Event objects.
These can be queried for their origin and some other things, and further be
used to implement hooks etc.
'''

from __future__ import unicode_literals
import time
import sys

class Event(object):

    '''Represents a generic message from the IRC server. It has methods
    that work on every message an IRC server could return.
    The Parser subclasses this class on the fly to create events named
    after their command.
    '''

    def __init__(self, prefix, command, params):
        self.prefix = prefix
        self.command = command
        self.params = params
        self.time = time.time()

    def __str__(self):
        '''A formatted version of the message.
        '''
        s = "{0} -- {1} from {2}: {3}"
        return s.format( time.asctime(time.gmtime(self.time))
                       , self.command
                       , self.prefix
                       , ' '.join(self.params)
                       )

    def __repr__(self):
        '''The raw representation of the message.'''
        params = ' '.join(self.params)
        msg = ' '.join(
                [ self.prefix
                , self.command
                , params
                ])
        return msg

    def origin(self):
        '''Returns the origin of the Event, which is either a server
        name, or a nick.

        Returns:
            A string representing the server name or nick, or an empty
            string if there is no prefix.
        '''
        if '!' in self.prefix:
            origin = self.prefix.split('!')[0]
        elif '@' in self.prefix:
            origin = self.prefix.split('@')[0]
        else:
            origin = self.prefix
        return origin

    def user(self):
        '''Gets the username of the origin, if any.

        Returns:
            A string representing the username, or an empty string if
            there is none.
        '''
        if '!' in self.prefix:
            user = self.prefix.split('!')[-1]
            if '@' in user:
                user = user.split('@')[0]
        else:
            user = ''
        return user

    def host(self):
        '''Get the host of the origin, if any.

        Returns:
            A string representing the hostname, or an empty string if
            there is none.
        '''
        if '@' in self.prefix:
            host = self.prefix.split('@')[-1]
        else:
            host = ''
        return host


class NumericReply(Event):
    
    '''A special subclass of Event. It prevents the numerous numeric
    replies to be turned into single events each.
    '''

    def __init__(self, *args):
        super(NumericReply, self).__init__(*args)
        self.number = self.command


class Parser(object):

    '''Provides a very simple, but powerful, event-based parser for IRC
    messages. It creates Event objects on the fly, named after their
    command.
    '''

    _events = {}
    _numreplies = []

    def events(self):
        '''Gets a list of all known events.
        '''
        return list(self._events)
    
    def numreplies(self):
        '''Get a list of all known numeric replies.
        '''
        return sorted(self._numreplies)

    def parse(self, string):
        '''Parse a single IRC message string, and return an appropriate
        Event object.

        Arguments:
            string -- A valid IRC message string.

        Returns:
            An event object.
        '''
        prefix = ''
        command = ''
        params = ''

        s = string.split(' ')

        if s[0].startswith(':'):
            prefix = s.pop(0)

        command = s.pop(0)

        params = self._parseParams(s)
        
        return self._generateEvent(prefix, command, params)

    def _parseParams(self, s):
        '''Splits the parameters into a list.

        Every item will be a single string without whitespace, unless a
        colon is encountered. In that case, the last item will be a
        string possibly containing whitespace.
        '''
        params = []
        while len(s) != 0:
            if not s[0].startswith(':'):
                params.append(s.pop(0))
            else:
                params.append(' '.join(s)[1:])
                break
        return params

    def _generateEvent(self, prefix, command, params):
        '''Create an Event object, either using an already known Event,
        or generate a new subclass on the fly.
        '''
        if command.isdigit():
            if not command in self._numreplies:
                self._numreplies.append(command)
            return NumericReply( prefix
                               , command
                               , params
                               )
        else:
            if command in self._events:
                event = self._events[command]
            else:
                if sys.version_info[0] < 3:
                    command = command.encode("utf-8")
                # make a new subclass of Event, named like the command.
                event = type( command
                            , (Event,)
                            , {}
                            )
                self._events[command] = event
            return event( prefix
                        , command
                        , params
                        )
