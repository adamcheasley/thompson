"""
    Thompson is an IRC bot that grabs the title tag when a URI is posted
    to a channel.
    Copyright (C) 2009  Adam Cheasley

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import sys
import socket
import string
import re
from titleGet import GetTitle
from datetime import datetime


s = socket.socket()

class Config:
    """
    Class for holding all the connection details
    """
    
    def __init__(self, host, port, nick, ident, name, channels):
        self.host = host
        self.port = port
        self.nick = nick
        self.ident = ident
        self.name = name
        self.channels = [channels]

class IRC:
    """
    main methods for dealing with the protocol and connection to the server
    """

    def ircConnect(self, config):
	"""
        This connects method to the server.
        Should pass in a config object.
        """
	s.connect((config.host, int(config.port)))
	s.send('NICK %s\r\n' % config.nick)
	s.send('USER %s %s bla :%s\r\n' % (config.ident, config.host, config.name))
	for ch in config.channels:
            s.send('JOIN %s\r\n' % ch)

    def serverResponse(self, temp_string):
        """
        Clean up the responses from the irc server and return a list of strings
        """
        for line in temp_string:
            line = string.rstrip(line)
            line = string.split(line)
            return line
        return

    def sendToChannel(self, channel, msg):
        """
        If the message isn't too long, send the string to the server
        """
        if msg:
            if len(msg) < 200:
                s.send('PRIVMSG %s :%s\r\n' % (channel, msg))
            else:
                print 'The title was too long'
                print

    def keepAlive(self, line):        
        """
        send ping to server
        """
        if(line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])

    def parseUser(self, server_string):
        """
        Gets the user nick from a server string.
        Expects the user string to be the first in a list
        """
        user = re.compile(':(.*)!').search(server_string[0]).group()
        return user[1:len(user)-1]

    def listener(self, server_response, word):
        """
        Listen for a particular word from the channel
        """
        if not server_response:
            return
        if len(server_response) >= 4 and not 'QUIT' in server_response:
            main_words = server_response[3:]
            # we need to remove the colon on the first word
            main_words[0] = main_words[0][1:]
            if word in main_words:
                return True


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print '\nYou need to pass in a server, channel and nick for Thompson'
        print 'Example: python thompson.py irc.xyxyx.org \# Thompson'
    else:
        c = Config(sys.argv[1], 6667, sys.argv[3], sys.argv[3], 'Just a bot', sys.argv[2])
        irc = IRC()
        listen = GetTitle()
        irc.ircConnect(c)
        read_buffer = ''
        print datetime.now()
        print 'Connected to server ' + sys.argv[1]
        print 60 * '-'
        print

        while True:
            #XXX I'd like this to be in a method or part of the 
            # server response method
            read_buffer = read_buffer + s.recv(500)
            temp = string.split(read_buffer, "\n")
            read_buffer = temp.pop( )

            response = irc.serverResponse(temp)
            if response:
                irc.keepAlive(response)
            uri = listen.listenerHTTP(response, 'http')
            if uri:
                title = listen.getTitle(uri)
                irc.sendToChannel(c.channels[0], title)
            
            user_hi = irc.listener(response, 'hello')
            if user_hi:
                user = irc.parseUser(response)
                thompson_say_hi = 'hey ' + user
                irc.sendToChannel(c.channels[0], thompson_say_hi)
