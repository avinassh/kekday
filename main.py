import praw
import humanize
from datetime import datetime
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


def get_cake_day(username):
    redditor = reddit_client.get_redditor(username)
    try:
        created_on = datetime.utcfromtimestamp(redditor.created_utc)
    except praw.errors.NotFound:
        return False
    return(humanize.naturalday(created_on))


@app.route('/')
def index():
    error_message = 'Redditor does not exist or Shadowbanned'
    username = request.values.get('username')
    if not username:
        return render_template('index.html')
    cakeday = get_cake_day(username)
    if cakeday:
        return render_template('result.html', username=username,
                               cakeday=cakeday)
    return render_template('index.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
