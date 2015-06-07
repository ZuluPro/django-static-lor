from __future__ import absolute_import

import warnings
from django import template
from lor.settings import FILES_URLS
from django.conf import settings as se

register = template.Library()


@register.simple_tag
def lor_url(file_name):
    if file_name not in FILES_URLS:
        warnings.warn("'%s' not found." % file_name)
        return ''
    file_matches = FILES_URLS[file_name]
    if se.DEBUG or se.DEBUG_TEMPLATE:
        return file_matches[0]
    elif len(file_matches) == 1 or not file_matches[1]:
        return file_matches[1]
    else:
        warnings.warn("No local '%s' found.")
        return ''
