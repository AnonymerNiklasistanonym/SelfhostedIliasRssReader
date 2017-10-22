# -*- coding: utf-8 -*-

"""
Script that scrapes rss feed and sends updates via console or email.
If desired it sends emails to entered recipients over the SimplifiedGmailApi.
"""

import json
import logging
import os
import sys

import feedparser
import requests



# Setup the Gmail API - set USE_GMAIL False if you want to use the Simplified Gmail API
USE_GMAIL = True

if USE_GMAIL:
    # Gmail Imports (not important for the actual crawler)
    from SendGmailSimplified.SendGmailSimplified import SimplifiedGmailApi
    from premailer import transform

# Paths for important directories and files - from home directory
HOME_DIR = os.path.expanduser('~')

# change this to the directory your script is: !!!!!!!!!!!!!!!!!
DIR_OF_SCRIPT = os.path.join(HOME_DIR,
                             os.path.join("Documents", "SelfhostedIliasRssReader"))
# GitHubBeta/SelfhostedIliasRssReader

PATH_FOR_LOG = os.path.join(DIR_OF_SCRIPT, "script.log")
PATH_OF_DATA_FILE = os.path.join(DIR_OF_SCRIPT, 'data.json')
PATH_OF_CREDENTIALS_FILE = os.path.join(DIR_OF_SCRIPT, 'credentials.json')
PATH_OF_CSS_FILE = os.path.join(DIR_OF_SCRIPT, 'main.css')

logging.basicConfig(filename=PATH_FOR_LOG, level=logging.DEBUG)

if os.path.isfile(PATH_OF_CREDENTIALS_FILE):
    with open(PATH_OF_CREDENTIALS_FILE) as json_file:
        DATA = json.load(json_file)

        URL = DATA["url"]
        USER_NAME = DATA["username"]
        PASSWORD = DATA["password"]

        if USE_GMAIL:
            RECIPIENTS = DATA["recipients"]
else:
    print("No credentials and url was found")
    sys.exit()

# Get current RSS content
CONTENT = requests.get(URL, auth=(USER_NAME, PASSWORD))

# Parse RSS content
PARSED_CONTENT = feedparser.parse(CONTENT.content)

if os.path.isfile(PATH_OF_DATA_FILE):
    with open(PATH_OF_DATA_FILE) as json_file:
        DATA = json.load(json_file)

        LATEST_DATE = DATA['date']

        print("Date of last update: " + DATA['date'])
        print("Current date of newest entry: " +
              PARSED_CONTENT['entries'][0]['published'])

        if DATA['date'] == PARSED_CONTENT['entries'][0]['published']:
            print("no new articles")
            sys.exit()
else:
    LATEST_DATE = "no date"

with open(PATH_OF_DATA_FILE, 'w') as outfile:
    json.dump({"date": PARSED_CONTENT['entries'][0]['published']}, outfile)

print("latest date: " + LATEST_DATE)

WALKING_RSS_STRING = "<h1>New Ilias RSS Entries:</h1>"

for entry in PARSED_CONTENT['entries']:

    print("current date: " + entry['published'])
    if LATEST_DATE == entry['published']:
        print("Newest entry detected!!!")
        break
    WALKING_RSS_STRING += '<div class="entry"><div class="size"><p class="title">' + \
        entry['title'] + '</p><p class="date">' + \
        entry['published'] + "</p></div>"
    WALKING_RSS_STRING += '<p class="content">' + \
        entry['summary_detail']['value'] + '</p>'
    WALKING_RSS_STRING += '<a href="' + \
        entry['link'] + \
        '"><button class="link-button">Link to content</button></a></div>'

print(WALKING_RSS_STRING)

if USE_GMAIL:
    with open(PATH_OF_CSS_FILE, 'r') as cssfile:
        CSS_DATA = cssfile.read().rstrip("\n")

    EMAIL_TEXT = ('<!DOCTYPE html><html><head><style type="text/css">' + CSS_DATA +
                  "</style></head><body>" + WALKING_RSS_STRING + "</body></html>")

    EMAIL_TEXT = transform(EMAIL_TEXT).replace("\n", "")

    DIR_OF_GMAIL_API_FILES = os.path.join(DIR_OF_SCRIPT,
                                          os.path.join("SendGmailSimplified",
                                                       "gmail_api_files"))
    PATH_OF_CLIENT_DATA = os.path.join(
        DIR_OF_GMAIL_API_FILES, "client_data.json")
    PATH_OF_CLIENT_SECRET = os.path.join(
        DIR_OF_GMAIL_API_FILES, "client_secret.json")
    GMAIL_SERVER = SimplifiedGmailApi(PATH_OF_CLIENT_DATA,
                                      PATH_OF_CLIENT_SECRET,
                                      DIR_OF_GMAIL_API_FILES)

    for recipient in RECIPIENTS:
        GMAIL_SERVER.send_html(
            recipient, "Ilias RSS Update", EMAIL_TEXT)


if USE_GMAIL:
    with open("aha.html", 'w') as outfile:
        with open(PATH_OF_CSS_FILE, 'r') as cssfile:
            CSS_DATA = cssfile.read().rstrip("\n")

        EMAIL_TEXT = ('<!DOCTYPE html><html><head><style type="text/css">' + CSS_DATA +
                    "</style></head><body>" + WALKING_RSS_STRING + "</body></html>")

        EMAIL_TEXT = transform(EMAIL_TEXT).replace("\n", "")
        outfile.write(EMAIL_TEXT)
