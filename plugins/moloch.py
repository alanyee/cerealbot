import random
from util import hook, http

lines = open('plugins/files/moloch.text').readlines()

poem_quotes = []

for i in xrange(len(lines)):
    if lines[i][0] != ' ':
        if len(poem_quotes) > 0 and len(poem_quotes[-1]) > 0:
            poem_quotes[-1][-1] = poem_quotes[-1][-1].strip(',')
        poem_quotes.append([])
    poem_quotes[-1].append(lines[i].strip())

@hook.command('moloch')
def moloch(inp, nick='', say=None):
    global poem_quotes
    quote = random.choice(poem_quotes)
    for q in quote[:-1]:
        say(q)
    say(quote[-1].strip(',- \t\n'))
