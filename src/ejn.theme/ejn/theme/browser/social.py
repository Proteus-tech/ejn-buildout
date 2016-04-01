from plone.app.layout.viewlets.social import SocialTagsViewlet as BaseViewlet
from plone.namedfile.utils import get_contenttype


class SocialTagsViewlet(BaseViewlet):
    _image_field_name = 'image'
    _image_size = 'large'

    @property
    def image_url(self):
        return '{base_url}/@@images/{fieldname}/{imagesize}'.format(
            base_url=self.context.absolute_url(),
            fieldname=self._image_field_name,
            imagesize=self._image_size)

    def twitter_metatags(self):
        for t in self.tags:
            if t.get('name') == 'twitter:image':
                t['content'] = self.image_url
            elif t.get('name') == 'twitter:card':
                t['content'] = 'summary_large_image'

    def facebook_metatags(self):
        mimetype = get_contenttype(self.context.image)
        for t in self.tags:
            if t.get('property') == 'og:image':
                t['content'] = self.image_url
            elif t.get('property') == 'og:image:type':
                t['content'] = mimetype

    def googleplus_metatags(self):
        for t in self.tags:
            if t.get('itemprop') == 'image':
                t['content'] = self.image_url

    def update(self):
        super(SocialTagsViewlet, self).update()
        if hasattr(self.context, self._image_field_name):
            self.twitter_metatags()
            self.facebook_metatags()
            self.googleplus_metatags()
