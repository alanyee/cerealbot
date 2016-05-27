import random
from util import hook, http

poem_quotes = []

def update():
    global poem_quotes
    poem_quotes = []
    lines = open('plugins/files/moloch.text').readlines()
    for i in xrange(len(lines)):
        if lines[i][0] != ' ':
            if len(poem_quotes) > 0 and len(poem_quotes[-1]) > 0:
                poem_quotes[-1][-1] = poem_quotes[-1][-1].strip(',')
            poem_quotes.append([])
        poem_quotes[-1].append(lines[i].strip())

update()

@hook.command('moloch')
def moloch(inp, nick='', say=None):
    global poem_quotes
    if inp.isdigit() and int(inp) < len(poem_quotes):
        quote = poem_quotes[int(inp)]
    else:
        quote = random.choice(poem_quotes)
    for q in quote[:-1]:
        say(q)
    say(quote[-1].strip(',- \t\n'))
