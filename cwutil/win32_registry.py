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


class ValueType:
    REG_SZ = _winreg.REG_SZ
    REG_EXPAND_SZ = _winreg.REG_EXPAND_SZ


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


def query_value(node, value):
    try:
        key, node = _get_real_node(node)
        key = _winreg.OpenKey(key, node, 0, _winreg.KEY_READ)
        try:
            return _winreg.QueryValueEx(key, value)
        finally:
            _winreg.CloseKey(key)
    except exceptions.WindowsError as e:
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
    key = _winreg.CreateKey(key, node)
    try:
        _winreg.SetValueEx(key, value_name, 0, value_type, value)
    finally:
        _winreg.CloseKey(key)


def iter_node_values(node):
    key, node = _get_real_node(node)
    key = _winreg.OpenKey(key, node, 0, _winreg.KEY_READ)
    try:
        index = 0
        while True:
            try:
                name, value, type = _winreg.EnumValue(key, index)
                yield name, value
                index += 1
            except exceptions.WindowsError:
                break
    finally:
        _winreg.CloseKey(key)


def del_value(node, value):
    key, node = _get_real_node(node)
    key = _winreg.OpenKey(key, node, 0, _winreg.KEY_ALL_ACCESS)
    try:
        _winreg.DeleteValue(key, value)
    finally:
        _winreg.CloseKey(key)
