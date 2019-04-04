"""
============================== 핵심일 ==============================
"""
# 패키지 라이브러리
from twitter import *

#doc#


# 나의 패키지
import __pymongo as mg
import __Twitter as twitter
import __list as lh

# 오픈 패키지
import numpy as np

from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer()
from nltk.corpus import stopwords
from collections import defaultdict
from collections import Counter

import tweepy
import pickle
import string
import json
import time
from random import sample

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 모듈 라이브러리
import News

# 전역변수
from Twitter_ import *

"""
============================== 로딩 ==============================
"""
def 보고용_트위터_유저타임라인df_기초검사_및_청소후_로딩():
    import Twitter_Classifier as classifier
    import Cleaner

    """
    분류된 뉴스 자료 로딩
    기초 검사 및 청소
    """
    df, g = classifier.TW_Predicted_Orig_df로딩(test_tbl='트위터_유저타임라인', test_col='text', dbgon=False)
    df = df.rename(columns={'_id':'tw_id'})
    df = Cleaner.any_None_columns_삭제(df=df)
    df = Cleaner.df컬럼들에_대한_중복처리(df=df, subset=DEDUPLICATE_COLS, action='제거')
    return df

"""
==============================  ==============================
"""
def time_series(fname):
    with open(data_path + fname, 'r') as f:
        all_dates = []
        for line in f:
            tweet = json.loads(line)
            all_dates.append(tweet.get('created_at'))
        ones = np.ones(len(all_dates))
        idx = pd.DatetimeIndex(all_dates)
        # the actual series (at series of 1s for the moment)
        my_series = pd.Series(ones, index=idx)

        # Resampling / bucketing into 1-minute buckets
        per_minute = my_series.resample('1Min', how='sum').fillna(0)
        print(my_series.head())
        print(per_minute.head())

        fig, ax = plt.subplots()
        ax.grid(True)
        ax.set_title("Tweet Frequencies")

        hours = mdates.MinuteLocator(interval=20)
        date_formatter = mdates.DateFormatter('%H:%M')

        datemin = datetime(2015, 10, 31, 15, 0)
        datemax = datetime(2015, 10, 31, 18, 0)

        ax.xaxis.set_major_locator(hours)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_xlim(datemin, datemax)
        max_freq = per_minute.max()
        ax.set_ylim(0, max_freq)
        ax.plot(per_minute.index, per_minute)

        plt.savefig(data_path + 'tweet_time_series.png')



def hashtag_stats(fname):
    # fname = user_timeline_screen_name.jsonl
    def get_hashtags(tweet):
        entities = tweet.get('entities', {})
        hashtags = entities.get('hashtags', [])
        return [tag['text'].lower() for tag in hashtags]

    with open(data_path + fname, 'r') as f:
        hashtag_count = defaultdict(int)
        for line in f:
            tweet = json.loads(line)
            hashtags_in_tweet = get_hashtags(tweet)
            n_of_hashtags = len(hashtags_in_tweet)
            hashtag_count[n_of_hashtags] += 1

        tweets_with_hashtags = sum([count for n_of_tags, count in hashtag_count.items() if n_of_tags > 0])
        tweets_no_hashtags = hashtag_count[0]
        tweets_total = tweets_no_hashtags + tweets_with_hashtags
        tweets_with_hashtags_percent = "%.2f" % (tweets_with_hashtags / tweets_total * 100)
        tweets_no_hashtags_percent = "%.2f" % (tweets_no_hashtags / tweets_total * 100)
        print("{} tweets without hashtags ({}%)".format(tweets_no_hashtags, tweets_no_hashtags_percent))
        print("{} tweets with at least one hashtag ({}%)".format(tweets_with_hashtags, tweets_with_hashtags_percent))

        for tag_count, tweet_count in hashtag_count.items():
            if tag_count > 0:
                percent_total = "%.2f" % (tweet_count / tweets_total * 100)
                percent_elite = "%.2f" % (tweet_count / tweets_with_hashtags * 100)
                print("{} tweets with {} hashtags ({}% total, {}% elite)".format(tweet_count,
                                                                                 tag_count,
                                                                                 percent_total,
                                                                                 percent_elite))

def mention_frequency(fname):
    # fname = user_timeline_screen_name.jsonl
    def get_mentions(tweet):
        entities = tweet.get('entities', {})
        hashtags = entities.get('user_mentions', [])
        return [tag['screen_name'] for tag in hashtags]

    with open(data_path + fname, 'r') as f:
        users = Counter()
        for line in f:
            tweet = json.loads(line)
            mentions_in_tweet = get_mentions(tweet)
            users.update(mentions_in_tweet)
        for user, count in users.most_common(20):
            print("{}: {}".format(user, count))

def term_frequency(fname):
    # fname = user_timeline_screen_name.jsonl
    def process(text, tokenizer=TweetTokenizer(), stopwords=[]):
        """Process the text of a tweet:
        - Lowercase
        - Tokenize
        - Stopword removal
        - Digits removal

        Return: list of strings
        """
        text = text.lower()
        tokens = tokenizer.tokenize(text)
        # If we want to normalize contraction, uncomment this
        # tokens = normalize_contractions(tokens)
        return [tok for tok in tokens if tok not in stopwords and not tok.isdigit()]

    def normalize_contractions(tokens):
        """Example of normalization for English contractions.

        Return: generator
        """
        token_map = {
            "i'm": "i am",
            "you're": "you are",
            "it's": "it is",
            "we're": "we are",
            "we'll": "we will",
        }
        for tok in tokens:
            if tok in token_map.keys():
                for item in token_map[tok].split():
                    yield item
            else:
                yield tok

    tweet_tokenizer = TweetTokenizer()
    punct = list(string.punctuation)
    stopword_list = stopwords.words('english') + punct + ['rt', 'via']

    tf = Counter()
    with open(data_path + fname, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            tokens = process(text=tweet.get('text', ''),
                             tokenizer=tweet_tokenizer,
                             stopwords=stopword_list)
            tf.update(tokens)

        # 내가 추가 변경.
        df = pd.DataFrame([dict(tf)]).T.rename(columns={0:'개수'})
        df['토큰'] = df.index
        df.index = range(len(df))
        return df

def followers_stats(screen_name):
    followers_file = data_path + 'users/{}/followers.jsonl'.format(screen_name)
    friends_file = data_path + 'users/{}/friends.jsonl'.format(screen_name)
    with open(followers_file) as f1, open(friends_file) as f2:
        t0 = time.time()
        followers = []
        friends = []
        for line in f1:
            profile = json.loads(line)
            followers.append(profile['screen_name'])
        for line in f2:
            profile = json.loads(line)
            friends.append(profile['screen_name'])
        t1 = time.time()
        mutual_friends = [user for user in friends if user in followers]
        followers_not_following = [user for user in followers if user not in friends]
        friends_not_following = [user for user in friends if user not in followers]
        t2 = time.time()
        print("----- Timing -----")
        print("Initialize data: {}".format(t1-t0))
        print("Set-based operations: {}".format(t2-t1))
        print("Total time: {}".format(t2-t0))
        print("----- Stats -----")
        print("{} has {} followers".format(screen_name, len(followers)))
        print("{} has {} friends".format(screen_name, len(friends)))
        print("{} has {} mutual friends".format(screen_name, len(mutual_friends)))
        print("{} friends are not following {} back".format(len(friends_not_following), screen_name))
        print("{} followers are not followed back by {}".format(len(followers_not_following), screen_name))

        some_mutual_friends = ', '.join(sample(mutual_friends, len(mutual_friends)))
        print("Some mutual friends: {}".format(some_mutual_friends))

def 팔로워_팔로잉_얻기(screen_name):
    def 팔로워와_팔로잉의_컬럼비교(li):
        df1 = pd.DataFrame(li[0])
        df2 = pd.DataFrame(li[1])
        li1 = list(df1.columns)
        li2 = list(df2.columns)
        print( lh.리스트1로부터_리스트2를_제거(li1, li2) )

    followers_file = data_path + 'users/{}/followers.jsonl'.format(screen_name)
    friends_file = data_path + 'users/{}/friends.jsonl'.format(screen_name)
    with open(followers_file) as f1, open(friends_file) as f2:
        t0 = time.time()
        followers = []
        friends = []
        for line in f1:
            profile = json.loads(line)
            followers.append(profile)
        for line in f2:
            profile = json.loads(line)
            friends.append(profile)

        li = [followers, friends]
        팔로워와_팔로잉의_컬럼비교(li)
        return li

def influence(screen_name1, screen_name2):
    followers_file1 = data_path + 'users/{}/followers.jsonl'.format(screen_name1)
    followers_file2 = data_path + 'users/{}/followers.jsonl'.format(screen_name2)
    with open(followers_file1) as f1, open(followers_file2) as f2:
        reach1 = []
        reach2 = []
        for line in f1:
            profile = json.loads(line)
            reach1.append((profile['screen_name'], profile['followers_count']))
        for line in f2:
            profile = json.loads(line)
            reach2.append((profile['screen_name'], profile['followers_count']))

    profile_file1 = data_path + 'users/{}/user_profile.json'.format(screen_name1)
    profile_file2 = data_path + 'users/{}/user_profile.json'.format(screen_name2)
    with open(profile_file1) as f1, open(profile_file2) as f2:
        profile1 = json.load(f1)
        profile2 = json.load(f2)
        followers1 = profile1['followers_count']
        followers2 = profile2['followers_count']
        tweets1 = profile1['statuses_count']
        tweets2 = profile2['statuses_count']

    sum_reach1 = sum([x[1] for x in reach1])
    sum_reach2 = sum([x[1] for x in reach2])
    avg_followers1 = round(sum_reach1 / followers1, 2)
    avg_followers2 = round(sum_reach2 / followers2, 2)

    timeline_file1 = data_path + 'user_timeline_{}.jsonl'.format(screen_name1)
    timeline_file2 = data_path + 'user_timeline_{}.jsonl'.format(screen_name2)
    with open(timeline_file1) as f1, open(timeline_file2) as f2:
        favorite_count1, retweet_count1 = [], []
        favorite_count2, retweet_count2 = [], []
        for line in f1:
            tweet = json.loads(line)
            favorite_count1.append(tweet['favorite_count'])
            retweet_count1.append(tweet['retweet_count'])
        for line in f2:
            tweet = json.loads(line)
            favorite_count2.append(tweet['favorite_count'])
            retweet_count2.append(tweet['retweet_count'])
    avg_favorite1 = round(sum(favorite_count1) / tweets1, 2)
    avg_favorite2 = round(sum(favorite_count2) / tweets2, 2)
    avg_retweet1 = round(sum(retweet_count1) / tweets1, 2)
    avg_retweet2 = round(sum(retweet_count2) / tweets2, 2)
    favorite_per_user1 = round(sum(favorite_count1) / followers1, 2)
    favorite_per_user2 = round(sum(favorite_count2) / followers2, 2)
    retweet_per_user1 = round(sum(retweet_count1) / followers1, 2)
    retweet_per_user2 = round(sum(retweet_count2) / followers2, 2)
    print("----- Stats {} -----".format(screen_name1))
    print("{} followers".format(followers1))
    print("{} users reached by 1-degree connections".format(sum_reach1))
    print("Average number of followers for {}'s followers: {}".format(screen_name1, avg_followers1))
    print("Favorited {} times ({} per tweet, {} per user)".format(sum(favorite_count1), avg_favorite1, favorite_per_user1))
    print("Retweeted {} times ({} per tweet, {} per user)".format(sum(retweet_count1), avg_retweet1, retweet_per_user1))
    print("----- Stats {} -----".format(screen_name2))
    print("{} followers".format(followers2))
    print("{} users reached by 1-degree connections".format(sum_reach2))
    print("Average number of followers for {}'s followers: {}".format(screen_name2, avg_followers2))
    print("Favorited {} times ({} per tweet, {} per user)".format(sum(favorite_count2), avg_favorite2, favorite_per_user2))
    print("Retweeted {} times ({} per tweet, {} per user)".format(sum(retweet_count2), avg_retweet2, retweet_per_user2))

if __name__ == '__main__':
    print('\n' + '='*60 + sys.modules[__name__].__file__)
    #pp.pprint({'sys.path':sys.path})
    #pp.pprint({'dir()':dir()})

    보고용_트위터_유저타임라인df_기초검사_및_청소후_로딩()
