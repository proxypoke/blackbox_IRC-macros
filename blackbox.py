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
# Contact or ask for me on the IRC of irc.datnode.net

# This program, hereafter called "blackbox", 
# is Free Software under the terms of the 
# GNU General Public license, which can be found at 
# http://www.gnu.org/copyleft/gpl.html.

# Version 0.1
# blackbox is still in active developement.

# Bugs:
#	None are currently known.

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


class IRC(object):
	'''A package of macros simplifying communication with an IRC server,
	encapsuling most of the commonly used low level functions to handy,
	callable functions.

	Attributes defined in this class:
		irc -- the socket.socket object
		socketOpen -- indicates the state of the socket (True = open)
		isConnected -- indicates the state of the connection (True = connected)
		logging -- indicates whether a log is maintained or not (True = active)
		logfile -- the file to which the log is written
		data -- stores the data received from the last call of recv()

	Non-RFC-Methods defined in this class:
		__init__([logging])
		logWrite(data)
		close()
		connect(host, port)
		send(data)
		recv([bufferlen])

	RFC-Methods defined in this class:
		quit([quitmsg])
		nickname(nick)
		username(user, real)
		join(channel [, keyword])
		part(channel [,partmsg])
		say(target, msg)
		action(target, msg)
		mode(channel, mode [, users])
		kick(channel, user [, reason])
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
		self.logfile.write("{0} -- {1}\n".format(currentTime, data))


	def close(self):
		'''Close the socket, set socketOpen to False. 
		Also close the log file if logging was active.'''
		if self.socketOpen:
			self.irc.close()
			self.socketOpen = False
		if self.logging:
			self.logfile.close()


	def connect(self, host, port):
		'''Connect to a network with the given adress on the given port.

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
		'''Send raw data to the IRC server, adding the trailing \\r\\n.

		Keyword Arguments:
			data -- a string describing a command to the server
		'''
		if not self.isConnected:
			raise IRCError("No active connection.")

		# convert to string
		data = str(data)

		# send data and add the trailing carriage return
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
			self.logWrite(data)

		# answer to pings
		if "PING" in data:
			self.send("PONG " + data[1])

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


	def join(self, channel, keyword = ""):
		'''Try to join a channel.

		Keyword Arguments:
			channel -- the target channel
			keyword -- Optional. For channels with mode +k.
		'''
		# convert to string
		channel = str(channel)

		# stop execution if the channel is an empty string
		if len(channel) == 0:
			return

		# add the hash if it is missing
		if channel[0] != '#':
			channel = '#' + channel

		# send join request to server
		self.send("JOIN {0} {1}".format(channel, keyword))


	def part(self, channel, partmsg = ""):
		'''Part a channel. Optionally send a part message.

		Keyword Arguments:
			channel -- the target channel
			partmsg -- Optional. A part message sent along the PART command.
		'''
		#convert to string
		channel = str(channel)

		# stop execution if the channel is an empty string
		if len(channel) == 0:
			return

		# add the hash if it is missing
		if channel[0] != '#':
			channel = '#' + channel

		# no part message given
		if partmsg == "":
			self.send("PART {0}".format(channel))
		else:
			self.send("PART {0} :{1}".format(channel, partmsg))


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


	def mode(self, channel, mode, users = ""):
		'''Set the mode(s) of a channel or (a) user(s) on a channel.
		Usually requires privileges in that channel.

		Keyword Arguments:
			channel -- the target channel
			mode -- one or more valid mode characters
			users -- Optional. One or more users separated by spaces.
		'''
		if users == "":
			self.send("MODE {0} {1}".format(channel, mode))
		else:
			self.send("MODE {0} {1} {2}".format(channel, mode, users))


	def kick(self, channel, user, reason = ""):
		'''Kick a user from a channel. 
		Usually requires privileges in that channel.

		Keyword Arguments:
			channel -- the target channel
			user -- the target user
			reason -- Optional. Specify a reason for the kick.'''
		if reason == "":
			self.send("KICK {0} {1}".format(channel, user))
		else:
			self.send("KICK {0} {1} :{2}".format(channel, user, reason))

