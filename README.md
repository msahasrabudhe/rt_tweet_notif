# rt_tweet_notif

An ad-hoc system to receive real-time tweets from a twitter account, and display
notifications on the screen. 

Does not require Twitter API or associating your account with Twitter Apps. 
Does not a Twitter require login. 

**Requirements**

Should work on Linux; tested on Ubuntu with Cinnamon desktop. Written in Python 2.7. Needs the libraries
* notify2
* urllib2
* HTMLParser
* cPickle

All these libraries are easily installable through `pip`.

Usage: 

```python
    python notify_rtt.py <twitter URL> [<delay>]
```

`<twitter URL>` specifies which twitter user to get notifications from. 
It should be the entire URL. For example, `http://twitter.com/ap`.

`<delay>` is an optional argument specifying how frequently to check for updates. 
The default value is 180 (every three minutes). Please keep this value high
in order to avoid unneessary requests to the servers.

Simply update the value of `HISTROOT` in `parse_tweets.py`, to point to a 
directory where you would like to store the tweet history, before executing
for the first time.

Example usage:

```python
    python notify_rtt.py http://twitter.com/google 300 &
```

This will start a background process that will query the official Twitter 
account of Google every five minutes, and display a new notification on the screen
if Google has sent a tweet in the last five minutes. 

**PS**: First-time queries to a new account (that does not already have history 
        in `HISTROOT`) causes the program to fetch the twenty
        most recent tweets, and hence you shall see twenty notifications on the screen.
        However, this can be easily avoided by modifying the code a little bit. 
        In particular, one can raise a flag if the history file doesn't already exist
        and avoid sending notifications if this flag is raised. 

**Implementation**

The program fetches the page source for the requested page every `<delay>` seconds. 
It then parses the source to check for new tweets (that always appear between two tags).
Notifications are sent using `notify2` to the user, which are set to never expire, 
but are equipped with a close button. This can be easily changed in `parse_tweets.py`. 
History is saved to avoid repeat notifications, so that notifications 
are sent only for new tweets.



