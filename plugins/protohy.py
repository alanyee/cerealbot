import nltk
import wikiquote as wq
import random
from sys import argv

def inc(db, key):
    if key not in db:
        db[key] = 0
    db[key] += 1

def find_hype_words(quote):
    print("finding hype word")
    tagged_words = nltk.pos_tag(nltk.word_tokenize(quote))
    nouns = {}
    pnouns = {}
    for word, tag in tagged_words:
        if tag == 'NN':
            inc(nouns, word)
        elif tag == 'PNN':
            inc(pnouns, word)
    print("constructed databases")
    if len(nouns) + len(pnouns) == 0:
        return None, None
    source_db = nouns
    replacement = 'blockchain'
    if len(pnouns) > 0 and (len(nouns) == 0 or max(nouns.values()) < max(pnouns.values())):
        source_db = pnouns
        replacement = 'Blockchain'
    max_freq = max(source_db.values())
    options = []
    for word in source_db:
        if source_db[word] == max_freq:
            options.append(word)
    return random.sample(options, max(len(options)/10, 1)), replacement

def hypify(quote):
    hype_words, replacement = find_hype_words(quote)
    print("hype_words: ", hype_words)
    if hype_words is None:
        return None
    hype_msg = quote.split()
    for i in range(len(hype_msg)):
        sanitized = hype_msg[i].strip(",.!?")
        if sanitized in hype_words:
            hype_msg[i] = hype_msg[i].replace(sanitized, replacement)
    return ' '.join(hype_msg)

def main():
    if len(argv) > 1:
        print(hypify(" ".join(argv[1:])))
    else:
        while True:
            try:
                titles = wq.random_titles(max_titles=1)
                print("found title: ", titles)
                quote= wq.quotes(titles[0])[0]
            except:
                continue
            break
        print("got quote:\n", quote)
        hype = hypify(quote)
        while hype is None:
            hype = hypify(quote)
        print(hype)

if __name__ == '__main__':
    main()
