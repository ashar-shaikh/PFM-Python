from datetime import datetime
from urllib.parse import urlencode
import requests
import feedparser
import internal.resources.rss_feed as rss
import re
from bs4 import BeautifulSoup
from datetime import datetime
from time import mktime


class RSSFeed:
    base_url = "https://www.brecorder.com/feeds/latest-news?"

    def __init__(self):
        self.params = {}

    def build_url(self):
        return self.base_url

    def fetch_feed(self):
        url = self.build_url()
        response = requests.get(url)
        feed_data = feedparser.parse(response.content)

        return feed_data

    def parse_feed(self, feed):
        articles = []
        for entry in feed.entries:
            article = {
                'id': entry.id if 'id' in entry else entry.guid if 'guid' in entry else None,
                'title': entry.title if 'title' in entry else 'Unknown',
                'link': entry.link if 'link' in entry else 'Unknown',
                'description': self.clean_description(entry.description) if 'description' in entry else 'Unknown',
                'published': datetime.fromtimestamp(mktime(entry.published_parsed)) if
                'published_parsed' in entry else 'Unknown'
            }
            articles.append(article)
        return articles

    def clean_description(self, description):
        cleaner = re.compile('<.*?>')
        cleantext = re.sub(cleaner, '', description)
        return cleantext

    def extract_link_from_description(self, description):
        soup = BeautifulSoup(description, 'html.parser')
        a_tag = soup.find('a', href=True)
        if a_tag:
            return a_tag['href']
        return None

    def fetch_results(self):
        feed = self.fetch_feed()
        if not feed:
            return None, 0
        articles = self.parse_feed(feed)
        count = len(articles)
        return articles, count
