import tweepy
import configparser
import os


def get_tokens():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['TWITTER']['API_KEY']
    api_secret_key = config['TWITTER']['API_SECRET_KEY']
    access_token_key = config['TWITTER']['ACCESS_TOKEN']
    access_token_secret = config['TWITTER']['ACCESS_TOKEN_SECRET']
    return api_key, api_secret_key, access_token_key, access_token_secret


if __name__ == '__main__':
    consumer_key, consumer_secret, access_token, access_secret = get_tokens()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    os.chdir('demo')
    for image in os.listdir('.'):
        print(image)
        api.update_with_media(image)
