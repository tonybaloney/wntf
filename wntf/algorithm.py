# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import wordnet
from functools import reduce

from .graphs import word_cloud as graph


class DiversityAlgorithm(object):
    def __init__(self, log):
        self.log = log
        with open('exclude_words.txt', 'r') as exclude:
            self.exclude_words = [line.rstrip() for line in exclude]
            self.log.debug('Filtering a collection of %i words',
                           len(self.exclude_words))

    wheels = {
        'profession': {
            'data': 'profession.txt',
            'words': [],
            'synsets': wordnet.synsets('profession')[0]},
        'orientation': {
            'data': 'orientation.txt',
            'words': [],
            'synsets': wordnet.synsets('orientation')[0]},
    }

    def tag(self, lines):
        try:
            tokenized_words = nltk.word_tokenize(lines)
            self.log.debug('Forming tokenize collection for %i items',
                      len(tokenized_words))
            return nltk.pos_tag(tokenized_words)
        except LookupError as le:
            print("Run install_words.py first")
            raise le

    def nouns(self, tagged_text):
        self.log.debug('Collecting nouns')
        return self.findtags('NN', tagged_text)

    def findtags(self, tag_prefix, tagged_text):
        cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
            if tag.startswith(tag_prefix))
        return dict((tag, cfd[tag].most_common(20)) for tag in cfd.conditions())

    def synsets(self, word):
        return wordnet.synsets(word)

    def process(self, data):
        word_cloud = []
        # Merge all the profile descriptions into 1 tag collection
        reduce(lambda x, y: word_cloud.extend(self.tag(y)), data)
        word_cloud_nouns = self.nouns(word_cloud)
        word_cloud_combined = []

        for noun_type, words in word_cloud_nouns.items():
            word_cloud_combined.extend(words)
        word_cloud_combined = filter(lambda x: x[0] not in self.exclude_words,
                                     word_cloud_combined)
        # Create visual word cloud
        graph(word_cloud_combined)

        for noun_type, words in word_cloud_nouns.items():
            for word, _ in words:
                if word not in self.exclude_words:
                    self.log.debug('Assessing nets for %s', word)

                    nets = wordnet.synsets(word)
                    self.log.debug('Got %i synsets', len(nets))
                    # inspect the first net and see what type of word it is
                    for key, wheel in self.wheels.items():
                        if len(nets) > 0:
                            # see if each hypernym matches a wheel
                            for hypernym in nets[0].hypernyms():
                                if wheel['synsets'].name().split('.')[:1] == \
                                hypernym.name().split('.')[:1]:
                                    self.log.debug('Matched %s to wheel %s', word, key)
                                    if nets[0] not in wheel['words']:
                                        print(word)
                                        wheel['words'].append(nets[0])
                        else:
                            self.log.warning('%s was not found in the synsets', word)

        '''
        TODO: This is half finished (my flight leaves soon)
        - build up a map of wheels and the words in those wheels (e.g professions, regligion, interests)
        - map those in a chord where the size of the difference between the angles in the chord represents the difference,
            e.g. carpenter is very different to IT, but banker is similar to accountant
        '''
