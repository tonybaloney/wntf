# -*- coding: utf-8 -*-
import yaml
import json
from functools import reduce

from .feeds.twitter import TwitterFeed
from .algorithm import tag, nouns


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

    with open('cache.json', 'w') as outfile:
        json.dump(data, outfile)

    word_cloud = []
    reduce(lambda x, y: word_cloud.extend(tag(y)),
                    data)
    word_cloud_nouns = nouns(word_cloud)
    try:
        print(word_cloud_nouns)
    except UnicodeEncodeError:
        print("Contains unicode, skipping")
        pass

if __name__ == '__main__':
    main()
