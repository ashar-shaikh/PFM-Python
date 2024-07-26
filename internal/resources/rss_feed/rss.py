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

    def __init__(self, params):
        self.params = params

    def build_url(self):
        # Initialize query parameters
        query_params = {}

        # Handle StockSymbol (Assuming OR logic for multiple symbols)
        if rss.STOCK_SYMBOL in self.params:
            stock_symbols_query = ' OR '.join(self.params[rss.STOCK_SYMBOL])
            if len(stock_symbols_query) > 4 and stock_symbols_query[:4] == ' OR ':
                stock_symbols_query = stock_symbols_query[4:]
            query_params['q'] = "(" + stock_symbols_query + ")"

        if rss.SEARCH_QUERY in self.params:
            if len(query_params['q']) > 1:
                query_params['q'] += ' AND ' + self.params[rss.SEARCH_QUERY]
            else:
                query_params['q'] = self.params[rss.SEARCH_QUERY]
        # Handle date range
        date_query = []
        if rss.AFTER_DATE in self.params:
            after_date = self.params[rss.AFTER_DATE]
            date_query.append(f'after:{after_date}')
        if rss.BEFORE_DATE in self.params:
            before_date = self.params[rss.BEFORE_DATE]
            date_query.append(f'before:{before_date}')
        if date_query:
            if 'q' in query_params:
                query_params['q'] += ' ' + ' '.join(date_query)
            else:
                query_params['q'] = ' '.join(date_query)

        if rss.COUNTRY in self.params:
            query_params['ceid'] = self.params[rss.COUNTRY]

        # Handle language
        if rss.LANGUAGE in self.params:
            query_params['hl'] = self.params[rss.LANGUAGE]

        # Encode query parameters
        query_string = urlencode(query_params)

        # Construct full URL
        full_url = self.base_url + query_string

        return full_url

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
