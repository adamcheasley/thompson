import unittest
from thompson import IRC
from titleGet import GetTitle


class Tests(unittest.TestCase):
    """
    Contains all the tests.
    """

    def testHTTPListener(self):
        line = [':joey!~joey@82-45-8-208.cable.ubr04.aztw.blueyonder.co.uk', 
                'PRIVMSG', '#', ':that', 'hello', 'world', 'http://someplacenice.co.uk']
        t = GetTitle()
        uri = t.listenerHTTP(line, 'http')
        self.assertEqual(uri, 'http://someplacenice.co.uk')

    def testSimpleTitleParser(self):
        page = '<html>\n <head>\n <title>Hello World</title>\n </head>\n <body></body>\n </html>'
        p = GetTitle()
        title = p.simpleTitleParser(page)
        self.assertEqual(title, 'Hello World')


if __name__ == '__main__':
        unittest.main()
