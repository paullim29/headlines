import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib.parse
import urllib3
from urllib.request import urlopen

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
'cnn': 'http://rss.cnn.com/rss/edition.rss',
'fox': 'http://feeds.foxnews.com/foxnews/latest',
'iol': 'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")
#@app.route("/<publication>")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    print ("get weather")
    weather = get_weather("London,UK")
    print (weather)
    #first_article = feed['entries'][0]
    return render_template("home.html", articles=feed['entries'], weather=weather)

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=eb91fdef8cce9faf368bcace95c3daa8"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    #data = urllib3.urlopen(url).read()
    #url = "url"
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"],
                    "temperature":parsed["main"]["temp"],
                    "city":parsed["name"]
                }
    return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)