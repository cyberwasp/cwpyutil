import unittest
import cwutil


class TestWin32Registry(unittest.TestCase):
    def test_get_win32_hklm_registry_value(self):
        NODE = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        VALUE = 'PATH'
        path = cwutil.get_win32_hklm_registry_value(NODE, VALUE)
        self.assertTrue('%SYSTEMROOT%' in path)

    def test_get_win32_hklm_registry_value_error(self):
        NODE = r'AAAA'
        VALUE = 'PATH'
        callable = lambda: cwutil.get_win32_hklm_registry_value(NODE, VALUE)
        self.assertRaises(cwutil.RegistryValueNotFount, callable)


if __name__ == '__main__':
    unittest.main()
