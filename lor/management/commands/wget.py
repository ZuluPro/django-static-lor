import os
import urllib2
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as se
from lor.settings import FILES, FILES_URLS


def _ask_yes_no(prompt_text):
    res = raw_input("%s [Y/n]: " % prompt_text)
    return not res.lower().startswith('n')


class Command(BaseCommand):
    help = 'Download defined static files'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--noinput', action='store_true')
        # parser.add_argument('-o', '--noinput', action='store_true')
        # parser.add_argument('-f', '--files')

    def handle(self, *args, **opts):
        noinput = opts.get('noinput', False)
        # Create static dir
        if not os.path.exists(se.LOR_STATIC_DIR):
            if noinput or _ask_yes_no('Create %s' % se.LOR_STATIC_DIR):
                os.makedirs(se.LOR_STATIC_DIR)
                self.stdout.write('Created %s' % se.LOR_STATIC_DIR)
        # Check if files
        if not FILES:
            self.stdout.write("No file defined.")
        for static in FILES:
            url = FILES_URLS[static][1]
            file_path = os.path.join(se.LOR_STATIC_DIR + FILES_URLS[static][0])
            dir_path = os.path.dirname(file_path)
            # Check if destination is writable
            if os.path.exists(file_path):
                if not noinput and not _ask_yes_no('Overwrite %s' % file_path):
                    continue
                elif noinput:
                    self.stdout.write("No create %s" % file_path)
                    continue
            # Get file from url
            try:
                res = urllib2.urlopen(url)
                if res.code != 200:
                    msg = "Can't get '%s' (%i)" % (url, res.code)
                    self.stderr.write(msg)
                    continue
            except IOError:
                self.stderr.write("Can't get '%s'" % url)
                continue
            # Write
            # Create subdirs if not exists
            if not os.path.exists(dir_path):
                os.makedirs(os.path.dirname(file_path))
            # Create static file
            with open(file_path, 'wb') as fd:
                fd.write(res.read())
                self.stdout.write('Created %s' % file_path)
