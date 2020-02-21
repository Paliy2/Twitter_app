import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
from web_map import create_map
from flask import Flask, render_template, request, redirect

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('title.html')


@app.route('/r', methods=['GET', 'POST'])
def parse_request():
    result = request.form['tweet_name']
    generated = 'Generate map'
    if result:
        main(result)
        generated = 'Map is generated. View map'
    return render_template('title.html', tweet_name=generated)


@app.route('/Map/')
def Map():
    return render_template('Map.html')


def main(name):
    while True:
        acct = name
        if (len(acct) < 1): break
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
        create_map(name_loc)
        return


if __name__ == '__main__':
    app.run(debug=True)
