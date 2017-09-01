# coding: utf8
import re
import logging
import logging.handlers
import urllib2
import threading
from Queue import Queue


q = Queue()
q.put('www.sohu.com')
valided_urls = set()
reg = re.compile(r'".*?//([\w, \.]*?sohu\.com.*?)"')
handler = logging.handlers.RotatingFileHandler(
    './exceptions.log',
    maxBytes=100 *1024 * 1024,
    backupCount=5
)
formatter = logging.Formatter(
    '%(asctime)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def valid():
    url = q.get()
    if url in valided_urls:
        return
    valided_urls.add(url)
    try:
        r = urllib2.urlopen('http://' + url, timeout=2)
        if r.code >= 400:
            logger.warning('%(url)s-%(code)s-%(msg)s' % {
                'url': r.url,
                'code': r.code,
                'msg': r.msg
            })
        content = r.read()
    except Exception as e:
        content = ''
        logger.warning('%(url)s-%(code)s-%(msg)s' % {
            'url': url,
            'code': 0,
            'msg': str(e)
        })
    urls = set(re.findall(reg, content))
    for u in urls:
        q.put(u)


def main():
    while True:
        if q.empty():
            break
        t1 = threading.Thread(target=valid)
        t2 = threading.Thread(target=valid)
        t3 = threading.Thread(target=valid)
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()


if __name__ == '__main__':
    main()
