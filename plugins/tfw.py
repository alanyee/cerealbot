import socket
import random
import nltk

from util import hook, http

socket.setdefaulttimeout(10)  # global setting

@hook.command()
def tfw(inp, say=None):
    r = "tfw "
    if random.randint(0,1) == 0:
        r += "no "
    if random.randint(0,1) == 0:
        r += find_word('VB') + " "
    say(r + find_word('N'))

def find_word(tag):
    d = open('/usr/share/dict/words').read().split('\n')
    w = d[random.randint(0,len(d))].strip().translate(None, "'")
    t = nltk.pos_tag(nltk.word_tokenize(w))[0][1]
    while t[:len(tag)] != tag:
        w = d[random.randint(0,len(d))].strip().translate(None, "'")
        t = nltk.pos_tag(nltk.word_tokenize(w))[0][1]
    return w


