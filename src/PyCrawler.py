__author__ = 'Nick'

from urllib import *
from urllib2 import *
from LinkParser import LinkParser
from argparse import *
from re import *
from robotparser import *
from urlparse import *
from time import sleep


class PyCrawler():

    def __init__(self, seed, domain='', filetypes=['html'], wait=1, limit=10):
        self.seed = str(seed)
        self.parser = LinkParser()
        self.file_regex = build_filetype_regex(filetypes)
        self.domain_regex = re.compile(domain)
        self.wait = wait
        self.robot_parser = RobotFileParser()
        self.limit = limit

    def crawl(self):
        seen = []
        frontier = [self.seed]
        while len(frontier) > 0 and len(seen) < self.limit:
            sleep(self.wait)
            url = frontier.pop(0)
            self.robot_parser.set_url(get_robots_url(url))
            if url not in seen and self.robot_parser.can_fetch('*', url):
                print 'crawling %s' % url
                html = read_html(url)
                self.parser.feed(html)
                links = self.parser.get_links()
                http_links = [resolve_relative_path(url, x) for x in links if self.file_regex.search(x)]
                for link in http_links:
                    if link not in frontier and self.domain_regex.search('link'):
                        frontier.append(link)
                seen.append(url)
        return seen


def read_html(url):
    request = Request(url)
    html = ''.join(urlopen(request).readlines())
    return html


def pad_url(url, host):
    if re.match("http://", url):
        return url
    else:
        return host + '/' + url


def get_robots_url(url):
    host = urlparse(url).netloc
    return 'http://' + host + '/robots.txt'


def resolve_relative_path(host, url):
    print 'url: %s' % url
    print 'host: %s' % host
    if re.match('../', url):
        if re.search('html$', host):
            print urljoin(host, url)
            return urljoin(host, url)
        else:
            result = urljoin(host+'/', url)
            print result
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
    pc = PyCrawler('http://ciir.cs.umass.edu/about', limit=30, wait=0)
    links = pc.crawl()
    print links


main()