from plone.app.layout.viewlets.social import SocialTagsViewlet as BaseViewlet
from plone.namedfile.utils import get_contenttype


class SocialTagsViewlet(BaseViewlet):
    def update(self):
        image_field_name = 'image'
        super(SocialTagsViewlet, self).update()
        if hasattr(self.context, image_field_name):
            ogimage = next(
                (t for t in self.tags if t.get('property') == 'og:image'), None)
            ogimagetype = next(
                (t for t in self.tags if t.get('property') == 'og:image:type'), None)
            twitterimage = next(
                (t for t in self.tags if t.get('property') == 'twitter:image'), None)
            image = next(
                (t for t in self.tags if t.get('itemprop') == 'image'), None)

            image_url = '{base_url}/@@images/{fieldname}/{imagesize}'.format(
                base_url=self.context.absolute_url(),
                fieldname=image_field_name,
                imagesize='large')

            mimetype = get_contenttype(self.context.image)

            if ogimage:
                ogimage['content'] = image_url
            if ogimagetype:
                ogimagetype['content'] = mimetype
            if image:
                image['content'] = image_url
            if twitterimage:
                twitterimage['content'] = image_url
