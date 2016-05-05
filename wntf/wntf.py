# -*- coding: utf-8 -*-
import yaml
from .feeds.twitter import TwitterFeed
from .algorithm import tokenize


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
    for m in feed.fetch_data():
        print(tokenize(m))

if __name__ == '__main__':
    main()