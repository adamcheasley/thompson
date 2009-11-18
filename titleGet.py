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
from BeautifulSoup import HTMLParseError
from urllib2 import urlopen
from urllib2 import URLError
from datetime import datetime


class GetTitle:
    
    def listenerHTTP(self, server_response, search_string):  
        if len(server_response) >= 4 and not 'QUIT' in server_response:            
            first = server_response[3]
            second = server_response[4:]
            if search_string == first[1:5]:
                return first[1:]
            for e in second:
                if search_string == e[0:4]:
                    return e

    def getPage(self, uri):
        """
        Attempt to grab the page
        """
        try:
            page = urlopen(uri)
        except URLError:
            print datetime.now()
            print 'Could not open URI'
            print 60 * '-'
            return
        else:
            print 'URI fetched'
            print uri
            return page

    def isImageURI(self, uri):
        """
        Find out whether the uri is pointing to an image
        """
        if uri[-3:] == 'jpg':
            return True
        elif uri[-3:] == 'png':
            return True
        
    def simpleTitleParser(self, page):
        """
        Takes a string from urllib and looks for the
        title tag. Returns the contents of that tag.
        """
        start_tag = page.find('<title>')
        end_tag = page.find('</title>')
        if start_tag > 0:
            content_start = start_tag + 7
            return page[content_start:end_tag]

    def getTitle(self, uri):
        """this returns the string within the <title>
        of a given URI"""
        if self.isImageURI(uri):
            print 'URI to an image'
            print 60 * '*'
            print 'Thompson will not try to parse images\n'
            return

        page1 = self.getPage(uri)
        if page1 == None:
            return

        try:
            soup = BeautifulSoup(page1)
        except HTMLParseError, TypeError:
            print 'Could not parse HTML with beautiful soup'
        except MemoryError:
            print 'Out of memory'
        else:
            print 'Parsed with beautiful soup'
            try:
                titleTag = soup.html.head.title.string
            except AttributeError:
                print 'HTML had no title'
                print 
                return
            if titleTag:
                try:
                    titleTag.encode('ascii')
                except UnicodeEncodeError:
                    print 'Title has an encoding error\n'
                    return
                print titleTag 
                print
                return titleTag.strip()

        page2 = self.getPage(uri)
        if page2 == None:
            return
        page_section = page2.read(1024)

        try:
            title_string = self.simpleTitleParser(page_section)
        except AttributeError:
            print 'Could not get simple title\n'
            return
        else:
            print 'title fetched using simple parser'
            print title_string + '\n'
            if title_string is not None:
                return title_string.strip()


