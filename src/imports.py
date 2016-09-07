#coding=utf-8

''' imports data managed by data.py into web database
    please run import.sh instead of running this directly '''

import data

import django
django.setup()

from search.models import Pages, Inverted
Pages.objects.all().delete()
Inverted.objects.all().delete()

pages = data.load("pages")
inverted = data.load("inverted")

cnt = 0
objList = []
for page in pages:
    print "create page %d/%d" % (cnt, len(pages))

    obj = Pages(
        id = cnt,
        htmlurl = page['htmlurl'],
        date = page['date'],
        title = page['title'],
        columnName = page['columnName'],
        content = page['content']
    )
    objList.append(obj)

    cnt += 1
Pages.objects.bulk_create(objList)

cnt = 0
objList = []
for key in inverted:
    print "create inverted %d/%d" % (cnt, len(inverted))
    cnt += 1

    for id in inverted[key]:
        obj = Inverted(key = key, pageId = id)
        objList.append(obj)
        if (len(objList) > 10000):
            Inverted.objects.bulk_create(objList)
            objList = []
Inverted.objects.bulk_create(objList)

