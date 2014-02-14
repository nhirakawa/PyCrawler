__author__ = 'Nick'

from HTMLParser import HTMLParser

class LinkParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def feed(self, data):
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if 'href' in attr:
                self.links.append(attr[1])

    def get_links(self):
        result = self.links
        self.links = []
        return result
