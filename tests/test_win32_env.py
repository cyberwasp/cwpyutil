import unittest
from unittest.case import skipIf
import cwutil



class TestWin32Env(unittest.TestCase):

    def test_get_win32_all_user_env(self):
        path = cwutil.get_win32_all_user_env('PATH', False)
        self.assertTrue('%SYSTEMROOT%' in path)
        path = cwutil.get_win32_all_user_env('PATH')
        self.assertFalse('%SYSTEMROOT%' in path)

    @skipIf(not cwutil.win32_is_user_an_admin(), "not run with administrative priveleges")
    def test_set_del_win32_all_user_env(self):
        cwutil.set_win32_all_user_env('AAA', 'BBB')
        value = cwutil.get_win32_all_user_env('AAA')
        self.assertEqual('BBB', value)
        cwutil.del_win32_all_user_env('AAA')
