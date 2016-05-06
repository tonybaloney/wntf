# -*- coding: utf-8 -*-
from __future__ import absolute_import
import twitter

from .base import Feed


class AlgorithmChoice(object):
    PROFILE = 'profile'
    FEED = 'feed'
    DUMMY = 'dummy'


class TwitterFeed(Feed):
    algorithm_choice = AlgorithmChoice.DUMMY

    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret, user):
        self.client = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token,
            access_token_secret=access_token_secret)
        if TwitterFeed.algorithm_choice != AlgorithmChoice.DUMMY:
            self.client.VerifyCredentials()
        self.user = user

    def fetch_data(self):
        return TwitterFeed.algorithm_map[self.algorithm_choice](self)

    def get_profile_iter(self):
        mates = self.client.GetFriends(screen_name=self.user)
        return [mate.description for mate in mates]

    def get_feed_iter(self):
        timeline = self.client.GetUserTimeline(screen_name=self.user)
        return [s.text for s in timeline]

    def get_dummy_iter(self):
        import json
        with open('cache.json', 'r') as file:
            text = file.read()
            return json.loads(text)

    algorithm_map = {
        AlgorithmChoice.PROFILE: get_profile_iter,
        AlgorithmChoice.FEED: get_feed_iter,
        AlgorithmChoice.DUMMY: get_dummy_iter
    }
