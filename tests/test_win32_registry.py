import unittest
import cwutil


class TestWin32Registry(unittest.TestCase):
    def test_get_win32_registry_value(self):
        NODE = r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        VALUE = 'PATH'
        path = cwutil.get_win32_registry_value(NODE, VALUE)
        self.assertTrue('%SYSTEMROOT%' in path)

    def test_get_win32_registry_value_error(self):
        NODE = r'HKEY_LOCAL_MACHINE\AAAA'
        VALUE = 'PATH'
        callable = lambda: cwutil.get_win32_registry_value(NODE, VALUE)
        self.assertRaises(cwutil.RegistryValueNotFount, callable)

    def test_get_win32_registry_hkey_invalid(self):
        NODE = r'HKEY_AAA\AAAA'
        VALUE = 'PATH'
        callable = lambda: cwutil.get_win32_registry_value(NODE, VALUE)
        self.assertRaises(cwutil.InvalidHKey, callable)

    def test_iter_win32_registry_node_values(self):
        NODE = r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        l = list(cwutil.iter_win32_registry_node_values(NODE))
        self.assertTrue(l > 0)

    def test_set_and_del_win32_registry_value(self):
        NODE = 'HKEY_CURRENT_USER\Software\CWasp\Test'
        VALUE = 'TestValue'
        l = cwutil.set_win32_registry_value(NODE, VALUE, "aaa")
        self.assertEqual(cwutil.get_win32_registry_value(NODE, VALUE), "aaa")
        cwutil.del_win32_registry_value(NODE, VALUE)
        callable = lambda: cwutil.get_win32_registry_value(NODE, VALUE)
        self.assertRaises(cwutil.RegistryValueNotFount, callable)

    def test_get_win32_registry_value_type(self):
        NODE = r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        VALUE = 'PATH'
        value_type = cwutil.get_win32_registry_value_type(NODE, VALUE)
        self.assertEqual(value_type, cwutil.RegistryValueType.REG_EXPAND_SZ)

if __name__ == '__main__':
    unittest.main()
