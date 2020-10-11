import random

from nltk.parse.generate import generate
from nltk import CFG


def rand_vocabulary(wpt=0.25):
    grammar = open('assets/text/grammar.txt', 'r').read()
    for i in ('N', 'Det', 'P', 'VP', 'VP_PP', 'VP_NP'):
        words = open(f'assets/text/{i}.txt', 'r').readlines()
        suffix = ''
        prefix = i
        if i.startswith('VP') and i != 'VP':
            suffix = ' ' + i.split('_')[1].strip()
            prefix = 'VP'
        for j in random.sample(words, int(len(words) * wpt)):
            if not j.strip():
                continue
            grammar += f"{prefix} -> '{j.strip()}'{suffix}\n"
    return grammar


def rand_sentences(n=10, depth=6, wpt=0.25):
    #grammar = CFG.fromstring(open('assets/text/grammar.txt', 'r').read())
    grammar = CFG.fromstring(rand_vocabulary(wpt))
    sentences = list(generate(grammar, n=n*20, depth=depth))
    return [' '.join(i) for i in random.sample(sentences, min(n, len(sentences)))]

def combine_sentences(n=2, depth=6, wpt=0.25):
    sentences = [i for _ in range(n) for i in rand_sentences(1, depth, wpt)]
    combs = [' ' + i for i in open('assets/text/C.txt', 'r').readlines() if i.strip()]
    combs = [i.replace('\n', '') for i in combs]
    combs += [',']
    s = sentences[0]
    for i in range(1, len(sentences)):
        s += random.choice(combs) + ' '
        s += sentences[i]
    s += '.'
    return s.capitalize()
