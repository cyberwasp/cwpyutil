import win32api

FILE_DESCRIPTION = 'FileDescription'
PRODUCT_VERSION = 'ProductVersion'
FILE_VERSION = 'FileVersion'


def get_win32_file_translations(file):
    return win32api.GetFileVersionInfo(file, '\\VarFileInfo\\Translation')


def get_win32_string_file_info(file, info, lang=None, code_page=None):
    if not (lang and code_page):
        lang, code_page = get_win32_file_translations(file)[0]
    path = '\\StringFileInfo\\%04X%04X\\%s' % (lang, code_page, info)
    return win32api.GetFileVersionInfo(file, path)


def get_win32_product_version(file, lang=None, code_page=None):
    return get_win32_string_file_info(file, PRODUCT_VERSION, lang, code_page)


def get_win32_file_version(file, lang=None, code_page=None):
    return get_win32_string_file_info(file, FILE_VERSION, lang, code_page)


def get_win32_file_description(file, lang=None, code_page=None):
    return get_win32_string_file_info(file, FILE_DESCRIPTION, lang, code_page)
