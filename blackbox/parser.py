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

from __future__ import unicode_literals
import time
import sys

class Event(object):
    '''
    '''
    def __init__(self, prefix, command, params):
        self.prefix = prefix
        self.command = command
        self.params = params
        self.time = time.time()

    def origin(self):
        '''Returns the origin of the Event, which is either a server
        name, or a nick.
        '''
        if '!' in self.prefix:
            o = self.prefix.split('!')[0]
        elif '@' in self.prefix:
            o = self.prefix.split('@')[0]
        else:
            o = self.prefix
        return o

    def user(self):
        '''Gets the user string of the origin, if any.
        '''
        if '!' in self.prefix:
            u = self.prefix.split('!')[-1]
            if '@' in u:
                u = u.split('@')[0]
        else:
            u = ''
        return u

    def host(self):
        '''Get the host of the origin, if any.
        '''
        if '@' in self.prefix:
            h = self.prefix.split('@')
        else:
            h = ''
        return h

    def __repr__(self):
        s = "{0} -- {1} from {2}: {3}"
        return s.format( time.asctime(time.gmtime(self.time))
                       , self.command
                       , self.prefix
                       , ' '.join(self.params)
                       )

class NumericReply(Event):
    '''
    '''
    def __init__(self, *args):
        super(NumericReply, self).__init__(*args)
        self.number = self.command

class Parser(object):
    '''
    '''
    _events = {}
    _numreplies = []

    def events(self):
        return list(self._events)
    
    def numreplies(self):
        return sorted(self._numreplies)

    def parse(self, string):
        '''
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
        params = []
        while len(s) != 0:
            if not s[0].startswith(':'):
                params.append(s.pop(0))
            else:
                params.append(' '.join(s)[1:])
                break
        return params

    def _generateEvent(self, prefix, command, params):
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
                event = type( command
                            , (Event,)
                            , {}
                            )
                self._events[command] = event
            return event( prefix
                        , command
                        , params
                        )
