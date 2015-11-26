from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.browser.sitemap import SitemapView as Base


class SitemapView(Base):

    item_template = ViewPageTemplateFile('sitemap-item.pt')
