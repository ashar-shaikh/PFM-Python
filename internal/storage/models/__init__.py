from internal.storage.models.generic.base import Base
from internal.storage.models.generic.background_tasks import BackgroundTasks
from internal.storage.models.assets.stocks import Stocks
from internal.storage.models.assets.assets import Assets
from internal.storage.models.news.rss_feeds import RSSFeeds
from internal.storage.models.news.news_content import NewsContent
from internal.storage.models.news.content_analysis import ContentAnalysis

# Expose the models
news_models = [RSSFeeds, NewsContent, ContentAnalysis]
asset_models = [Stocks, Assets]
generic_models = [Base, BackgroundTasks]
__all__ = generic_models + news_models + asset_models
