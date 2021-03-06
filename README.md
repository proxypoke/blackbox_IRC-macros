# blackbox IRC Macros
## About

This python module - simply called blackbox from here on - is intended to
encapsulate most of the low level IRC protocol into handy, easily callable
methods of an IRC object that contains the socket object.  It is mainly meant
to be used in bots, but can of course be used for any other application
communicating with an IRC server as well.  

## License

Copyright (c) slowpoke (Proxy) < proxypoke at lavabit dot com>

Official IRC channel: [#hacking on DatNode][irc]

blackbox is Free Software under the terms of the 
[GNU General Public License v3][gpl].

This means, in short:
You have the freedom to use blackbox for any purpose, as well the freedom to
change and share it (including any changes you made) with or without
compensation.  You may not restrict these freedoms for any version of this
software including derivates, and you cannot add any other restriction beyond
those outlined in the terms of the GNU GPL v3.  

## Installation

There are multiple ways to install blackbox:

1. blackbox has a [PyPI entry][pypi], so you can simply install it using
	[easy_install][] or [pip][] (this is the recommended way):

		pip install blackbox
		easy_install blackbox

2. Download the source, and manually install it:

		python setup.py install

3. Download the source and place the package where you want to use it.

## Usage

Using blackbox is easy.  Assuming you have either installed it correctly or
have placed the package folder into the same folder than your code, you can
import the main module like this: 

	import blackbox

This module holds a class called IRC, which holds all of the main
functionality of blackbox.  You can create a simple IRC object without any
parameters: 

	irc = blackbox.IRC()

Now let's connect to a network and join a channel:

	irc.connect("irc.freenode.net", 6667)
	irc.nickname("YourNickName")
	irc.username("YourUserName", "YourRealName")
	irc.join("#YourChannel")

Of course we also need to receive data. That's what recv does. It also
handles PING replies for you!  

	data = irc.recv()

The data returned from recv are single lines from the server, ending (usually)
in '\\r\\n', but this might change depending on the IRCd the network you are
connecting to runs (though it shouldn't, it would mean the IRCd doesn't
correctly implement the IRC protocol).

## Documentation

For further insight into blackbox, use help(), all its methods are extensively
documented.  Also, many methods are very similar to slash-commands from
popular IRC clients such as XChat, irssi or weechat, so using them should come
natural to regular IRC users.

## Logging

blackbox uses the [logging][] module from the stdlib. It uses two loggers,
blackbox.in and blackbox.out, both of which log to INFO. Per default, they log
into a NullHandler, so if you want to enable logging, define a logger in your
application and set the level to INFO. You can then further define how and
where blackbox logs.

[irc]: irc://irc.datnode.net/hacking
[gpl]: http://www.gnu.org/licenses/gpl.html
[pypi]: http://pypi.python.org/pypi/blackbox/
[easy_install]: http://peak.telecommunity.com/DevCenter/EasyInstall 
[pip]: http://pypi.python.org/pypi/pip
[unreal]: http://www.unrealircd.com/
[logging]: http://docs.python.org/library/logging.html
