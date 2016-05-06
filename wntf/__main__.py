# -*- coding: utf-8 -*-
import yaml
import argparse
import json
import logging

from .feeds.twitter import TwitterFeed, AlgorithmChoice
from .algorithm import DiversityAlgorithm


def main(args):
    log = logging.getLogger('__main__')
    if args.debug:
        print('Using debug level for logging')
        log.setLevel(logging.DEBUG)

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

    alg = DiversityAlgorithm(log)
    alg.process(data)
    print(alg.wheels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    main(args)
