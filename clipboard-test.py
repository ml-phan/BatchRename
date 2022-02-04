import ctypes

import win32api, win32gui


def create_window() -> int:
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = print
    wc.lpszClassName = "demo"
    wc.hInstance = win32api.GetModuleHandle(None)
    class_atom = win32gui.RegisterClass(wc)
    return win32gui.CreateWindow(class_atom, 'demo', 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)


if __name__ == '__main__':
    hwnd = create_window()
    ctypes.windll.user32.AddClipboardFormatListener(hwnd)
    win32gui.PumpMessages()