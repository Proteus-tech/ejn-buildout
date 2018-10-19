# -*- extra stuff goes here -*-

import plone.z3cform
import os

from plone.app.z3cform import templates


dir_path = os.path.dirname(os.path.realpath(__file__))
layout_path = dir_path + '/' + 'overrides/plone.app.z3cform.templates.layout.pt'

layout_factory_new = plone.z3cform.templates.ZopeTwoFormTemplateFactory(
    layout_path,
    form=plone.z3cform.interfaces.IFormWrapper,
    request=plone.app.z3cform.interfaces.IPloneFormLayer)

templates.layout_factory = layout_factory_new

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
