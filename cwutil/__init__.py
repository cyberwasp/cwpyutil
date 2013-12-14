import win32_adm
import win32_env
import who_lock_file
import win32_file_resources
import win32_registry
who_lock_file = who_lock_file.who_lock_file
get_win32_product_version = win32_file_resources.get_win32_product_version
get_win32_file_version = win32_file_resources.get_win32_file_version
get_win32_file_description = win32_file_resources.get_win32_file_description
get_win32_registry_value = win32_registry.get_value
get_win32_registry_value_type = win32_registry.get_value_type
del_win32_registry_value = win32_registry.del_value
set_win32_registry_value = win32_registry.set_value
iter_win32_registry_node_values = win32_registry.iter_node_values
RegistryValueNotFount = win32_registry.RegistryValueNotFount
InvalidHKey = win32_registry.InvalidHKey
RegistryValueType = win32_registry.ValueType
get_win32_all_user_env = win32_env.get_all_user_env
set_win32_all_user_env = win32_env.set_all_user_env
win32_is_user_an_admin = win32_adm.win32_is_user_an_admin
del_win32_all_user_env = win32_env.del_all_user_env