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

# ASCII banner created with http://www.network-science.de/ascii/


# blackbox IRC macros - Oper commands module

# (c) 2011 Proxy of KOS-MOS Productions
# Offical IRC channel: irc.datnode.net/#KOS-MOS
# Offical repository on github: https://github.com/proxypoke/blackbox_IRC-macros

# This program, hereafter called "blackbox", 
# is Free Software under the terms of the 
# GNU General Public license, which can be found at 
# http://www.gnu.org/copyleft/gpl.html.

# Version 0.2 (alpha)
# blackbox is still in active developement.

# Bugs:
#	None are currently known.

import blackbox

class IRC(blackbox.IRC):
	'''A package of macros simplifying communication with an IRC server,
	encapsuling most of the commonly used low level functions to handy,
	callable functions.

	This is the Oper version of blackbox. It contains commands only usable by
	IRC Operators in addition to all other commands defined in the regular
	blackbox. If the application you are writing does not have or need Oper
	access, consider using the regular version of blackbox instead.

	WARNING: ALL COMMANDS ARE UNTESTED. USE AT OWN RISK!

	RFC-Methods for Opers defined in this class:
		servconnect(targetserv, port [, remoteserv])
		die()
		kill(client, comment)
		oper(username, password)
		rehash()
		restart()
		service(nick, distribution, type_, info)
		squit(server, comment)
		wallops(message)
	'''
	def __init__(self, logging = False):
		'''Initializes the blackbox module. Pass on the logging parameter.

		Keyword Arguments:
			logging -- Optional. Turns on logging. Defaults to False.
		'''
		blackbox.IRC.__init__(self, logging)
		

	def servconnect(self, targetserv, port, remoteserv = ""):
		'''Requests the server to try to establish a new connection to another
		server. 

		Keyword Arguments:
			targetserv -- Server to connect to
			port -- Port on which to connect
			remoteserv -- Optional. Pass on the CONNECT request to the remote
				remote server instead
		'''
		if remoteserv == "":
			self.send("CONNECT {0} {1}".format(targetserv, port))
		else:
			self.send("CONNECT {0} {1} {2}".format(targetserv, port, remoteserv))


	def die(self):
		'''Shuts down the local server.
		'''
		self.send("DIE")


	def kill(self, user, reason):
		'''Terminates the connection of a client with the server network.

		Keyword Arguments:
			user -- The target of the KILL command
			reason -- The reason for the KILL.
		'''
		self.send("KILL {0} {1}".format(user, reason))


	def oper(self, username, password):
		'''Obtains Oper privileges.

		Keyword Arguments:
			username -- The username for the Oper privileges
			password -- The password for the username
		'''
		self.send("OPER {0} {1}".format(username, password))


	def rehash(self):
		'''Forces the local server to reprocess its configuration file.
		'''
		self.send("REHASH")


	def restart(self):
		'''Forces the local server to restart itself.'''
		'''
		'''
		self.send("RESTART")


	def service(self, nick, distribution, info):
		'''Registers a new service.

		Keyword Arguments:
			nick -- Name of the service
			distribution -- Visibility of the service
			info -- Description of the service
		'''
		self.send("SERVICE {0} * {1} 0 0 :{2}".format(nick, distribution, info))


	def squit(self, server, comment):
		'''Disconnects a server link.

		Keyword Arguments:
			server -- The target server (can be remote)
			comment -- A reason for this action.
		'''
		self.send("SQUIT {0} :{1}".format(server, comment))


	def wallops(self, message):
		'''Sends a message to all users with mode +w set.
		'''
		self.send("WALLOPS {0}".format(message))
