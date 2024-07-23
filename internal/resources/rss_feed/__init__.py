# Defining Constants
from internal.resources.rss_feed.rss import RSSFeed

BEFORE_DATE = "beforeDate"
AFTER_DATE = "afterDate"
STOCK_SYMBOL = "stockSymbol"
LANGUAGE = "language"
COUNTRY = "country"
TOPIC = "topic"
SEARCH_QUERY = "searchQuery"


# Defining RSSFeed class
def new_rss_feed(params):
    return RSSFeed(params)
