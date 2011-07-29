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

import socket
import time

class IRCError(Exception):
	'''Exception for connection related errors.

	Attributes:
		msg -- a message describing the error.
	'''

	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return repr(self.msg)


class Core(object):
	'''A package of macros simplifying communication with an IRC server,
	encapsuling most of the commonly used low level functions to handy,
	callable functions.

	Core class: This class implements all basic server commands as defined
	in the IRC RFC. It does not contain commands only usable by IRC
	Operators, these are contained in the OperCore class.

	Attributes defined in this class:
		irc -- the socket.socket object
		socketOpen -- indicates the state of the socket (True = open)
		isConnected -- indicates the state of the connection (True = connected)
		logging -- indicates whether a log is maintained or not (True = active)
		logfile -- the file to which the log is written
		data -- stores the data received from the last call of recv()

	Regular Methods defined in this class:
		__init__([logging])
		logWrite(data)
		close()
		connect(host, port)
		send(data)
		recv([bufferlen])

	Methods implementing RFC commands defined in this class:
		quit([quitmsg])
		nickname(nick)
		username(user, real)
		join(channel [, keyword])
		part(channel [,partmsg])
		say(target, msg)
		action(target, msg)
		mode(channel, mode [, users])
		kick(channel, user [, reason])
		away(message)
		invite(nickname, channel)
		notice(target, message)
		serverpassword(password)
		settopic(channel, topic)
		admin([server])
		info([server]
		ison(nicknames)
		links([servmask [, server]])
		chanlist([channels [, server]])
		lusers([mask [, server]])
		names([channels [, server]])
		servlist([mask [, type_]])
		stats(query [, server])
		time([server])
		gettopic(channel)
		trace([target])
		userhost(nicknames)
		users([server])
		version([server])
		who(mask [, oponly])
		whois(nickname [, server])
		whowas(nickname [, count [, server]])
	'''

	def __init__(self, logging = False):
		'''Initialize the object, create the socket, set the attributes to
		their default values. Create a log file if logging is set to True.

		Keyword Arguments:
			logging -- Optional. Turns on logging. Defaults to False.
		'''
		# create the socket
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socketOpen = True

		self.isConnected = False

		# storage for received data
		self.data = None

		# create a dated log file if logging is turned on
		self.logging = logging
		if self.logging:
			# replace spaces with underscore
			currentTime = time.asctime().replace(" ", "_")
			# replace colons with hyphen
			currentTime = currentTime.replace(":", "-")
			# create logfile
			try:
				self.logfile = open("blackbox_log_{0}.txt".format(currentTime), "w")
			except IOError:
				print "An error occured while trying to create the logfile."
				while True:
					input_ = raw_input("Continue without logging? (y/n)\n>",)
					if input_ not in ["y", "n"]:
						print "Invalid input. Please enter 'y' or 'n'."
						continue
					
					elif input_ == "y":
						self.logging = False
						self.logfile = None
						break
					else:
						print "Aborting..."
						quit()
		else:
			self.logfile = None
			

	def logWrite(self, data):
		'''Write to the log file.

		Keyword Arguments:
			data -- the data to write into the file.
		'''
		# abort if the function was called without a file object present
		if self.logfile == None:
			raise IOError("No log file present.")
		# get current local time hh:mm:ss
		getTime = time.localtime()[3:6]
		currentTime = []
		
		# convert tuple contents into strings
		for t in getTime:
			currentTime.append(str(t))

		currentTime = ":".join(currentTime)

		# write to log
		self.logfile.write("{0} {1}\n".format(currentTime, data))


	def close(self):
		'''Close the socket, set socketOpen to False. 
		Also close the log file if logging was active.'''
		if self.socketOpen:
			self.irc.close()
			self.socketOpen = False
		if self.logging:
			self.logfile.close()


	def connect(self, host, port):
		'''Connect to a network with the given adress on the given port. Will do
		nothing when self.isConnected is True.

		Keyword Arguments:
			host -- the network's adress, either a DNS entry or an IP
			port -- the port on which the connection will run
		'''
		if not self.socketOpen:
			raise socket.error("The socket is closed.")
		# do nothing if a connection is already established
		if self.isConnected:
			return

		# convert types and abort on error
		host = str(host)
		try:
			port = int(port)
		except ValueError:
			raise TypeError("'port' parameter expects an integer. Got '{0}', which is {1}.".format(port, type(port)))

		# initiate the connection
		self.irc.connect((host, port))
		self.isConnected = True

		
	def send(self, data):
		'''Send raw data to the IRC server, adding the trailing CRNL.

		Keyword Arguments:
			data -- a string describing a command to the server
		'''
		if not self.isConnected:
			raise IRCError("No active connection.")

		data = str(data)

		if self.logging:
			self.logWrite("<-- " + data)

		# send data and add the trailing CRNL
		self.irc.send(data + "\r\n")


	def recv(self, bufferlen = 4096):
		'''Listen to data from the server, PONG if the server PINGs.
		Return the received data.

		Keyword Arguments:
			bufferlen -- Optional. Changes the size of the buffer. Defaults to 4096.
		'''
		if not self.isConnected:
			raise IRCError("No active connection.")

		data = self.irc.recv(bufferlen)

		# strip \r\n
		data = data.strip("\r")
		data = data.strip("\n")

		# write to log if logging is active
		if self.logging:
			self.logWrite("--> " + data)

		# answer to pings
		if "PING" in data:
			self.send("PONG " + data.split()[1])

		# save to internal storage and return received data
		self.data = data
		return data


	def quit(self, quitmsg = ""):
		'''Quit the server. Optionally send a quit message.

		Keyword Arguments:
			quitmsg -- Optional. A quit message sent along the QUIT command.'''
		if quitmsg == "":
			self.send("QUIT")
		else:
			self.send("QUIT :{0}".format(quitmsg))

		# set self.isConnected to False
		self.isConnected = False


	def nickname(self, nick):
		'''Set or change the nickname.

		Keyword Arguments:
			nick -- a valid nickname (no spaces, special characters restricted)
		'''
		self.send("NICK {0}".format(nick))


	def username(self, user, real=None):
		'''Set the user- and realname.

		Keyword Arguments:
			user -- a valid username (no spaces, special characters restricted)
			real -- Optional. A real name or description (spaces allowed).
					Defaults to the value of the user argument.
		'''
		if real == None:
			real = user
		self.send("USER {0} {0} {0} :{1}.".format(user, real))


	def join(self, channels, keywords = ""):
		'''Try to join a number of channels, with optional keywords.

		Keyword Arguments:
			channels -- the target channels, separated by ','
			keywords -- Optional. For channels with mode +k, separated by ','
		
		Note: When joining multiple channels with and without mode +k, either
		put the channels with +k first so their keywords get assigned correctly,
		or replace empty keywords with '*'. The first method is advised.
		'''
		channels = str(channels)
		# stop execution if the channel is an empty string
		if len(channels) == 0:
			return

		# split the channels string at every comma
		split = channels.split(',')

		# add the hash for every channel if it is missing
		channels = ""
		for channel in split:
			if channel != "":
				if channel[0] != '#':
					channel = '#' + channel + ','
					channels += channel
				else:
					channels += channel

		# send join request to server
		if keywords == "":
			self.send("JOIN {0}".format(channels))
		else:
			self.send("JOIN {0} {1}".format(channels, keywords))


	def part(self, channels, partmsg = ""):
		'''Part one or more channels. Optionally send a part message.

		Keyword Arguments:
			channel -- the target channels, separated by ','
			partmsg -- Optional. A part message sent along with the PART command
		'''
		channels = str(channels)

		# stop execution if the channel is an empty string
		if len(channels) == 0:
			return

		# split the channels string at every comma
		split = channels.split(',')

		# add the hash for every channel if it is missing
		channels = ""
		for channel in split:
			if channel != "":
				if channel[0] != '#':
					channel = '#' + channel + ','
					channels += channel
				else:
					channels += channel

		# no part message given
		if partmsg == "":
			self.send("PART {0}".format(channels))
		else:
			self.send("PART {0} :{1}".format(channels, partmsg))


	def say(self, target, msg):
		'''Send a message to a user or channel.

		Keyword Arguments:
			target -- either another user or channel (with the usual hash)
			msg -- the message to send
		'''
		self.send("PRIVMSG {0} :{1}".format(target, msg))


	def action(self, target, msg):
		''''Do' an action in third person in a private message or channel.
			Has the same effect as '/me' in many clients.

		Keyword Arguments:
			target - either a user or channel (with the usual hash)
			msg - an action to 'do'. 
		'''
		self.send("PRIVMSG {0} :\x01ACTION {1}\x01".format(target, msg))


	def mode(self, target, mode, args = ""):
		'''Set the mode(s) of a channel or user, with optional arguments.

		Keyword Arguments:
			target -- the target channel or user
			mode -- one or more valid mode characters
			args -- Optional. One or more arguments (eg usernames).
		'''
		if args == "":
			self.send("MODE {0} {1}".format(target, mode))
		else:
			self.send("MODE {0} {1} {2}".format(target, mode, args))


	def kick(self, channel, user, reason = ""):
		'''Kick a user from a channel. 
		Usually requires privileges in that channel.

		Keyword Arguments:
			channel -- the target channel
			user -- the target user
			reason -- Optional. Specify a reason for the kick.
		'''
		if reason == "":
			self.send("KICK {0} {1}".format(channel, user))
		else:
			self.send("KICK {0} {1} :{2}".format(channel, user, reason))


	def away(self, message = ""):
		'''Mark yourself as away, specifying a message to be sent to others. If 
		message is omitted, the away status will be removed.

		Keyword Arguments:
			message -- Message to be sent. Must be omitted to unmark
		'''
		if message == "":
			self.send("AWAY")
		else:
			self.send("AWAY {0}".format(message))


	def invite(self, user, channel):
		'''Invite a user to a channel.

		Keyword Arguments;
			user -- The user to invite
			channel -- The channel to invite to
		'''
		self.send("INVITE {0} {1}".format(user, channel))


	def notice(self, target, message):
		'''Send a notice to a user or channel.

		Keyword Arguments:
			target -- Either a user or a channel (prefixed with the usual hash)
			message -- The message to send
		'''
		self.send("NOTICE {0}, {1}".format(target, message))


	def serverpassword(self, password):
		'''Sends the server password (if required).

		Keyword Arguments:
			password -- The server password.
		'''
		self.send("PASS {0}".format(password))


	def squery(self, servicename = "", message = ""):
		'''Not implemented.
		'''
		return NotImplemented


	def summon(self, user = "", server = "", channel = ""):
		'''Not implemented.
		'''
		return NotImplemented

	def settopic(self, channel, topic):
		'''Set the topic of a channel.
		Note: To query for the topic use gettopic().

		Keyword Arguments:
			channel -- The channel to set the topic for
			topic -- The text to set as the topic
		'''
		channel = str(channel)

		# stop execution if the channel is an empty string
		if len(channel) == 0:
			return

		# add the hash if it is missing
		if channel[0] != '#':
			channel = '#' + channel

		# Set the topic
		self.send("TOPIC {0} {1}".format(channel, topic))


	def admin(self, target = ""):
		'''Requests information about the administrator of the local server, or,
		if target is specified, the server of the target (wildcards accepted).

		Keyword Arguments:
			target -- Optional. Forward the request to the server of target
				(can be a client or a server)
		'''
		if target == "":
			self.send("ADMIN")
		else:
			self.send("ADMIN {0}".format(target))


	def info(self, target = ""):
		'''Requests information about the local server, or, if target is
		specified, the server of the target (wildcards accepted).

		Keyword Arguments:
			target -- Optional. Forward the request to the server of target
				(can be a client or a server)
		'''
		if target == "":
			self.send("INFO")
		else:
			self.send("INFO {0}".format(target))


	def ison(self, nicknames):
		'''Requests information about the online status of one or more 
		nicknames. The server returns all nicknames that are currently online.

		Keyword Arguments:
			nicknames -- Either a space separated string of nicknames, or a 
				python list of strings.
		'''
		# check type of kwarg
		if type(nicknames) == str:
			pass
		if type(nicknames) == list:
			nicknames = " ".join(nicknames)

		self.send("ISON {0}".format(nicknames))


	def links(self, servmask = "", server = ""):
		'''Queries the specified server, or, if omitted, the local server,
		for a list of known servers matching servmask. If servmask is omitted,
		all known servers are returned.

		Keyword Arguments:
			servmask -- Optional. Only servers matching servmask will be 
				returned. Accepts wildcards.
			server -- Optional. Queries the specified server instead of the 
				local server.
		'''
		if servmask == "" and server == "":
			self.send("LINKS")
		elif server == "":
			self.send("LINKS {0}".format(servmask))
		else:
			self.send("LINKS {1} {0}".format(servmask, server))


	def chanlist(self, channels = "", server = ""):
		'''Queries for a list of channels and their topics. If channels is 
		specified, lists only the status of those channels. If server is 
		specified, forwards the request to that server.

		Keyword Arguments:
			channels - Optional. Requests only the listed channels, separated
				by ','
			server -- Optional. Forwards the request to the specified server.
				Accepts wildcards.
		'''
		channels = str(channels)


		# split the channels string at every comma
		split = channels.split(',')

		# add the hash for every channel if it is missing
		channels = ""
		for channel in split:
			if channel != "":
				if channel[0] != '#':
					channel = '#' + channel + ','
					channels += channel
				else:
					channels += channel

		# Send the request
		if server == "":
			self.send("LIST {0}".format(channels))
		else:
			self.send("LIST {0} {1}".format(channels, server))

	def lusers(self, mask = "", server = ""):
		'''Gets statistics about the size of the IRC network. Without mask, the
		reply will be about the whole network, else about the parts that match
		mask. If server is omitted, the local server will be queried, else the
		query will be forwarded to server.

		Keyword Arguments:
			mask -- Optional. Narrows down the query, matching mask.
			server -- Optional. Forwards the query to server.
		'''
		if mask == "" and server == "":
			self.send("LUSERS")
		elif server == "":
			self.send("LUSERS {0}".format(mask))
		else:
			self.send("LUSERS {0} {1}".format(mask, server))


	def names(self, channels = "", server = ""):
		'''Queries for a list of nicknames sorted by channel that are visible to
		the client. If channels is specified, only lists for those channels are
		returned. If server is given, the request is forwarded to that server.

		Keyword Arguments:
			channels - Optional. A list of channels separated by ','
			server -- Optional. Forwards the request to a server. Wildcards
				accepted.
		'''
		channels = str(channels)
		# stop execution if the channel is an empty string

		# split the channels string at every comma
		split = channels.split(',')

		# add the hash for every channel if it is missing
		channels = ""
		for channel in split:
			if channel != "":
				if channel[0] != '#':
					channel = '#' + channel + ','
					channels += channel
				else:
					channels += channel

		# send the request
		if channels == "" and server == "":
			self.send("NAMES")
		elif server == "":
			self.send("NAMES {0}".format(channels))
		else:
			self.send("NAMES {0} {1}".format(channels, server))


	def servlist(self, mask = "", type_ = ""):
		'''Lists services connected to the network and visible to the user, 
		matching mask if specified and of the matching type if specified.

		Keyword Arguments:
			mask -- Optional. Narrows down the matches. Wildcards accepted.
			type_ -- Optional. Only services matching type_ will be returned.
		'''
		if mask == "" and type_ == "":
			self.send("SERVLIST")
		elif type_ == "":
			self.send("SERVLIST {0}".format(mask))
		else:
			self.send("SERVLIST {0} {1}".format(mask, type_))


	def stats(self, query, server = ""):
		'''Queries for certain server statistics. If note specified otherwise by
		the server argument, the local server is queried.

		Keyword Arguments:
			query -- A letter describing the query. Mostly implementation 
				dependant. The following SHOULD be supported by all servers:
					l -- a list of the server's connections, their length and 
						bandwidth usage
					m -- usage count of all commands supported by the server
					o -- a list of privileged users, operators
					u -- server uptime
			server -- Optional. Forwards the request to a server. Wildcards
				accepted.
		'''
		if server == "":
			self.send("STATS {0}".format(query))
		else:
			self.send("STATS {0} {1}".format(query, server))


	def time(self, server = ""):
		'''Queries the local time of the local server, or a remote server if 
		specified.

		Keyword Arguments:
			server -- Optional. Forwards the request to a server. Wildcards
				accepted.
		'''
		if server == "":
			self.send("TIME")
		else:
			self.send("TIME {0}".format(server))


	def gettopic(self, channel):
		'''Queries for the topic of a channel.
		Note: To set the topic of a channel use settopic().

		Keyword Arguments:
			channel -- The channel for which the topic is queried
		'''
		self.send("TOPIC {0}".format(channel))


	def trace(self, server = ""):
		'''Traces a route to the local or a remote server, if specified.

		Keyword Arguments:
			server --  Optional. Forwards the request to a server. Wildcards
				accepted.
		'''
		if server == "":
			self.send("TRACE")
		else:
			self.send("TRACE {0}".format(server))


	def userhost(self, nicknames):
		'''Queries for host information about the given nicknames.

		Keyword Arguments:
			nicknames -- A space separated string of nicknames or a python list
				of strings.
		'''
		# check the kwarg for type, replace if necessary
		if type(nicknames) == str:
			pass
		elif type(nicknames) == list:
			nicknames = " ".join(nicknames)

		self.send("USERHOST {0}".format(nicknames))

	def users(self, server = ""):
		'''Queries for a list of users logged into the server.
		Note: Disabled on most servers for security reasons.

		Keyword Arguments:
			server --  Optional. Forwards the request to a server. Wildcards
				accepted.
		'''
		if server == "":
			self.send("USERS")
		else:
			self.send("USERS {0}".format(server))


	def version(self, server = ""):
		'''Queries for the version of the server program.

			server --  Optional. Forwards the request to a server. Wildcards
				accepted.
		'''
		if server == "":
			self.send("VERSION")
		else:
			self.send("VERSION {0}".format(server))


	def who(self, mask = "", oponly = False):
		'''Queries for a list of information about all users matching mask, or, if
		mask is omitted, all users who aren't invisible (mode +i). If oponly is
		True, only operators matching mask will be listed.

		Keyword Arguments:
			mask -- Optional. Narrows down the query. Wildcards accepted.
			oponly -- Optional. List only Operators. Defaults to False.
		'''
		if mask == "" and not oponly:
			self.send("WHO")
		elif not oponly:
			self.send("WHO {0}".format(mask))
		else:
			self.send("WHO {0} o".format(mask))


	def whois(self, nickname, server = ""):
		'''Queries for information about a specific user.

		Keyword Arguments:
			nickname -- The nickname to query.
			server -- Optional. Forwards the request to a server. Wildcards
				accepted.
		'''
		if server == "":
			self.send("WHOIS {0}".format(nickname))
		else:
			self.send("WHOIS {1} {0}".format(nickname, server))


	def whowas(self, nickname, count = "", server = ""):
		'''Queries for information about a nickname that no longer exists.

		Keyword Arguments:
			nickname -- The nickname to query
			count -- Optional. Limits the maximum amount of entries that are
				returned, if any.
			server -- Optional. Forwards the request to a server. Wildcards
				accepted.
		'''
		if count == "" and server == "":
			self.send("WHOWAS {0}".format(nickname))
		elif server == "":
			self.send("WHOWAS {0} {1}".format(nickname, count))
		else:
			self.send("WHOWAS {0} {1} {2}".format(nickname, count, server))




###########################
#   ___  _ __   ___ _ __  #
#  / _ \| '_ \ / _ \ '__| #
# | (_) | |_) |  __/ |    #
#  \___/| .__/ \___|_|    #
#       |_|               #
###########################


class OperCore(Core):
	'''A package of macros simplifying communication with an IRC server,
	encapsuling most of the commonly used low level functions to handy,
	callable functions.

	OperCore class: This class implements all basic server commands as 
	defined in the IRC RFC, including the commands reserved for IRC
	Operators. If your application does not have or need these
	privileges, consider using the Core class instead.

	WARNING: ALL COMMANDS ARE UNTESTED. USE AT OWN RISK!

	Methods implementing RFC commands for Opers defined in this class:
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
		Core.__init__(self, logging)
		

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
