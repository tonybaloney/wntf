# -*- coding: utf-8 -*-
import yaml
import json
from functools import reduce
from .feeds.twitter import TwitterFeed, AlgorithmChoice
from .algorithm import process, tag


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

    process(data)


if __name__ == '__main__':
    main()
