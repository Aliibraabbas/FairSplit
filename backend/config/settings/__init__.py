"""
Django settings redirector for FairSplit project.

This file automatically imports the development settings.
For production, set DJANGO_SETTINGS_MODULE=config.settings.prod
"""

from .dev import *
