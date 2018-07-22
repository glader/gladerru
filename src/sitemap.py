from core.sitemap import sitemaps as core_sitemap
from mountains.sitemap import sitemaps as mountain_sitemap
from movies.sitemap import sitemaps as movies_sitemap

sitemaps = {}
sitemaps.update(mountain_sitemap)
sitemaps.update(movies_sitemap)
sitemaps.update(core_sitemap)
