#coding=utf-8
import re
import time
import json
import urllib2
import HTMLParser # just used to unescape

def load(url):
    ''' get response body from a url '''
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11' }
    req = urllib2.Request(url, None, headers)
    ret = urllib2.urlopen(req).read()
    time.sleep(0.2)
    return ret;

def loadJson(url, encoding = 'utf-8'):
    ''' get json response from a url '''
    try:
        raw = load(url)
        ret = json.loads(raw, encoding)
    except urllib2.HTTPError as err:
        if err.code == 404:
            ret = None
        else:
            raise
    return ret

def htmlToText(html):
    text = " ".join(re.split("<.*?>", html))
    return HTMLParser.HTMLParser().unescape(text.decode('utf8')).encode('utf8')

def loadIndex(stYear = 2016, stMonth = 1):
    ''' get index of all thu news throw JSON API '''
    print "loading index..."

    def nextMonth(year, month):
        month += 1
        if month == 13:
            month = 1
            year += 1
        return (year, month)
    
    def prevMonth(year, month):
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        return (year, month)
            
    def indexUrl(year, month):
        return 'http://news.tsinghua.edu.cn/publish/thunews/newsCollections/d_%d_%d.json' % (year, month);
    
    def addToIndex(obj):
        for i in obj["data"]:
            for item in obj["data"][i]:
                news = item.copy()
                news["date"] = "%s/%s/%s" % (obj["dateYearStr"], obj["dateMonStr"], item["day"])
                del news["day"]
                news['htmlurl'] = news['htmlurl'][:-5] + '_' + news['htmlurl'][-5:]
                news['title'] = news['title'].encode('utf8')
                index.append(news)
    
    index = []
    cnt = 0
    
    (year, month) = (stYear, stMonth)
    while True:
        print " -- %d: working on %d/%d" % (cnt, year, month)
        cnt += 1
        
        obj = loadJson(indexUrl(year, month))
        if obj == None:
            break
        addToIndex(obj)
        (year, month) = nextMonth(year, month)
    
    (year, month) = prevMonth(stYear, stMonth)
    while True:
        print " -- %d: working on %d/%d" % (cnt, year, month)
        cnt += 1
        
        obj = loadJson(indexUrl(year, month))
        if obj == None:
            break
        addToIndex(obj)
        (year, month) = prevMonth(year, month)
    
    return index

def loadPages(index):
    ''' load news according to index '''
    print "loading news"

    cnt = 0
    for item in index:
        print " -- %d: working on %s" % (cnt, item["title"])
        cnt += 1

        html = load("http://news.tsinghua.edu.cn/" + item["htmlurl"])
        contentHtml = re.search('<article.*?>(.*?)</article>', html, re.S).group(1)
        item["content"] = htmlToText(contentHtml)

    return index

