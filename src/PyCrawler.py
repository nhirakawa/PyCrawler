__author__ = 'Nick'

from urllib2 import *
from re import *
from robotparser import *
from urlparse import *
from time import sleep
from HTMLParser import HTMLParser
from argparse import ArgumentParser


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


class PyCrawler():
	def __init__(self, seed, domain='', filetypes=[''], wait=1, limit=10):
		self.seed = str(seed)
		self.parser = LinkParser()
		self.file_regex = build_filetype_regex(filetypes)
		self.html_regex = build_filetype_regex(['html', '/'])
		self.domain_regex = compile(domain)
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
				if not html:
					print 'Bad URL was found'
					continue
				self.parser.feed(html)
				links = self.parser.get_links()
				http_links = [resolve_relative_path(url, x) for x in links if self.html_regex.search(x)]
				file_links = [resolve_relative_path(url, x) for x in links if self.file_regex.search(x)]
				for link in http_links:
					if link not in frontier and self.domain_regex.search(link):
						frontier.append(link)
				for link in file_links:
					if self.domain_regex.search(link) and len(seen) < self.limit - 1:
						seen.append(link)
				seen.append(url)
		return seen


def read_html(url):
	request = Request(url)
	try:
		html = ''.join(urlopen(request).readlines())
		return html
	except URLError:
		print 'URL: %s\t is unavailable' % url
		return None


def get_robots_url(url):
	host = urlparse(url).netloc
	return 'http://' + host + '/robots.txt'


def resolve_relative_path(host, url):
	if not search('(html|/)$', host):
		host += '/'
	result = urljoin(host, url)
	return result


def build_filetype_regex(filetypes):
	s = r'.('
	for f in filetypes:
		s += f + '|'
	s = s[:-1]
	s += ')$'
	return compile(s)


def write_links(filename, links):
	links.sort()
	with open(filename, 'w') as f:
		for link in links:
			f.write(link)
			f.write('\n')


def parse_args():
	parser = ArgumentParser(description='Crawl the web. Hack the planet.')
	parser.add_argument('-s', '--source', default='http://ciir.cs.umass.edu', dest='source',
						help='The URL to crawl from', metavar='source')
	parser.add_argument('-l', '--limit', default=100, type=int, dest='limit',
						help='Limit the number of URL\'s to crawl', metavar='limit')
	parser.add_argument('-w', '--wait', default=5, type=int, dest='wait', help='Time to wait between requests',
						metavar='wait')
	parser.add_argument('-d', '--domain', default='cs.umass.edu', dest='domain',
						help='Limit the crawler to a specific domain', metavar='domain')
	return parser.parse_args()


def main():
	args = parse_args()
	pc = PyCrawler(args.source, filetypes=['pdf'], limit=args.limit, wait=args.wait, domain=args.domain)
	links = pc.crawl()
	print len(links)
	write_links('../results.txt', links)


if __name__ == '__main__':
    main()
