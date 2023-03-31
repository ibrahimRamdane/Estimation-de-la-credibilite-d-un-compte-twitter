import numpy as np
import pandas as pd
import tweepy
import os
import sys


from collect.API import *


def get_last_tweets(name, count):
    """_cette fonction retourne un dataframe pandas
    représentant le contenu des count-ièmes derniers tweets de l'utilisateur name, ainsi que 
    le nombre de retweets, le nombre de likes et l'id de chacun des tweets_

    Params:

        _name_ : string du nom de l'utilisateur twitter
        _count_ : integer du nombre de tweets à chercher

    Returns:
        _tweets_df_: _dataframe pandas des objets sus-cités_
    """

    api = twitter_setup()
    user = api.get_user(screen_name=name)
    ID = user.id_str
    tweets = tweepy.Cursor(api.user_timeline, id=ID,
                           tweet_mode='extended').items(count)

    objects = ['Date', 'Id', 'Texte', 'RT', 'Nombre likes']

    tweets_list = []

    for tweet in tweets:
        if 'retweeted_status' in tweet._json:
            tweets_list.append([tweet.created_at,  tweet.id,   tweet._json['retweeted_status']
                               ['full_text'], tweet.retweet_count, tweet.favorite_count])

        else:
            tweets_list.append([tweet.created_at,  tweet.id,
                               tweet.full_text, tweet.retweet_count, tweet.favorite_count])
    tweets_df = pd.DataFrame(tweets_list, columns=objects)

    # print(tweets_df)  # visu

    return tweets_df


def get_last_tweets_by_subject(subject, count_, result_type_='recent'):
    """_cette fonction retourne un dataframe pandas
    représentant le contenu du nombre count de tweets présents sur twitter relatifs au sujet _subject_, ainsi que 
    le nombre de retweets, le nombre de likes et l'id de chacun des tweets_

    Params:

        _subject_ : string du nom du sujet
        _count_ : integer du nombre de tweets à chercher
        _result_type__ : string pouvant être modifié par mixed (include both popular and real time results in the response)
                        ,recent (return only the most recent results in the response) and
                        popular (return only the most popular results in the response)

    Returns:
        _tweets_df_: _dataframe pandas des objets sus-cités_
    """

    #tweets = api.search_tweets(q= subject,result_type = result_type_ ,count = count_, tweet_mode='extended')

    api = twitter_setup()

    tweets = tweepy.Cursor(api.search_tweets, q=subject,
                           result_type=result_type_, tweet_mode='extended').items(count_)

    tweets_list = []
    for tweet in tweets:
        if 'retweeted_status' in tweet._json:
            tweets_list.append([tweet.created_at,  tweet.id,   tweet._json['retweeted_status']
                               ['full_text'], tweet.retweet_count, tweet.favorite_count])

        else:
            tweets_list.append([tweet.created_at,  tweet.id,
                               tweet.full_text, tweet.retweet_count, tweet.favorite_count])

    objects = ['Date', 'Id', 'Texte', 'RT', 'Nombre likes']
    tweets_df = pd.DataFrame(tweets_list, columns=objects)

    # print(tweets_df)

    return tweets_df


if __name__ == '__main__':
    subject = "wildfire"
    name_ = input("@ : ")
    get_last_tweets(subject, name_, 100)
