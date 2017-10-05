#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2
import notify2
from HTMLParser import HTMLParser
import cPickle as pickle

HISTROOT = '/home/dokania/.tw_hist'

# A class that helps us parse tweets. 
class TweetParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tw = ''
        self.in_tweet = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_tweet = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_tweet = False

    def handle_data(self, data):
        if self.in_tweet:
            self.tw += data

# Retrieve the first tweet between stag and etag. 
def get_tag_data(p_source, stag, etag):
    nchars_tag = len(stag)

    # Find the first occurrence of stag in p_source. 
    tpos = p_source.find(stag)

    # If nothing is found, return None. 
    if tpos == -1:
        return None

    # We want the part of the page source till the end tag. 
    epos = p_source[tpos:].find(etag)

    # Return the tweet in HTML, as well as the new position
    #    where to reset our page source. 
    return p_source[tpos+nchars_tag:tpos+epos], tpos+epos 

# Handler to add a close button to the notifications. 
def close_notif(notif_obj, action):
    notif_obj.close()

# Handler to add a button to open the twitter feed in browser. 
def open_account_firefox(notif_obj, action, feed):
    ff = os.popen('firefox %s 2> /dev/null &' %(feed))

def parse_feed(feed):
    # Remove trailing '/' from feed.
    while feed[-1] == '/':
        feed = feed[:-1]

    # Userhandle of user. 
    tw_userhandle = feed.split('/')[-1]
    tw_hist       = HISTROOT + '/' + tw_userhandle + '_history.pkl'

    # Load previous tweets. 
    if not os.path.exists(tw_hist):
        # We are seeing this user for the first time. 
        tw_file    = open(tw_hist, 'w')
        tw_file.close()
        n_tweets   = 0
        f_tweet    = -1
        prv_tweets = {}
    else:
        # We have seen this user before. 
        tw_file    = open(tw_hist, 'r')
        prv_tweets = pickle.load(tw_file)
        tw_file.close()
        n_tweets   = len(prv_tweets.keys())
        f_tweet    = prv_tweets.keys()[-1] if n_tweets > 0 else -1
    
    # Open handle to retrieve tweets. 
    try:
        tw_handle = urllib2.urlopen(feed)
    except:
        print 'Unable to connect to %s right now.' %(feed) 
        return

    # No errors.
    p_source  = tw_handle.read()

    # Close connection. 
    tw_handle.close()

    # Retrieve the account name, to title our notifications properly.
    account_name = get_tag_data(p_source, '<title>', '</title>')
    # Get the account name, but exclude " | Twitter" from it. 
    account_name = account_name[0].split('|')[0].strip()

    # Tags to look for. 
    stag = '<div class="js-tweet-text-container">'
    etag = '</div>'

    # New tweets. 
    new_tweets = []

    while True:
        next_tweet = get_tag_data(p_source, stag, etag)

        # If there are no more occurrences of this tag, we
        #    do not have any more tweets. 
        if next_tweet is None:
            break

        this_tweet = next_tweet[0]
        next_pos   = next_tweet[1]

        # Initialise the parser. 
        parser = TweetParser()

        # Feed the tweet to the parser. 
        parser.feed(this_tweet)

        # Check if this tweet already exists. 
        # If so, we need not scan any further. 
        if n_tweets > 0 and prv_tweets[f_tweet] == parser.tw:
            break

        # parser.tw now contains the new tweet. 
        new_tweets += [parser.tw]

        # Advance p_source
        p_source = p_source[next_pos:]


    # Now add these new tweets to our history. 

    # However, if there are no new ones, we need not do anything. 
    if len(new_tweets) == 0:
        return 

    # For notifications. 
    notifs = []
    notify2.init('Tw updates')

    # We read the tweets in reverse chronological order. So, we must add them 
    #    to our dictionary in the reverse order.
    for tw in new_tweets[::-1]:
        f_tweet = f_tweet + 1
        prv_tweets[f_tweet] = tw

        # Create a notification. 
        notifs   += [notify2.Notification(account_name, tw, 'Update from @'+tw_userhandle)]
        tw_notif  = notifs[-1]

        # Set timeout of one minute. 
        tw_notif.set_timeout(60000)                 # Sixty-thousand milliseconds. 
        # Set low urgency.
        tw_notif.set_urgency(notify2.URGENCY_LOW)
        # Add button to close it. 
        tw_notif.add_action('action_close', 'Close', close_notif)
        # Add button to open twitter account page in Firefox
        tw_notif.add_action('open_tw_account', 'Open in Firefox', open_account_firefox, user_data=feed)
        # Show the notification
        tw_notif.show()

    # Finally, write the dictionary prv_tweets back to file. 
    with open(tw_hist, 'w') as tw_file:
        tw_file.write(pickle.dumps(prv_tweets))

    # Fin.
    return
