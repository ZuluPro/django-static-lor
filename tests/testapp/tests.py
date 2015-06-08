from mock import patch
from django.test import TestCase
from django.test.utils import override_settings
from lor.management.commands.wget import _ask_yes_no
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


class LogUrlTest(TestCase):
    @patch('lor.templatetags.lor.USE_LOCAL_URLS', True)
    def test_get_local_url(self):
        self.assertEqual(lor_url('testfile'), '/static/testfile.txt')

    @patch('lor.templatetags.lor.USE_LOCAL_URLS', False)
    def test_get_remote_url(self):
        self.assertEqual(lor_url('testfile'), '/textfile.txt')
