import win32gui

def active_title():
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    return title

if __name__ == "__main__":
    while True: