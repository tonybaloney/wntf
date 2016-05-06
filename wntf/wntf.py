# -*- coding: utf-8 -*-
import yaml
import json
from functools import reduce
from pprint import pprint
from .feeds.twitter import TwitterFeed, AlgorithmChoice
from .algorithm import tag, nouns, antonyms


def main():
    with open('config.yml') as f:
        config = yaml.load(f)
    feed = TwitterFeed(
        config['consumer_key'],
        config['consumer_secret'],
        config['access_token'],
        config['access_token_secret'],
        config['user']
    )
    data = feed.fetch_data()

    if TwitterFeed.algorithm_choice != AlgorithmChoice.DUMMY:
        with open('cache.json', 'w') as outfile:
            json.dump(data, outfile)

    word_cloud = []
    reduce(lambda x, y: word_cloud.extend(tag(y)),
                    data)
    word_cloud_nouns = nouns(word_cloud)

    with open('exclude_words.txt', 'r') as exclude:
        exclude_words = exclude.read_lines()

    try:
        for noun_type in list(word_cloud_nouns):
            for word in word_cloud_nouns[noun_type]:
                if word not in exclude_words:
                    pprint(antonyms(word[0]))

    except UnicodeEncodeError:
        print("Contains unicode, skipping")
        pass

if __name__ == '__main__':
    main()
