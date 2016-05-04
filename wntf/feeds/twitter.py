# -*- coding: utf-8 -*-
from __future__ import absolute_import
import twitter

from .base import Feed


class AlgorithmChoice(object):
    PROFILE = 'profile'
    FEED = 'feed'


class TwitterFeed(Feed):
    algorithm_choice = AlgorithmChoice.FEED

    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret, user):
        self.client = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token,
            access_token_secret=access_token_secret)
        self.client.VerifyCredentials()
        self.user = user

    def fetch_data(self):
        return TwitterFeed.algorithm_map[self.algorithm_choice](self)

    def get_profile_iter(self):
        pass

    def get_feed_iter(self):
        return self.client.GetUserTimeline(screen_name=self.user)

    algorithm_map = {
        AlgorithmChoice.PROFILE: get_profile_iter,
        AlgorithmChoice.FEED: get_feed_iter
    }
