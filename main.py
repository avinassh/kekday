import praw
from flask import Flask
from flask import request, render_template
from prawoauth2 import PrawOAuth2Mini

from settings import (app_key, app_secret, access_token, refresh_token,
                      user_agent, scopes)

reddit_client = praw.Reddit(user_agent=user_agent)
oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key,
                              app_secret=app_secret,
                              access_token=access_token,
                              refresh_token=refresh_token, scopes=scopes)

app = Flask(__name__)


@app.route('/')
def index():
    username = request.values.get('username')
    if not username:
        return render_template('index.html')
    cakeday = get_cake_day(username)
    return render_template('result.html', redditor=username, cakeday=cakeday)

if __name__ == '__main__':
    app.run(debug=True)
