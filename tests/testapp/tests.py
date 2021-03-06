import os
from shutil import rmtree
from StringIO import StringIO
from mock import patch
from django.test import TestCase
from django.core.management import call_command
from django.conf import settings as se
from lor.management.commands.wget import _ask_yes_no, Command
from lor.templatetags.lor import lor_url


class AskYesOrNoTest(TestCase):
    @patch('__builtin__.raw_input', return_value='y')
    def test_answer_yes(self, raw_input):
        self.assertEqual(_ask_yes_no(''), True)

    @patch('__builtin__.raw_input', return_value='')
    def test_answer_yes_by_default(self, raw_input):
        self.assertEqual(_ask_yes_no(''), True)

    @patch('__builtin__.raw_input', return_value='n')
    def test_answer_no(self, raw_input):
        self.assertEqual(_ask_yes_no(''), False)


@patch('lor.templatetags.lor.USE_LOCAL_URLS', True)
class LogUrlLocalTest(TestCase):
    def test_local_url(self):
        self.assertEqual(lor_url('testfile'), '/static/testfile.txt')

    def test_local_url_is_none(self):
        self.assertEqual(lor_url('localisnone'), '')


@patch('lor.templatetags.lor.USE_LOCAL_URLS', False)
class LogUrlRemoteTest(TestCase):
    def test_remote_url(self):
        self.assertEqual(lor_url('testfile'), '/textfile.txt')

    def test_remote_url_is_none(self):
        self.assertEqual(lor_url('remoteisnone'), '')

    def test_no_remote_url(self):
        self.assertEqual(lor_url('noremote'), '')


CREATE_STATIC_DIR_URLS = {'testfile': ('txt/testfile.txt', '/textfile.txt')}


class BaseWgetTest(TestCase):
    # @patch('lor.management.commands.wget.STATIC_DIR', '/tmp/lor_test/')
    # @patch('lor.management.commands.wget.os.makedirs')
    # @patch('__builtin__.raw_input', return_value='y')
    # @patch('__builtin__.file')
    # @patch('lor.management.commands.wget.FILES_URLS', CREATE_STATIC_DIR_URLS)
    def setUp(self):
        try:
            rmtree(se.LOR_STATIC_DIR)
        except OSError:
            pass
    tearDown = setUp


class WgetCreateStaticDirectoryTest(BaseWgetTest):
    @patch('__builtin__.raw_input', return_value='')
    def test_create_static_directory_trueinput(self, *args):
        Command()._create_static_directory(False)
        self.assertTrue(os.path.exists(se.LOR_STATIC_DIR))

    @patch('__builtin__.raw_input', return_value='n')
    def test_create_static_directory_falseinput(self, *args):
        Command()._create_static_directory(False)
        self.assertFalse(os.path.exists(se.LOR_STATIC_DIR))

    def test_create_static_directory_noinput(self):
        Command()._create_static_directory(True)
        self.assertTrue(os.path.exists(se.LOR_STATIC_DIR))


CREATE_STATIC_DIR_URLS = {'testfile': ('testfile.txt', '/textfile.txt')}


class WgetCheckDestinationTest(TestCase):
    file_path = os.path.join(se.LOR_STATIC_DIR, 'testfile.txt')

    def setUp(self):
        try:
            os.makedirs(se.LOR_STATIC_DIR)
        except OSError:
            pass

    def tearDown(self):
        try:
            os.remove(self.file_path)
        except OSError:
            pass

    @patch('lor.management.commands.wget.FILES_URLS', CREATE_STATIC_DIR_URLS)
    def test_check_destination_exists_noinput(self, *args):
        open(self.file_path, 'a').close()
        isTrue = Command()._check_destination(True, self.file_path)
        self.assertFalse(isTrue)

    @patch('__builtin__.raw_input', return_value='')
    def test_check_destination_exists_input_yes(self, *args):
        open(self.file_path, 'a').close()
        isTrue = Command()._check_destination(False, self.file_path)
        self.assertTrue(isTrue)

    @patch('__builtin__.raw_input', return_value='n')
    def test_check_destination_exists_input_no(self, *args):
        open(self.file_path, 'a').close()
        isTrue = Command()._check_destination(False, self.file_path)
        self.assertFalse(isTrue)

    def test_check_destination_not_exists(self):
        isTrue = Command()._check_destination(True, self.file_path)
        self.assertTrue(isTrue)


class MockResponse(object):
    def __init__(self, resp_data, code=200, msg='OK'):
        self.resp_data = resp_data
        self.code = code
        self.msg = msg
        self.headers = {'content-type': 'text/xml; charset=utf-8'}

    def read(self):
        return self.resp_data

    def getcode(self):
        return self.code


class WgetGetRemoteFileTest(BaseWgetTest):
    @patch('lor.management.commands.wget.urllib2.urlopen', MockResponse)
    def test_get_url(self, *args):
        fd = Command()._get_remote_file('testfile.txt')
        self.assertIsNotNone(fd)

    def test_io_error(self, *args):
        fd = Command()._get_remote_file('http://localhost:65535/testfile.txt')
        self.assertIsNone(fd)

    @patch('lor.management.commands.wget.urllib2.urlopen')
    def test_get_url_404(self, *args):
        fd = Command()._get_remote_file('testfile.txt')
        self.assertIsNone(fd)


class WgetCreateLocalFileTest(BaseWgetTest):
    file_path = os.path.join(se.LOR_STATIC_DIR, 'testfile.txt')
    long_file_path = os.path.join(se.LOR_STATIC_DIR, 'txt/test/testfile.txt')

    def setUp(self):
        try:
            os.makedirs(se.LOR_STATIC_DIR)
        except OSError:
            pass
        self.response = StringIO('Test response')

    def tearDown(self):
        try:
            rmtree(se.LOR_STATIC_DIR)
        except OSError:
            pass

    def test_create_parent_dirs(self):
        Command()._create_local_file(self.response, self.long_file_path)

    def test_write_file(self):
        Command()._create_local_file(self.response, self.file_path)
