import tweepy
import configparser
import os
import threading
import time
import sys

from tweepy.error import TweepError


WAIT_TIME = 20
done = False


def get_tokens():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['TWITTER']['API_KEY']
    api_secret_key = config['TWITTER']['API_SECRET_KEY']
    access_token_key = config['TWITTER']['ACCESS_TOKEN']
    access_token_secret = config['TWITTER']['ACCESS_TOKEN_SECRET']
    return api_key, api_secret_key, access_token_key, access_token_secret


def animate():
    for c in range(WAIT_TIME, -1, -1):
        if done:
            break
        sys.stdout.write('\rWaiting for ' + str(c) + ' secs.... ')
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\rTweeting\n')


def write_tweeted_img(file_name):
    file = open('tweeted_imgs.txt', 'a')
    file.write('{}\n'.format(file_name))
    file.close()


def check_img_tweeted(file_name):
    with open('tweeted_imgs.txt') as f:
        if file_name in f.read():
            return True
    return False


if __name__ == '__main__':
    consumer_key, consumer_secret, access_token, access_secret = get_tokens()
    count = 0

    print('Connecting to Twitter...')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    print('Connected!\n')

    os.chdir('images')
    for image in os.listdir('.'):

        if check_img_tweeted(image):
            print('Already Tweeted {} before'.format(image))
            os.remove(image)
            continue

        try:
            api.update_with_media(image)
            print('Tweeted {}'.format(image))
            write_tweeted_img(image)
            count += 1
            os.remove(image)
            done = False

        except TweepError:
            continue

        t = threading.Thread(target=animate)
        t.start()
        time.sleep(WAIT_TIME)
        done = True

    print('\nSuccessfully Tweeted {} Images'.format(count))
