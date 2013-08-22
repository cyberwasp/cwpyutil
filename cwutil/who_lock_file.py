import win32process
import win32api
import psutil
import pywintypes
import sys


def who_lock_file(file_name):
    for pid in win32process.EnumProcesses():
        try:
            process = psutil.Process(pid)
            #check lock open files
            open_files = process.get_open_files()
            for f in open_files:
                if f.path.upper().endswith(file_name.upper()):
                    yield process
                    break
            #check lock module
            process_handle = win32api.OpenProcess(0xFFFF, True, pid)
            modules = win32process.EnumProcessModules(process_handle)
            for m in modules:
                module_name = win32process.GetModuleFileNameEx(process_handle, m)
                if module_name.upper().endswith(file_name.upper()):
                    yield process
        #ignore some known errors
        except pywintypes.error as e:
            if not e[0] in [299, 5, 87]:
                raise
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: who_lock_file <file name>")
    else:
        who_lock_file(sys.argv[1])