__author__ = 'Nick'

from urllib2 import *
from LinkParser import LinkParser

def main():
    parser = LinkParser()
    parser.feed('<a href="www.google.com">Data</a>')
    parser.feed('<a  href = "www.facebook.com"></a>')
    parser.close()
    for url in parser.get_links():
        open_url('http://' + url)

def crawl(seed):


def open_url(url):
    request = urlopen(url)
    print request.readlines()

main()