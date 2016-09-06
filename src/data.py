#coding=utf-8

''' manage data and store it as json '''

import json

path = '../data'

def load(key):
    f = open('%s/%s.json' % (path, key), 'r')
    return json.loads(f.read())

def save(key, value):
    f = open('%s/%s.json' % (path, key), 'w')
    f.write(json.dumps(value))

