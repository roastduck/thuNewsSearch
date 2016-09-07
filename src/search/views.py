import re
import json
import time
import jieba
from django.forms.models import model_to_dict
from django.http import HttpResponse
from models import Pages

def search(request):
    ''' JSON API
        GET q : list of keywords to search
        GET page : page number to show, starting from 1
        GET filtertype : 0 = all, 1 = this year, 2 = this month
        return : { "error" : "message" } or a list of pages '''

    if (request.GET.has_key('q')):
        keywords = request.GET.getlist('q')
        keywords = list(reduce(lambda x, y: x | y, map(set, map(jieba.cut_for_search, keywords))))
    else:
        return HttpResponse('{ "error": "empty query" }', content_type = 'application/json')
    if (request.GET.has_key('page')):
        page = int(request.GET['page'])
    else:
        page = 1
    if (page < 1):
        page = 1
    if request.GET.has_key('filtertype'):
        filterType = int(request.GET['filtertype'])
    else:
        filterType = 0
    if (filterType < 0) or (filterType > 2):
        filterType = 0

    newsPerPage = 10
    news = Pages.satisfyKeys(keywords)[(page - 1) * newsPerPage : page * newsPerPage]
    news = map(model_to_dict, news)

    if filterType == 1:
        cur = time.strftime("%Y/")
        news = filter(lambda x: x["date"].startswith(cur), news)
    if filterType == 2:
        cur = time.strftime("%Y/%m")
        news = filter(lambda x: x["date"].startswith(cur), news)

    def digestContent(page):
        content = page['content']
        title = page['title']
        arr = []
        ret = ''

        for key in keywords:
            for piece in re.finditer(key, content):
                span = piece.span()
                span = (max(0, span[0] - 20), min(len(content), span[1] + 20))
                arr.append((span[0], 1))
                arr.append((span[1], -1))
        arr.sort(lambda x, y: 1 if x[0] > y[0] else -1 if x[0] < y[0] else 0)

        stPos = -1
        stCnt = 0
        for item in arr:
            if item[1] == 1:
                if stCnt == 0:
                    stPos = item[0]
                stCnt += 1
            else:
                stCnt -= 1
                if stCnt == 0:
                    ret += content[stPos : item[0]] + '...'
                    if len(ret) > 150:
                        break
                    stPos = -1
            if (stPos != -1) and (len(ret) + item[0] - stPos > 150):
                ret += content[stPos : item[0]] + '...'
                break
        if ret == '':
            ret = content[:130]

        for key in keywords:
            ret = ret.replace(key, "<em>%s</em>" % key)
            title = title.replace(key, "<em>%s</em>" % key)

        page['content'] = ret
        page['title'] = title
        return page

    news = map(digestContent, news)
    return HttpResponse(json.dumps(news).encode('utf8'), content_type = 'application/json')

