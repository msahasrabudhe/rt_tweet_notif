# rt_tweet_notif

An ad-hoc system to receive real-time tweets from a twitter account, and display
notifications on the screen. 

Does not require Twitter API or associating your account with Twitter Apps. 
Does not require login. 

**Requirements**

Should work on Linux; tested on Ubuntu. Written in Python 2.7. Needs the libraries
* notify2
* urllib2
* HTMLParser
* cPickle

All these libraries are easily installable through `pip.`
Usage: 
'''
    python notify_rtt.py <twitter URL> [<delay>]
'''
`<twitter URL>` specifies which twitter user to get notifications from. 
`<delay>` is an optional argument specifying how frequently to check for updates. 
The default value is 180 (every three minutes). Please keep this value low
in order to avoid unneessary requests to the servers.

Simply update the value of HISTROOT in parse_tweets.py, to point to a 
directory where you would like to store the tweet history before executing. 

**Implementation**

The program fetches the page source for the requested page every `<delay>` seconds. 
It then parses the source to check for new tweets (that always appear between two tags).
Notifications are sent using `notify2` to the user, which are set to never expire, 
but are equipped with a close button. This can be easily changed in `parse_tweets.py`. 
History is saved to avoid repeat notifications, so that notifications 
are sent only for new tweets.



