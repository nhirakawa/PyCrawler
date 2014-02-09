__author__ = 'Nick'

from urllib2 import *
from LinkParser import LinkParser
from argparse import *
from re import *

class PyCrawler():

    def __init__(self, seed, filetypes=['html'], wait=5):
        self.seed = str(seed)
        self.parser = LinkParser()
        self.regex = re.compile(build_regex(filetypes))
        self.wait = wait

    def crawl(self):
        seen = set([])
        def breadth_first(url):
            url = pad_url(url)
            if url in seen:
                return
            else:
                html = open_url(url)
                self.parser.feed(html)
                links = self.parser.get_links()
                print map(lambda s: url+'/'+s, links)
        breadth_first(self.seed)
        return seen

def open_url(url):
    request = urlopen(url)
    return ''.join(request.readlines())

def regex(file):
    match = re.search(".(pdf|html)$", file)
    if match:
        print file

def pad_url(url):
    if re.match('http://',url):
        return url
    else:
        return 'http://'+url

def build_regex(filetypes):
    s = r'.('
    for f in filetypes:
        s += f + '|'
    s = s[:-1]
    s += ')$'
    return s

def main():
    pc = PyCrawler('ciir.cs.umass.edu')
    pc.crawl()




main()