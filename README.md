# inst_parser

This program can download all photo/video from profile instagram (if profile is open or u have access to it)

python 3.7.7

modules: os, json, time, glob, bs4, requests, selenium


You need to fill config.py:

    USERNAME = '<username instagram>'
    PASSWORD = '<password instagram>'
    PROFILE = r'<nickname of target profile>'
    BATCH_SIZE = 50 -> how many files to get in one request (max=50)
    NEW_COOKIE = True -> get cookies (need use once, then u can rewrite it to False)
    STORIES_DOWNLOAD = True -> True if u need download stories or False if don't
    MEDIA_DOWNLOAD = True -> True if u need download media or False if don't
