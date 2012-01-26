# blackbox IRC macros

# (c) 2011 Proxy of KOS-MOS Productions
# Offical IRC channel: irc://irc.datnode.net/KOS-MOS
# Offical repository on github: https://github.com/proxypoke/blackbox_IRC-macros

# This program, hereafter called 'blackbox', 
# is Free Software under the terms of the 
# GNU General Public license, which can be found at 
# http://www.gnu.org/copyleft/gpl.html.

from distutils.core import setup

setup   ( name = 'blackbox'
        , version = '0.5'
        , author = 'slowpoke (Proxy)'
        , author_email = 'proxypoke@lavabit.com'
        , url = 'https://github.com/proxypoke/blackbox_IRC-macros'
        , description = 'A Python module to abstract and encapsulate the IRC protocol'
        , packages = ['blackbox']
        , classifiers = [ 'Programming Language :: Python :: 2'
                        , 'Programming Language :: Python :: 3'
                        , 'License :: OSI Approved :: GNU General Public License (GPL)'
                        , 'Intended Audience :: Developers'
                        , 'Operating System :: OS Independent'
                        , 'Development Status :: 4 - Beta'
                        , 'Topic :: Communications :: Chat :: Internet Relay Chat'
                        , 'Topic :: Software Development :: Libraries :: Python Modules'
                        ]
        , long_description = '''
This python module - simply called blackbox from here on - is intended to  
encapsulate most of the low level IRC protocol into handy, easily callable 
methods of an IRC object that contains the socket object.
It is mainly meant to be used in bots, but can of course be used for any 
other application communicating with an IRC server as well.
'''
        )
