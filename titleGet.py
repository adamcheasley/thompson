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
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from urllib2 import URLError


class GetTitle:
    
    def listener(self, server_response, search_string):  
        if len(server_response) >= 4 and not 'QUIT' in server_response:            
            first = server_response[3]
            second = server_response[4:]
            if search_string == first[1:5]:
                return first[1:]
            for e in second:
                if search_string == e[0:4]:
                    return e

    def getTitle(self, uri):
        """this returns the string within the <title>
        of a given URI"""
        try:
            page = urlopen(uri)
        except URLError:
            return
	soup = BeautifulSoup(page)
	titleTag = soup.html.head.title.string
	return titleTag


if __name__ == '__main__':
    g = GetTitle()
    uri = 'http://www.someplacenice.co.uk'
    line = [':joey!~joey@82-45-8-208.cable.ubr04.aztw.blueyonder.co.uk', 
            'PRIVMSG', '#', ':that', uri, 'be', 'comfortable']
    line2 = [':joey!~joey@82-45-8-208.cable.ubr04.aztw.blueyonder.co.uk', 
            'PRIVMSG', '#', ':http://google.com']
    address = g.listener(line, 'http')
    address2 = g.listener(line2, 'http')
    print g.getTitle(address)
    print g.getTitle(address2)
