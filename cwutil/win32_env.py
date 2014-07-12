import win32_registry
import os
from win32api import SendMessage
import win32con

ENV_REG_NODE = r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment'


def get_all_user_env(name, expanded=True):
    value = win32_registry.get_value(ENV_REG_NODE, name)
    if expanded:
        return os.path.expandvars(value)
    else:
        return value


def set_all_user_env(name, value):
    win32_registry.set_value(ENV_REG_NODE, name, value, win32_registry.ValueType.REG_EXPAND_SZ)
    SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')


def del_all_user_env(name):
    win32_registry.del_value(ENV_REG_NODE, name)
