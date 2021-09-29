import requests
from dotenv import load_dotenv
import os
import praw

load_dotenv()

# only these 5 variables have to be set
HOST = os.getenv("WALLABAG_HOST")
USERNAME = os.getenv("WALLABAG_USERNAME")
PASSWORD = os.getenv("WALLABAG_PASSWORD")
CLIENTID = os.getenv("WALLABAG_CLIENTID")
SECRET = os.getenv("WALLABAG_SECRET")

gettoken = {'username': USERNAME, 'password': PASSWORD, 'client_id': CLIENTID, 'client_secret': SECRET, 'grant_type': 'password'}
r = requests.get('{}/oauth/v2/token'.format(HOST), gettoken)
access = r.json().get('access_token')

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENTID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent="wallabag syncer",
    username=os.getenv("REDDIT_USERNAME"),
)

saved_posts = reddit.user.me().saved()
links=[]
for post in saved_posts:
    reddit_link="https://www.reddit.com"+post.permalink
    links.append(reddit_link)
    try:
        link=post.url_overridden_by_dest
        links.append(link)
    except:
        pass
    post.unsave()

i=1
size=len(links)
for link in links:
    if "i.redd.it" in link:
        i+=1
        continue
    a = 0                       # should the article be already read? 0 or 1
    f = 0                       # should the article be added as favorited? 0 or 1
    print("Adding links: {}/{}".format(i,size))
    article = {'url': link, 'archive': a , 'starred': f, 'access_token': access}
    r = requests.post('{}/api/entries.json'.format(HOST), article)
    i+=1
