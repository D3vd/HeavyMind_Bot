# TODO: Create a system that prevents duplicate Tweets

import praw
import configparser
import urllib.request
import time
import os

from prawcore.exceptions import ResponseException
from urllib.error import HTTPError


class ClientInfo:
    id = ''
    secret = ''
    user_agent = 'Image_Scraper'


def get_client_info():
    config = configparser.ConfigParser()
    config.read("config.ini")
    id = config["REDDIT"]["CLIENT_ID"]
    secret = config["REDDIT"]["CLIENT_SECRET"]

    return id, secret


def save_list(img_url_list):
    for img_url in img_url_list:
        file = open('img_links.txt', 'a')
        file.write('{} \n'.format(img_url))
        file.close()


def get_img_urls(sub, li):
    try:
        r = praw.Reddit(client_id=ClientInfo.id, client_secret=ClientInfo.secret, user_agent=ClientInfo.user_agent)
        submissions = r.subreddit(sub).hot(limit=li)

        return [submission.url for submission in submissions]

    except HTTPError:
        print("Too many Requests. Try again later!")
        time.sleep(400)
        return 0

    except ResponseException:
        print("Client info is wrong. Check again.")
        return 0


def download_img(img_url, img_title, filename):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    try:
        print('Downloading ' + img_title + '....')
        urllib.request.urlretrieve(img_url, filename)
        return 1

    except HTTPError as e:
        print("Too many Requests. Try again later!")
        return 0


def remove_wrong_format():
    loc = 'images/'
    for image in os.listdir(loc):
        if not image.endswith('.jpg'):
            os.remove(image)


if __name__ == '__main__':

    ClientInfo.id, ClientInfo.secret = get_client_info()

    subreddit = 'heavymind'
    num = int(input('Enter Limit: '))
    print()
    url_list = get_img_urls(subreddit, num)

    if url_list:

        save_list(url_list)

        for url in url_list:

            file_name = 'images/'
            # status = download_img(url, url.split('/')[-1], file_name+url.split('/')[-1])




