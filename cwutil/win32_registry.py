import sys


if sys.version_info.major == 2:
    import _winreg as winreg
    from exceptions import WindowsError
else:
    import winreg

CORE_NAMES = {
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKEY_DYN_DATA": winreg.HKEY_DYN_DATA,
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
    "HKEY_USERS": winreg.HKEY_USERS,
}


class ValueType:
    REG_SZ = winreg.REG_SZ
    REG_EXPAND_SZ = winreg.REG_EXPAND_SZ


class RegistryValueNotFount(Exception):
    pass


class InvalidHKey(Exception):
    pass


def _get_real_node(node):
    node = node.replace("/", "\\")
    hkey = node.split("\\")[0].upper()
    if hkey in CORE_NAMES:
        hkey = CORE_NAMES[hkey]
    else:
        raise InvalidHKey(hkey)
    return hkey, "\\".join(node.split("\\")[1:])


def query_value(node, value):
    try:
        key, node = _get_real_node(node)
        key = winreg.OpenKey(key, node, 0, winreg.KEY_READ)
        try:
            return winreg.QueryValueEx(key, value)
        finally:
            winreg.CloseKey(key)
    except WindowsError as e:
        if e.errno == 2:
            raise RegistryValueNotFount(node, value)
        else:
            raise


def get_value(node, value):
    return str(query_value(node, value)[0])


def get_value_type(node, value):
    return query_value(node, value)[1]


def set_value(node, value_name, value, value_type=ValueType.REG_SZ):
    key, node = _get_real_node(node)
    key = winreg.CreateKey(key, node)
    try:
        winreg.SetValueEx(key, value_name, 0, value_type, value)
    finally:
        winreg.CloseKey(key)


def iter_node_values(node):
    key, node = _get_real_node(node)
    key = winreg.OpenKey(key, node, 0, winreg.KEY_READ)
    try:
        index = 0
        while True:
            try:
                name, value, type = winreg.EnumValue(key, index)
                yield name, value
                index += 1
            except WindowsError:
                break
    finally:
        winreg.CloseKey(key)


def del_value(node, value):
    key, node = _get_real_node(node)
    key = winreg.OpenKey(key, node, 0, winreg.KEY_ALL_ACCESS)
    try:
        winreg.DeleteValue(key, value)
    finally:
        winreg.CloseKey(key)
