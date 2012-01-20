# blackbox IRC Macros
## About

This python module - simply called blackbox from here on - is intended to encapsulate most of the low level IRC protocol into handy, easily callable methods of an IRC object that contains the socket object.
It is mainly meant to be used in bots, but can of course be used for any other application communicating with an IRC server as well.


## License

Copyright (c) Proxy of KOS-MOS Productions 

Official IRC channel: [irc://irc.datnode.net/KOS-MOS](irc://irc.datnode.net/KOS-MOS)

blackbox is Free Software under the terms of the [GNU General Public License v3](http://www.gnu.org/licenses/gpl.html).

This means, in short:
You have the freedom to use blackbox for any purpose, as well the freedom to change and share it (including any changes you made) with or without compensation.
You may not restrict these freedoms for any version of this software including derivates, and you cannot add any other restriction beyond those outlined in the terms of the GNU GPL v3.

## Installation

Currently there is but one way to install blackbox:
download the source and run setup.py with the 'install' parameter (you might need adminstrative privileges).


A PyPI entry for blackbox is in the works.
Once that is done, you will be able to use [easy\_install](http://peak.telecommunity.com/DevCenter/EasyInstall) or [pip](http://pypi.python.org/pypi/pip) to install blackbox.

## Usage

Using blackbox is easy.
Assuming you have either installed it correctly or have placed the package folder into the same folder than your code, you can import the main module like this:

	from blackbox import blackbox

This module holds a class called IRC, which holds all of the main functionality of blackbox.
You can create a simple IRC object without any parameters:

	irc = blackbox.IRC()

Now let's connect to a network and join a channel:

	irc.connect("irc.freenode.net", 6667)
	irc.nickname("YourNickName")
	irc.username("YourUserName", "YourRealName")
	irc.join("#YourChannel")

Of course we also need to receive data.
That's what recv does.
It also handles PING replies for you!

	data = irc.recv()

Keep in mind when parsing data from recv() that it can be a long string that contains more than one line of IRC replies.
They are usually seperated by a '\\r\\n', but this can change depending on what IRCd the network you are connecting to runs.
blackbox is mainly tested on UnrealIRCd, which uses '\\r\\n', so please report any weird behavior or bugs you may encounter on other IRCds.

For further insight into blackbox, use help(), all its methods are extensively documented.
Also, many methods are very similar to slash-commands from popular IRC clients such as XChat.
