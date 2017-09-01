# coding: utf8
import re
import logging
import urllib2
import thread
from Queue import Queue


q = Queue()
q.put('www.sohu.com')
valided_urls = set()
reg = re.compile(r'".*?//([\w, \.]*?sohu\.com.*?)"')


def valid():
    url = q.get()
    if url in valided_urls:
        return
    valided_urls.add(url)
    try:
        r = urllib2.urlopen('http://' + url, timeout=2)
        if r.code >= 400:
            print r.url, r.code, r.msg, datetime.datetime()
        content = r.read()
    except Exception as e:
        content = ''
        print str(e)
    urls = set(re.findall(reg, content))
    print len(urls)
    for u in urls:
        q.put(u)


def main():
    while True:
        valid()


if __name__ == '__main__':
    main()
