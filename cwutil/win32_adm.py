from win32com.shell import shell


def win32_is_user_an_admin():
    return shell.IsUserAnAdmin()
