import _winreg
import exceptions


class RegistryValueNotFount(Exception):
    pass


def get_win32_hklm_registry_value(node, value):
    try:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, node, 0, _winreg.KEY_READ)
        return str(_winreg.QueryValueEx(key, value)[0])
    except exceptions.WindowsError as e:
        if e.errno == 2:
            raise RegistryValueNotFount('HKEY_LOCAL_MACHINE', node, value)
        else:
            raise