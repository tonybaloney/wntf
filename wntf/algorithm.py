# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import wordnet
from functools import reduce
from pprint import pprint
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)


wheels = {
    'profession': {
        'data': 'profession.txt',
        'words': [],
        'synsets': wordnet.synsets('profession')[0]}
}


def tag(lines):
    try:
        tokenized_words = nltk.word_tokenize(lines)
        log.debug('Forming tokenize collection for %i items',
                  len(tokenized_words))
        return nltk.pos_tag(tokenized_words)
    except LookupError as le:
        print("Run install_words.py first")
        raise le


def nouns(tagged_text):
    log.debug('Collecting nouns')
    return findtags('NN', tagged_text)


def findtags(tag_prefix, tagged_text):
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
        if tag.startswith(tag_prefix))
    return dict((tag, cfd[tag].most_common(20)) for tag in cfd.conditions())


def synsets(word):
    return wordnet.synsets(word)


def process(data):
    word_cloud = []
    # Merge all the profile descriptions into 1 tag collection
    reduce(lambda x, y: word_cloud.extend(tag(y)), data)
    word_cloud_nouns = nouns(word_cloud)

    with open('exclude_words.txt', 'r') as exclude:
        exclude_words = exclude.readlines()
        log.debug('Filtering a collection of %i words',
                  len(exclude_words))

    for noun_type, words in word_cloud_nouns.items():
        for word, _ in words:
            if word not in exclude_words:
                log.debug('Assessing nets for %s', word)
                nets = wordnet.synsets(word)
                log.debug('Got %i synsets', len(nets))
                # inspect the first net and see what type of word it is
                for key, wheel in wheels.items():
                    if len(nets) > 0:
                        if wheel['synsets'] in nets[0].hypernyms():
                            wheel['words'].append(nets[0])
                    else:
                        log.warning('%s was not found in the synsets', word)

    '''
    
    TODO: This is half finished (my flight leaves soon)
    - build up a map of wheels and the words in those wheels (e.g professions, regligion, interests)
    - map those in a chord where the size of the difference between the angles in the chord represents the difference,
        e.g. carpenter is very different to IT, but banker is similar to accountant
    
    '''
    pprint(wheels)
