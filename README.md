# SelfhostedIliasRssReader
Read the private Ilias RSS feed

<br>

## What does this Python 3 script?
It can be run as a cron job and checks then every execution if there are new entries in the RSS feed (primary target is the private feed of the Integrated Learning, Information and Work Cooperation System platform also known as ILIAS).

If desired it sends via the embedded gmail api submodule a email to your email address.

<br>

## How does it work

Set the script as a cron job on your server (tested on a Raspberry Pi with Raspbian).

Then edit the [`credentials.json`](credentials.json) file with your personal private URL, password and user name:

```json
{
    "url": "https://yourPrivateIliasUrlWithPasswordAndUsername",
    "password": "yourPassword",
    "username": "yourUsername",
    "recipients": ["yourEmailAddress"]
}
```

**If you want to send an email look into the Readme of the submodule and set `USE_GMAIL` true.**