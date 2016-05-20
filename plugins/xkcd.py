from urllib2 import urlopen
from urllib import quote_plus

from util import hook, http

@hook.command
def xkcd(inp, nick=''):
    ".xkcd <some string>"
    base_url = 'https://relevantxkcd.appspot.com/process?action=xkcd&query='
    data = urlopen(base_url + quote_plus(inp)).read()
    return "xkcd.com/{}".format(data.split()[2])
