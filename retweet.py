# Import Tweepy, sleep, credentials.py
import os
import tweepy
import yaml
from time import sleep


def get_keys_and_token():
    if not os.path.isfile('keys.yaml'):
        keys = {'consumer_key': os.environ['CONSUMER_KEY'],
                'consumer_secret': os.environ['CONSUMER_SECRET'],
                'access_token': os.environ['ACCESS_TOKEN'],
                'access_token_secret': os.environ['ACCESS_TOKEN_SECRET'],
                }
    else:
        with open('keys.yaml') as f:
            keys = yaml.load(f, Loader=yaml.FullLoader)

    return keys


def like_and_retweet():
    # Get keys and token
    keys = get_keys_and_token()
    # Get config file
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Access and authorize our Twitter credentials from credentials.py
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth)

    # Define Keywords
    lang = config.get('settings', {}).get('language', 'en')
    max_tweet = config.get('settings', {}).get('max_tweet', '4')
    keywords = [f'#{k}' for k in config.get('keywords', [])]
    keywords = ' OR '.join(keywords) + '  -filter:retweets'

    new_tweet = 0
    for tweet in tweepy.Cursor(api.search, q=(keywords), lang=lang).items(15):
        try:
            # Add \n escape character to print() to organize tweets
            print('\nTweet by: @' + tweet.user.screen_name)

            if tweet.retweeted:
                print('Already Retweeted')
                continue

            # Retweet tweets as they are found
            tweet.retweet()
            print('Retweeted the tweet')
            tweet.favorite()
            print('Like the tweet')
            sleep(10)
            new_tweet += 1
            if new_tweet == max_tweet:
                break

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break


if __name__ == "__main__":
    like_and_retweet()
