__author__ = 'Nick'

from urllib import *
from urllib2 import *
from LinkParser import LinkParser
from argparse import *
from re import *
from robotparser import *
from urlparse import *


class PyCrawler():

    def __init__(self, seed, filetypes=['html'], wait=5000, limit=10):
        self.seed = str(seed)
        self.parser = LinkParser()
        self.regex = build_filetype_regex(filetypes)
        self.wait = wait
        self.robot_parser = RobotFileParser()
        self.limit = limit

    def crawl(self):
        seen = []
        print 'seen: %s' % seen
        print type(seen)
        frontier = [self.seed]
        while len(frontier) > 0 and seen.__len__() < self.limit:
            url = frontier.pop(0)
            self.robot_parser.set_url(url)
            if url not in seen and self.robot_parser.can_fetch('*', url):
                print 'crawling %s' % url
                host, html = read_html(url)
                self.parser.feed(html)
                links = self.parser.get_links()
                http_links = [resolve_relative_path(url, x) for x in links if self.regex.search(x)]
                print http_links
                for link in http_links:
                    if link not in frontier:
                        frontier.append(link)
                seen.append(url)
        print 'seen: %s' % seen
        return seen


def read_html(url):
    request = Request(url)
    html = ''.join(urlopen(request).readlines())
    host = request.get_host()
    return host, html


def pad_url(url, host):
    if re.match("http://", url):
        return url
    else:
        return host + '/' + url


def get_robots_url(url):
    host = urlparse(url).netloc
    return host + '/robots.txt'


def resolve_relative_path(host, url):
    print 'url: %s' % url
    print 'host: %s' % host
    if re.match('../', url):
        result = urljoin(host, url[2:])
        return result
    if not re.search('html$', host):
        host += '/'
    result = urljoin(host, url)
    print result
    return result


def build_filetype_regex(filetypes):
    s = r'.('
    for f in filetypes:
        s += f + '|'
    s = s[:-1]
    s += ')$'
    return re.compile(s)


def main():
    pc = PyCrawler('http://ciir.cs.umass.edu/about')
    links = pc.crawl()
    print links
    print links.__len__()




main()