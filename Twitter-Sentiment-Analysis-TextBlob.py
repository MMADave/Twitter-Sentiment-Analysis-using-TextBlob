# Queen's Master of Management Analytics - Text Analytics Project
# Natural Language Processing script using TextBlob
# Adapted from Stephen W. Thomas (Course instructor)
# MMADave Feb 2015

# The main package to help us with our text analysis
from textblob import TextBlob

# For reading input files in CSV format
import csv
import sys
# For doing cool regular expressions
import re
import time
# For sorting dictionaries
import operator

# Intialize an empty list to hold all of our tweets
tweets = []


# A helper function that removes all the non ASCII characters
# from the given string. Retuns a string with only ASCII characters.
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)



# LOAD AND CLEAN DATA

# Load in the input file and process each row at a time.
# We assume that the file has three columns:
# 0. The tweet text.
# 1. The tweet ID.
# 2. The tweet publish date
#
# We create a data structure for each tweet:
#
# id:       The ID of the tweet
# pubdate:  The publication date of the tweet
# orig:     The original, unpreprocessed string of characters
# clean:    The preprocessed string of characters
# TextBlob: The TextBlob object, created from the 'clean' string

with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader.next()
    for row in reader:

        tweet= dict()
        tweet['orig'] = row[2]
        tweet['id'] = int(row[0])
        tweet['pubdate'] = time.strftime('%Y/%m/%d', time.strptime(row[1],'%a %b %d %H:%M:%S +0000 %Y'))

        # Ignore retweets
        if re.match(r'^RT.*', tweet['orig']):
            continue

        tweet['clean'] = tweet['orig']

        # Remove all non-ascii characters
        tweet['clean'] = strip_non_ascii(tweet['clean'])

        # Remove URLS. (I stole this regex from the internet.)
        tweet['clean'] = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet['clean'])

        # Fix classic tweet lingo
        tweet['clean'] = re.sub(r'\bthats\b', 'that is', tweet['clean'])
        tweet['clean'] = re.sub(r'\bive\b', 'i have', tweet['clean'])
        tweet['clean'] = re.sub(r'\bim\b', 'i am', tweet['clean'])
        tweet['clean'] = re.sub(r'\bya\b', 'yeah', tweet['clean'])
        tweet['clean'] = re.sub(r'\bcant\b', 'can not', tweet['clean'])
        tweet['clean'] = re.sub(r'\bwont\b', 'will not', tweet['clean'])
        tweet['clean'] = re.sub(r'\bid\b', 'i would', tweet['clean'])
        tweet['clean'] = re.sub(r'wtf', 'what the fuck', tweet['clean'])
        tweet['clean'] = re.sub(r'\bwth\b', 'what the hell', tweet['clean'])
        tweet['clean'] = re.sub(r'\br\b', 'are', tweet['clean'])
        tweet['clean'] = re.sub(r'\bu\b', 'you', tweet['clean'])
        tweet['clean'] = re.sub(r'\bk\b', 'OK', tweet['clean'])
        tweet['clean'] = re.sub(r'\bsux\b', 'sucks', tweet['clean'])
        tweet['clean'] = re.sub(r'\bno+\b', 'no', tweet['clean'])
        tweet['clean'] = re.sub(r'\bcoo+\b', 'cool', tweet['clean'])
        tweet['clean'] = re.sub(r'\\n', ' ', tweet['clean'])
        tweet['clean'] = re.sub(r'\\r', ' ', tweet['clean'])
        tweet['clean'] = re.sub(r'&gt;', '', tweet['clean'])
        tweet['clean'] = re.sub(r'&amp;', 'and', tweet['clean'])
        tweet['clean'] = re.sub(r'\$ *hit', 'shit', tweet['clean'])
        tweet['clean'] = re.sub(r' w\/', 'with', tweet['clean'])
        tweet['clean'] = re.sub(r'\ddelay', '\d delay', tweet['clean'])

        # Create textblob object
        tweet['TextBlob'] = TextBlob(tweet['clean'])

        # Correct spelling (WARNING: SLOW)
        #tweet['TextBlob'] = tweet['TextBlob'].correct()

        tweets.append(tweet)



# sentiment analysis
print "id,Date,polarity,sentiment,count"
for tweet in tweets:
    tweet['polarity'] = float(tweet['TextBlob'].sentiment.polarity)
    tweet['subjectivity'] = float(tweet['TextBlob'].sentiment.subjectivity)

    if tweet['polarity'] >= 0.1:
        tweet['sentiment'] = 'positive'
    elif tweet['polarity'] <= -0.1:
        tweet['sentiment'] = 'negative'
    else:
        tweet['sentiment'] = 'neutral'
    print "%d,%s,%.2f,%s,1" % (tweet['id'],tweet['pubdate'],tweet['polarity'],tweet['sentiment'])
