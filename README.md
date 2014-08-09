PyCrawler
=========

- A web crawler written in python (requires python 2.7)
- Collects HTML and PDF files only
- Always obeys robots.txt policies

How to Run
==========

- To run, simply run `$ python PyCrawler.py`
- Results are placed in the current directory in the file `results.txt`

Command Line Arguments
======================

`-s, --source`  The URL to start at

`-l, --limit`   Limit the number of URL's crawled

`-w, --wait`    Time, in seconds, to wait between requests

`-d, --domain`  Limit URL's crawled to domain
