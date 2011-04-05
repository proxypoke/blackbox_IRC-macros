# blackbox IRC Macros

## About

This python module - simply called blackbox from here on - is intended to encapsulate most of the low level IRC protocol into handy, easily callable methods of an IRC object that contains the socket object.
It is mainly meant to be used in bots, but can of course be used for any other application communicating with an IRC server as well.

## License

blackbox is Free Software under the terms of the GNU GPL 3.0.

## Implementation Status

The following RFC-defined commands have been implemented already:
* QUIT as quit()
* NICK as nickname()
* USER as username()
* JOIN as join() (currently does not support multiple join requests)
* PART as part()
* PRIVMSG as say() (regular message) and action() (emote)
* MODE as mode()
* KICK as kick()

For their respective keyword arguments refer to their docstrings.

# Branching

I'm trying out the branching model described [here](http://nvie.com/posts/a-successful-git-branching-model/). Although overkill for such a small, one-man project, I'd like to get used to this style of version control.

