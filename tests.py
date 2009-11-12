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

    def testIsImageURI(self):
        uri = 'http://someplacenice.co.uk/images/me.jpg'
        uri2 = 'http://someplacenice.co.uk/images/me.png'
        uri3 = 'http://someplacenice.co.uk/index.php'
        t = GetTitle()
        self.assertEqual(t.isImageURI(uri), True)
        self.assertEqual(t.isImageURI(uri2), True)
        self.assertEqual(t.isImageURI(uri3), None)


if __name__ == '__main__':
        unittest.main()
