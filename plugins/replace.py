" seen.py: written by rray in "

from util import hook
import os
import re
from collections import deque

chan_db = {}

@hook.event('PRIVMSG')
def log_msg(inp, nick=''):
    if re.match(r's/(.*)/(.*)', inp[1]) != None:
        return
    if not inp[0] in chan_db:
        chan_db[inp[0]] = {}
    if not nick in chan_db[inp[0]]:
        chan_db[inp[0]][nick] = deque(maxlen=15)
    chan_db[inp[0]][nick].append(inp[1])

@hook.regex(r'^s/(.*)/(.*)')
def strreplace(match, say=None, chan='', nick=''):
    "s/<text to be replace>/<replacement text>"
    print "wow pls"
    p = match.groups()[0]
    n = match.groups()[1]
    print "p", p, "n", n
    try:
        for i in reversed(chan_db[chan][nick]):
            t = re.search(p, i)
            if t != None:
                say("<{}> {}".format(nick, re.sub(p, n, i)))
                return
    except:
        pass
