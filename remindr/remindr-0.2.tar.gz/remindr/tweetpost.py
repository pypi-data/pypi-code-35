# vim:ts=4:sw=4:ft=python:fileencoding=utf-8
# Copyright © 2017-2019 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

'''Post a tweet to Twitter'''

# standard libraires imports
import logging

# 3rd party libraries imports
import feedparser
import tweepy

def tweetpost(clioptions, cfgoptions, tweet, language):
    '''Post a tweet'''
    if clioptions.dryrun:
         print('Should have tweeted => {tweet}'.format(tweet=tweet))
    else:
        consumer_key = cfgoptions['twitter']['consumer_key']
        consumer_secret = cfgoptions['twitter']['consumer_secret']
        access_token = cfgoptions['twitter']['access_token']
        access_token_secret = cfgoptions['twitter']['access_token_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        try:
            if 'path_to_image' in cfgoptions and cfgoptions['twitter']['image']:
                api.update_with_media(cfgoptions['image']['path_to_image'], tweet)
            elif '{lang}_image_path'.format(lang=language) in cfgoptions['image'] and cfgoptions['twitter']['image']:
                api.update_with_media(cfgoptions['image']['{lang}_image_path'.format(lang=language)], tweet)
            # if the user uses mastodon_image_path
            elif 'twitter_image_path' in cfgoptions['image'] and cfgoptions['twitter']['image']:
                api.update_with_media(cfgoptions['image']['twitter_image_path'], tweet)
            else:
                api.update_status(tweet)
        except tweepy.TweepError as err:
            logging.warning('Error occurred while updating status: {err}'.format(err=err))
