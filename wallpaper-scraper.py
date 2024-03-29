#!/bin/python3
import getpass
import os
import sys
from datetime import date
from urllib.error import HTTPError

import praw
import wget

directory = "."

if len(sys.argv) > 1:
    directory = sys.argv[1]
    print

directory += f"/{str(date.today())}"

id_secret = [x.replace("\n", "") for x in open(os.path.expanduser("~/.cache/wallpaper-scraper-keys"), "r").readlines()]

reddit = praw.Reddit(
    client_id=id_secret[0],
    client_secret=id_secret[1],
    user_agent="wallpaper-scraper",
    username=input("Reddit Username: "),
    password=getpass.getpass(prompt="Reddit Password: ",))

try:
    os.mkdir(directory)
except:
    pass

subreddit = reddit.subreddit("wallpapers")
os.chdir(directory)
for post in subreddit.top("week", limit=20):
    if "/r/wallpapers" not in post.url:
        print(post.title, "\n", post.url)
        filename: str = (post.title + post.url[-4:]).replace("/", ".")
        try:
            wget.download(post.url, filename)
            print("\n")
        except HTTPError as e:
            print(f"HTTP Error {e.code}.")
