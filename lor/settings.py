from django.conf import settings as se


FILES_URLS = {}
if hasattr(se, 'LOR_FILES_URLS'):
    FILES_URLS.update(se.LOR_FILES_URLS)

FILES = FILES_URLS.keys()

STATIC_DIR = se.LOG_STATIC_DIR if hasattr(se, 'LOG_STATIC_DIR') else None

USE_LOCAL_URLS = se.LOR_LOCAL_URLS if hasattr(se, 'LOR_LOCAL_URLS') else False
