from django.conf import settings as se


def _make_googleapi_url(suffix):
    return 'https://ajax.googleapis.com/ajax/libs/' + suffix

FILES_URLS = {
    'jquery': ('/static/js/jquery.js',
               _make_googleapi_url('jquery/1.11.3/jquery.min.js')),
    'angularjs': ('/static/js/angularjs.js',
                  _make_googleapi_url('angularjs/1.3.15/angular.min.js')),
}
if hasattr(se, 'LOR_FILES_URLS'):
    FILES_URLS.update(se.LOR_FILES_URLS)
