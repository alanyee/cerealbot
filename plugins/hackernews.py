import urllib2
import json
import re
import argparse
import random
from bs4 import BeautifulSoup

from util import hook, http

@hook.regex('https://news.ycombinator.com/item\?id=(\d+)')
def link_id(match, say=None):
    say(hn_id(match.group(1)))

@hook.regex('https://news.ycombinator.com/user\?id=(\w+)')
def link_user(match, say=None):
    say(hn_user(match.group(1)))

@hook.command
@hook.command('hn')
def hackernews(inp, nick=''):
    ".hackernews|.hn (-f only posts currently on frontpage)/(-d sort by recency) <query>/--user|-u <user>/--id|-i <id>"
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', nargs=1)
    parser.add_argument('-i', '--id', nargs=1)
    parser.add_argument('-d',  action='store_true')
    parser.add_argument('-f',  action='store_true')
    parser.add_argument('query', metavar='query', nargs='*')

    args = vars(parser.parse_args(str(inp).split()))

    if args['id']:
        if args['query'] or args['user']:
            return 'id or other things. pick one. pick wisely'
        return hn_id(args['id'])
    else:
        if args['query'] or args['f']:
            return hn_query(args)
        elif args['user']:
            return hn_user(args['user'][0])

def hn_query(args):
    if args['d']:
        url = 'http://hn.algolia.com/api/v1/search_by_date?'
    else:
        url = 'http://hn.algolia.com/api/v1/search?'
    if args['f']:
        url = url + 'tags=front_page&'

    url = url+'query='+'+'.join(args['query'])

    response = urllib2.urlopen(url)
    data = json.load(response)   
    hits = data['hits']
    post = None
    if len(hits) == 0:
        return 'no posts matching that query'
    if args['user']:
        for i in hits:
            if i['author'] == args['user']:
                post = i
                break
        if post == None:
            return "no posts by that author"
    elif args['f'] and not args['query']:
        post = hits[random.randint(0, len(hits))]
    else:
        post = hits[0]

    return hn_id(post['objectID'])

def hn_id(object_id):
    url = 'http://hn.algolia.com/api/v1/items/'+object_id
    hn_url = 'https://news.ycombinator.com/item?id='+object_id
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        if data['points'] is None or data['points'] == 'None':
            data['points'] = 0
        if 'title' in data:
            result = u'[ ({} points) {} by {} | {} | HN Discussion: {} ]'.format(data['points'], data['title'], data['author'], data['url'], hn_url)
        else:
            print data
            soup = BeautifulSoup(data['text'])
            data['text'] = soup.get_text()
            result = u'[ ({} points) "{}" by {} ]'.format(data['points'], data['text'], data['author'])
            if len(result) > 408:
                data['text'] = data['text'][:408-len(result)-3] + '...'
            result = u'[ ({} points) "{}" by {} ]'.format(data['points'], data['text'], data['author'])
    except Exception as e:
        print url
        print e
        return "post not found"
    return result

def hn_user(user):
    url = 'http://hn.algolia.com/api/v1/users/'+user
    hn_url = 'https://news.ycombinator.com/user?id='+user
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)
        about = data['about']
        if len(about) == 0:
            return '[ User: {} | karma: {} | Link: {} ]'.format(data['username'], data['karma'], hn_url)
        about = about.split('<p>')[0]
        return '[ User: {} | karma: {} | {} | Link: {} ]'.format(data['username'], data['karma'], about, hn_url)
    except Exception as e:
        print e, type(e)
        return "user not found"
