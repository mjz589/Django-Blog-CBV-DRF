from django.contrib.sitemaps import Sitemap
from portfolio.models import Portfolio
from django.urls import reverse


class portfolioitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Portfolio.objects.filter(publish_status=True)

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, item):
        return reverse("portfolio:single", kwargs={"pid": item.id})
