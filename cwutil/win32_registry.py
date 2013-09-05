import _winreg
import exceptions

CORE_NAMES = {
    "HKEY_CLASSES_ROOT": _winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_CONFIG": _winreg.HKEY_CURRENT_CONFIG,
    "HKEY_CURRENT_USER": _winreg.HKEY_CURRENT_USER,
    "HKEY_DYN_DATA": _winreg.HKEY_DYN_DATA,
    "HKEY_LOCAL_MACHINE": _winreg.HKEY_LOCAL_MACHINE,
    "HKEY_PERFORMANCE_DATA": _winreg.HKEY_PERFORMANCE_DATA,
    "HKEY_USERS": _winreg.HKEY_USERS,
}


class RegistryValueNotFount(Exception):
    pass


class InvalidHKey(Exception):
    pass


def _get_real_node(node):
    node = node.replace("/", "\\")
    hkey = node.split("\\")[0].upper()
    if CORE_NAMES.has_key(hkey):
        hkey = CORE_NAMES[hkey]
    else:
        raise InvalidHKey(hkey)
    return hkey, "\\".join(node.split("\\")[1:])


def get_value(node, value):
    try:
        key, node = _get_real_node(node)
        key = _winreg.OpenKey(key, node, 0, _winreg.KEY_READ)
        return str(_winreg.QueryValueEx(key, value)[0])
    except exceptions.WindowsError as e:
        if e.errno == 2:
            raise RegistryValueNotFount(node, value)
        else:
            raise


def iter_node_values(node):
    key, node = _get_real_node(node)
    key = _winreg.OpenKey(key, node, 0, _winreg.KEY_READ)
    index = 0
    while True:
        try:
            name, value, type = _winreg.EnumValue(key, index)
            yield name, value
            index += 1
        except exceptions.WindowsError:
            break


