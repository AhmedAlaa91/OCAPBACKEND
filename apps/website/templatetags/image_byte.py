import os
from base64 import b64encode

from django import template

register = template.Library()  # noqa


@register.filter  # noqa
def bin_2_img(_bin):  # noqa
    try:
        if _bin:  # noqa
            return b64encode(_bin.read()).decode("utf-8")  # noqa
        else:
            return _bin
    except:
        return _bin
