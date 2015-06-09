=================
Django Static LoR
=================

LoR as "Local or Remote" is a useful tool for manage static files between
testing and production.

Install
=======

Install the package on your system: ::

    pip install django-static-lor

Make the following things in your ``settings.py``:

* Add ``lor`` app at the beginning of your ``INSTALLED_APPS``
* Add ``LOR_USE_LOCAL_URLS`` for define if you want local or remote URLs
  (Better is simply ``LOR_USE_LOCAL_URLS = DEBUG``
* Add ``LOR_STATIC_DIR`` for define where is the app's static directory
* Add ``LOR_STATIC_DIR`` in ``STATICFILES_DIRS`` if you want to serve it when ``DEBUG == False``
* Add you matches in ``LOR_FILES_URLS``

Your settings will look like something like this: ::

    INSTALLED_APPS = (
          'lor',
          ...
    )
    LOR_USE_LOCAL_URLS = False
    LOR_STATIC_DIR = '/my/lor/static/dir/'
    STATICFILES_DIRS = (
        ...
        LOR_STATIC_DIR,
    )

    LOR_FILES_URLS = {
        'jquery': ('js/jquery.js',
            'https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js')
    }

Done!

Usage
=====

In templates
------------

::

    {% load lor %}
    My jQuery URL: {% lor_url 'jquery' %}
    
    
Collect remote files
--------------------

::

  ./manage.py wget

This will download all files in ``LOR_FILES_URLS`` and put them in ``LOR_USE_LOCAL_URLS``.
