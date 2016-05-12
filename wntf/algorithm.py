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
        self.load_wheels()

    wheels = {
        'profession': {
            'data': 'wntf/wheels/profession.txt',
            'words': [],
            'pattern': {},
            'synsets': wordnet.synsets('profession')[0]},
        'orientation': {
            'data': 'wntf/wheels/orientation.txt',
            'words': [],
            'pattern': {},
            'synsets': wordnet.synsets('orientation')[0]},
    }

    def tag(self, lines):
        try:
            tokenized_words = nltk.word_tokenize(lines)
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

    def load_wheel(self, wheel, data_file):
        with open(data_file, 'r') as wheel_data:
            lines = wheel_data.readlines()
            if len(lines) == 0:
                return
            lines = filter(lambda line: not line.startswith('#') and line.strip() != '', lines)
            for index in lines:
                indices = index.split(',')
                wheel['pattern'][indices[0].rstrip()] = {'words': [item.strip() for item in indices],
                                                         'matches': [],
                                                         'count': 0}
        print(wheel['pattern'])

    def load_wheels(self):
        for key, wheel in self.wheels.items():
            self.load_wheel(wheel, wheel['data'])

    def increment_pattern(self, pattern, word):
        pattern['count'] = pattern['count'] + 1
        pattern['matches'].append(word)

    def match_wheel_word(self, wheel, hypernym):
        for key, patterns in wheel['pattern'].items():
            if key == hypernym:
                self.increment_pattern(wheel['pattern'], hypernym)
                return True
            if hypernym in patterns['words']:
                self.increment_pattern(wheel['pattern'], hypernym)
                return True
        return False

    def match_wheel(self, wheel, synset, word):
        # see if each hypernym matches a wheel
        for hypernym in synset.hypernyms():
            proper_name = hypernym.name().split('.')[:1][0]
            self.log.debug('hypernym %s in %s', proper_name, word)
            if self.match_wheel_word(wheel, proper_name):
                self.log.debug('matched %s to wheel', proper_name)
                return True
        return False

    def process(self, data):
        word_cloud = []
        # Merge all the profile descriptions into 1 tag collection
        reduce(lambda x, y: word_cloud.extend(self.tag(y)), data)
        word_cloud_nouns = self.nouns(word_cloud)
        word_cloud_combined = []

        for noun_type, words in word_cloud_nouns.items():
            word_cloud_combined.extend(words)
        word_cloud_combined = filter(lambda x: x[0].lower() not in self.exclude_words,
                                     word_cloud_combined)
        # Create visual word cloud
        graph(word_cloud_combined)

        for noun_type, words in word_cloud_nouns.items():
            for word, _ in words:
                self.log.debug('Assessing nets for %s:%s', word, noun_type)

                nets = wordnet.synsets(word)
                self.log.debug('Got %i synsets', len(nets))
                # inspect the first net and see what type of word it is
                for key, wheel in self.wheels.items():
                    if len(nets) > 0:
                        for net in nets:
                            self.match_wheel(wheel, net, word)
                            # todo - break on match
                    else:
                        self.log.warning('%s was not found in the synsets', word)

        '''
        TODO: 
        - map those in a chord where the size of the difference between the angles in the chord represents the difference,
            e.g. carpenter is very different to IT, but banker is similar to accountant
        '''
