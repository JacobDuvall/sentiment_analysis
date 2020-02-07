# pip install tweepy --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org

#TODO: Drop this info into table
# https://pythonprogramming.net/twitter-stream-sentiment-analysis-python/

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time

ckey = "ui5q58rlnjLIzolSsCQdxsNyy"
csecret = "QYl8n7Iww9JVUHXm7N0BlGZowcpuWlo8SbvLtT4MgTsiGos8cM"
atoken = "1178665586278174721-Zhm3e9rO8s4HAq7N8jRmjOyuK7QUrj"
asecret = "3Fwp3vqIwnjJA6v6Fjpahof3szIclfekWm0ACQJY5XjDS"

def sentiment1(analyzer, tweet):
    vs = analyzer.polarity_scores(tweet)
    sentiment = vs['compound']
    return sentiment

def twitter_process(phrase):

    analyzer = SentimentIntensityAnalyzer()

    class listener(StreamListener):

        def on_status(self, status):
            if hasattr(status, 'retweeted_status'):
                try:
                    created_at = status.created_at
                    tweet = unidecode(status.retweeted_status.extended_tweet["full_text"])
                    sentiment = sentiment1(analyzer, tweet)
                    print(created_at, '\n', tweet, '\n', sentiment)
                except:
                    created_at = status.created_at
                    tweet = unidecode(status.retweeted_status.text)
                    sentiment1(analyzer, tweet)
            else:
                try:
                    created_at = status.created_at
                    tweet = unidecode(status.extended_tweet["full_text"])
                    sentiment1(analyzer, tweet)
                except AttributeError:
                    created_at = status.created_at
                    tweet = unidecode(status.text)
                    sentiment1(analyzer, tweet)

    while True:

        try:
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            twitterStream = Stream(auth, listener(), verify=False)
            twitterStream.filter(track=phrase)
        except Exception as e:
            print(str(e))
            time.sleep(5)


def entry():
        twitter_process(['a', 'e', 'i', 'o', 'u'])

if __name__ == "__main__":
    entry()
