# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import wordnet
from functools import reduce

from .graphs import word_cloud as graph_words
from .graphs import wheel_radii


class DiversityAlgorithm(object):
    def __init__(self, log):
        '''
        :param log: The `logging` instance
        :type  log: Instance of the Python log
        '''
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
        '''
        Tokenize and categorise the words in the collection of
        text

        :param lines: The list of strings with the text to match
        :type  lines: ``list`` of ``str``

        :rtype: :class:
        :return:
        '''
        try:
            tokenized_words = nltk.word_tokenize(lines)
            return nltk.pos_tag(tokenized_words)
        except LookupError as le:
            print("Run install_words.py first")
            raise le

    def nouns(self, tagged_text):
        '''
        Find all nouns in a collection of tagged text
        '''
        self.log.debug('Collecting nouns')
        return self.findtags('NN', tagged_text)

    def findtags(self, tag_prefix, tagged_text):
        '''
        Find all words that match a 'tag' (word type) prefix

        :param tag_prefix: The tag prefix
        :type  tag_prefix: ``str``

        :param tagged_text: The text to search
        :type  tagged_text: ``list`` of ``dict``
        '''
        cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
            if tag.startswith(tag_prefix))
        return dict((tag, cfd[tag].most_common(50)) for tag in cfd.conditions())

    def synsets(self, word):
        '''
        Get synsets for a given word

        :param word: The word
        :type  word: ``str``

        :rtype: ``list`` of :class:`Synset`
        '''
        return wordnet.synsets(word)

    def load_wheel(self, wheel, data_file):
        '''
        Load the data from a wheel data file

        :param wheel: The target diversity wheel
        :type  wheel: ``dict``

        :param data_file: The path to the wheel data file
        :type  data_file: ``str``
        '''
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

    def load_wheels(self):
        '''
        Load the data for all diversity wheels
        '''
        for key, wheel in self.wheels.items():
            self.load_wheel(wheel, wheel['data'])

    def increment_pattern(self, pattern, word, count):
        '''
        A word has matched a pattern in a wheel, increment the match on the wheel
        '''
        pattern['count'] = pattern['count'] + count
        pattern['matches'].append(word)

    def match_wheel_word(self, wheel, word, count):
        '''
        Try and match a word against a wheel

        :param wheel: The target wheel
        :type  wheel: ``dict``

        :param word: The word to match
        :type  word: ``str``

        :rtype: ``bool``
        :return: `True` if match, else `False`
        '''
        for key, patterns in wheel['pattern'].items():
            if word in patterns['words']:
                self.increment_pattern(patterns, word, count)
                return True
        return False

    def match_wheel(self, wheel, synset, word, count):
        '''
        Attempt to match a keyword to a wheel

        :param wheel: The target wheel
        :type  wheel: ``dict`` wheel

        :param synset: The word synset
        :type  synset: :class:`Synset`

        :param word: The target word
        :type  word: ``str``

        :rtype: ``bool``
        :return: `True` if match, else `False`
        '''
        # first check if the word itself matches a wheel
        if self.match_wheel_word(wheel, word, count):
            self.log.debug('matched word %s to wheel', word)
            return True
        # see if each hypernym matches a wheel
        synsets = wordnet.synsets(word)
        if len(synsets) > 0:
            for synset in synsets:
                for hypernym in synset.hypernyms():
                    proper_name = hypernym.name().split('.')[:1][0]
                    if self.match_wheel_word(wheel, proper_name, count):
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
        graph_words(word_cloud_combined)
        for noun_type, words in word_cloud_nouns.items():
            for word, count in words:
                nets = wordnet.synsets(word)
                # inspect the first net and see what type of word it is
                for key, wheel in self.wheels.items():
                    if self.match_wheel(wheel, nets, word, count):
                        break

        for key, wheel in self.wheels.items():
            wheel_radii(wheel, key)
        '''
        TODO:
        - map those in a chord where the size of the difference
            between the angles in the chord represents the difference,
            e.g. carpenter is very different to IT, but banker is similar to accountant
        '''
