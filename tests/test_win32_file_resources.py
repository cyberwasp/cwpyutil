import os
import unittest
import sys
import cwutil

test_file = os.path.expandvars('$WINDIR\\System32\\Python%d%d.dll') % sys.version_info[:2]

class TestWin32FileResources(unittest.TestCase):

    def test_get_win32_file_description(self):
        description = cwutil.get_win32_file_description(test_file)
        self.assertEqual('Python Core', description)

    def test_get_win32_product_version(self):
        version = cwutil.get_win32_product_version(test_file)
        self.assertEqual('%d.%d.%d' % sys.version_info[:3], version)

    def test_get_win32_file_version(self):
        version = cwutil.get_win32_file_version(test_file)
        self.assertEqual('%d.%d.%d' % sys.version_info[:3], version)


if __name__ == '__main__':
    unittest.main()
