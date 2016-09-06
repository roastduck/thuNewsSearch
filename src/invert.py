#coding=utf-8

''' build the inverted list '''

import jieba
import HTMLParser

import data

def words(str):
    return set(filter(lambda x: not x.isspace(), map(lambda x: x.encode('utf8'), jieba.cut_for_search(str))))

def buildList(pages):
    inverted = {}
    cnt = -1

    for page in pages:
        cnt += 1 # not only used to display progress
        page["title"] = HTMLParser.HTMLParser().unescape(page["title"])
        print "%d: working on %s %s" % (cnt, page["date"], page["title"])

        for word in (words(page['title']) | words(page['content'])):
            if not inverted.has_key(word):
                inverted[word] = []
            inverted[word].append(cnt)
    
    return inverted

if __name__ == '__main__':
    pages = data.load('pages')
    data.save('inverted', buildList(pages))

