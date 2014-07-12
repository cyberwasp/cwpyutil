import ctypes
import os
import tempfile
import unittest
import cwutil


class TestWhoLockFile(unittest.TestCase):
    def test_who_lock_file_open(self):
        fn = tempfile.mktemp()
        with open(fn, 'w') as f:
            f.write('asdfasd')
            res = list(cwutil.who_lock_file(fn))
            self.assertTrue(len(res) == 1)
            self.assertTrue('python.exe' in res[0].exe())
        os.remove(fn)

    def test_who_lock_file_load(self):
        dll_name = os.path.expandvars('$WinDir\System32\wscript.exe')
        ctypes.CDLL(dll_name)
        res = cwutil.who_lock_file(os.path.basename(dll_name))
        self.assertIn('python.exe', [os.path.basename(item.exe()).lower() for item in res])


if __name__ == '__main__':
    unittest.main()
