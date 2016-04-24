import socket
import subprocess
import time
import random
import nltk

from util import hook, http

socket.setdefaulttimeout(10)  # global setting


@hook.regex(r'(.*)(\w+)-ass\s(\w+)(.*)')
def assword(match, nick='', say=None):
    prefix = match.group(1)
    adj = match.group(2)
    noun = match.group(3)
    suffix = match.group(4)

    say("<{}> {}{} ass-{}{}".format(nick, prefix, adj, noun, suffix))

def get_version():
    try:
        stdout = subprocess.check_output(['git', 'log', '--format=%h'])
    except:
        revnumber = 0
        shorthash = '????'
    else:
        revs = stdout.splitlines()
        revnumber = len(revs)
        shorthash = revs[0]

    http.ua_skybot = 'Skybot/r%d %s (http://github.com/rmmh/skybot)' \
        % (revnumber, shorthash)

    return shorthash, revnumber


# autorejoin channels
@hook.event('KICK')
def rejoin(paraml, conn=None):
    if paraml[1] == conn.nick:
        if paraml[0].lower() in conn.conf.get("channels", []):
            conn.join(paraml[0])


# join channels when invited
@hook.event('INVITE')
def invite(paraml, conn=None):
    conn.join(paraml[-1])


@hook.event('004')
def onjoin(paraml, conn=None):
    # identify to services
    nickserv_password = conn.conf.get('nickserv_password', '')
    nickserv_name = conn.conf.get('nickserv_name', 'nickserv')
    nickserv_command = conn.conf.get('nickserv_command', 'IDENTIFY %s')
    if nickserv_password:
        conn.msg(nickserv_name, nickserv_command % nickserv_password)
        time.sleep(1)

    # set mode on self
    mode = conn.conf.get('mode')
    if mode:
        conn.cmd('MODE', [conn.nick, mode])

    # join channels
    for channel in conn.conf.get("channels", []):
        conn.join(channel)
        time.sleep(1)  # don't flood JOINs

    # set user-agent
    ident, rev = get_version()


@hook.command
def rekt(inp, say=None, nick=''):
    if(len(inp.strip()) != 0):
        nick = inp.strip()
    say(nick + ": #rekt")

@hook.command
def enlighten(inp, say=None, nick=''):
    if(len(inp.strip()) != 0):
        nick = inp.strip()
    say("And thus " + nick + " was enlightened")

@hook.command
def algernon(inp, say=None, nick=''):
    dc = ['hi', 'ping', 'did you get my email?', 'did you get my ping']
    dc.extend(['are you home? no one\'s answering the door'])
    dc.extend(['did you get my voicemail?'])
    dc.extend(['did you get my pm?', 'pls respond'])
    if(len(inp.strip()) != 0):
        nick = inp.strip()
    lim = random.randint(0,len(dc)/2)
    random.shuffle(dc)
    for i in range(lim):
        say(nick + ': ' + dc[i])

@hook.command
@hook.regex(r'^wooo*$')
def woo(inp, say=None):
    say('WOOOOOOOOOO' + str('O'*random.randint(0,10)) + '!')

@hook.command
def boo(inp, say=None):
    say('booooooo' + str('o'*random.randint(0,10)))

@hook.command
@hook.regex(r'^weee*$')
def wee(inp, say=None):
    say('weeeee' + str('e'*random.randint(0,10)) + '!')

@hook.regex(r'^wha*$')
def wha(inp, say=None):
    say('whaa' + str('a'*random.randint(0,10)) + 't?')

@hook.command
def pcoutin(inp, say=None):
    dc = ['a', 'w', 'f', 'r', 'e', 'p', 'g']
    lim = random.randint(12, 22)
    r = []
    for i in range(0, lim):
        r.append(dc[random.randint(0,6)])
    say("<pcoutin> " + ''.join(r))

@hook.command
def markov(inp, say=None):
    say("@markov " + inp)

@hook.command
def command(inp, say=None):
    say("," + inp)

@hook.regex(r'^unzzz$')
def unzzz(inp, nick='', say=None):
    sweet_princes = ['arnog', 'ajohn', 'dymk', 'rray', 'tetranoir',  'rhaps0dy', 'mike_pizza']
    if nick in sleeplist:
        say("good morning "+nick+"1")

@hook.regex(r'^zzz$')
def zzz(inp, nick='', say=None):
    sweet_princes = ['arnog', 'ajohn', 'dymk', 'rray', 'tetranoir',  'rhaps0dy', 'mike_pizza']
    if nick in sleeplist:
        say("good night sweet prince")

@hook.regex(r'^trust nobody$')
def trust(inp, say=None):
    say("not even yourself")

locations = {}
@hook.command
def find(inp):
    ".find <nick> find someone | set <nick> <location> set your location | unset <nick> unset your location"
    global locations
    ilist = inp.split()
    if ilist[0] == 'set':
        locations[ilist[1].lower().strip('_')] = ' '.join(ilist[2:])
        return 'set {}\'s location'.format(ilist[1])
    elif ilist[0] == 'unset':
        nick = ilist[1].strip('_').lower()
        if nick in locations:
            del locations[nick]
            return 'location for {} unset'.format(nick)
        else:
            return '{} not known'.format(nick)
    nick = ilist[0].strip('_').lower()
    if nick in locations:
        print locations
        return nick + ' is in ' + locations[nick]
    return 'idk'


@hook.command()
def recon(inp, say=None):
    nick = inp.split()[0]
    say("Searching the UCSD database for information about {}".format(nick))
    say("Scanning... ")
    say("Found an entry for {}".format(nick))
    say("{}: Computer Science and Engineering major at UCSD".format(nick))

@hook.command()
def sungod(inp, say=None):
    word = inp.split()[0]
    d = {'dymk': 'MOSSSHHHPIIIT WOOOO',
         'Oca': 'uuughghhhjkghh',
         'ac_': 'guuys pls no kamikaze pls',
         'rray': '#deded',
         'abuss': 'why didn\'t you ask me to go to sungod??? :(',
         'amber': 'oca pls',
         'snoop_dogg': 'HOW\'S IT GOING SDSU WOOOOO',
         'dwang': 'i\'ll just go because im scared of da police'}
    if word in d.keys():
        say('<{}> {}'.format(word, d[word]))

@hook.command('bz')
def bz(inp, say=None):
    bz_list = ["BAZINGA", "ZEMSCHWAMBLE", "BEDAZZLE", "ZABONGA", "ZIMBABWE", "SCHLAMZOONI", "ZLENGSHWANGLE"]
    bangs = random.randint(1, 6)
    say(random.choice(bz_list) + '!'*bangs)

@hook.regex(r'.*cerealbot is .*')
def thanks(match, nick=''):
    return 'thanks'


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

@hook.command()
def source(inp):
    return "https://github.com/rohan166/skybot"

@hook.regex(r'^\x01VERSION\x01$')
def version(inp, notice=None):
    ident, rev = get_version()
    notice('\x01VERSION skybot %s r%d - http://github.com/rmmh/'
           'skybot/\x01' % (ident, rev))
