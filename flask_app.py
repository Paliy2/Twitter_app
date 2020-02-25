import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import os

from web_map import create_map
from flask import Flask, render_template, request, redirect, make_response
from functools import update_wrapper, wraps
from datetime import datetime

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def find_number(directory):
    '''
    str -> int
    list directory for Map.html files and get the number of last created file
    '''
    arr = os.listdir(directory)
    max_num = 0
    for item in arr:
        if item[3].isdigit():
            if int(item[3]) > max_num:
                max_num = int(item[3])
    return max_num


global number
number = find_number('/home/yewgen/mysite/templates')

app = Flask(__name__)


# disable cashe - despite doesn't help
def no_cache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache,\
        must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route('/')
def index():
    return render_template('title.html')


@app.route('/r', methods=['GET', 'POST'])
@no_cache
def parse_request():
    result = request.form['tweet_name']
    generated = 'Generate map'

    response = make_response(render_template('title.html',
                                             tweet_name=generated))
    if result:
        global number
        if number >= 10:
            number = 0

        main(result)

        generated = 'Map has been generated.\n View map'

        response = make_response(render_template('title.html',
                                                 tweet_name=generated))

    return response


@app.route('/Map/')
@no_cache
def Map():
    global number
    return render_template('Map{}.html'.format(number - 1))


def main(name):
    '''
    str -> int
    Fuction takes the name of Twitter account you want to view
    Then it takes all needed data(name and location)
    and generates a web map based on this data
    Function also counts a number of created files
    and returns the number from 0 to 9 that should be considered
    during map generation
    '''
    global number
    while True:
        acct = name
        if (len(acct) < 1):
            break
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '15'})
        # print('Retrieving', url)
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        js = json.loads(data)
        users = js['users']

        name_loc = {}
        for user in users:
            name = user['name']
            location = user['location']
            print(name, location)
            name_loc[name] = location
        # print(name_loc)
        create_map(name_loc, 'templates/Map{}.html'.format(number))
        number += 1
        if number >= 10:
            for i in range(number - 1):
                os.system('rm \
                /home/yewgen/mysite/templates/Map{}.html'.format(i))
        return number


if __name__ == '__main__':
    app.run(debug=True)
