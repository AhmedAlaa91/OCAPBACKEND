# coding: utf-8
"""
Django settings override for development environment
"""
# pylint: disable=wildcard-import,unused-wildcard-import
from __future__ import annotations

from .common import *

DEBUG = convert_str_bool(getenv('DJANGO_DEBUG'), True)


# Disable authentication
ORANGE_AUTH_API_BYPASS = True
