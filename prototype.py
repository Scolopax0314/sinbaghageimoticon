import ctypes
import ctypes.wintypes
import win32con
import win32api
import win32gui
import time
import win32clipboard
from PIL import Image, ImageGrab, ImageFont, ImageDraw
import io
import pyautogui
import os
import threading
import tkinter as tk
from tkinter import ttk


def maxmin(Mm, a, b):
    if a > b:
        if Mm:
            return a
        return b
    if Mm:
        return b
    return a

def enum_child(parent_hwnd):
    child_windows = []

    def enum_child_proc(hwnd, lParam):
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        child_windows.append((hwnd, title, class_name))
        return True

    win32gui.EnumChildWindows(parent_hwnd, enum_child_proc, None)
    return child_windows

def get_text(hwnd):
    length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH) + 1
    buffer = ctypes.create_unicode_buffer(length)
    win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, length, buffer)
    return buffer.value

def setClipboard():
    bitmap = io.BytesIO()
    imageLoad("output_image").convert("RGB").save(bitmap, "BMP")
    convData = bitmap.getvalue()[14:]
    bitmap.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, convData)
    win32clipboard.CloseClipboard()

def SendImage():
    setClipboard()
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)
    pyautogui.hotkey("enter")

def imageLoad(name):
    imagename = name + ".png"
    imagepath = os.path.join("images", imagename)
    image = Image.open(imagepath)
    return image

def makeimg(input):
    baseimg = imageLoad("baseimg")
    outputimg = baseimg.copy()

    draw = ImageDraw.Draw(outputimg)

    font_path = os.path.join("font", "malgunbd.ttf")
    text = input
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)
    position = (385, 70)

    draw.text(position, text, fill="black", font=font)

    output_path = os.path.join("images", 'output_image.png')
    outputimg.save(output_path)

def active_title():
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    return title

def next_title(current_title, key_title):
    titles = []

    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                titles.append(title)
        return True

    win32gui.EnumWindows(enum_windows_proc, None)

    if current_title in titles:
        current_index = titles.index(current_title)
        next_index = (current_index + 1) % len(titles)
        if titles[next_index] == key_title:
            return True
        return False
    return False

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", ctypes.wintypes.DWORD),
        ("scanCode", ctypes.wintypes.DWORD),
        ("flags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
    ]

class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", ctypes.wintypes.HWND),
        ("message", ctypes.wintypes.UINT),
        ("wParam", ctypes.wintypes.WPARAM),
        ("lParam", ctypes.wintypes.LPARAM),
        ("time", ctypes.wintypes.DWORD),
        ("pt", ctypes.wintypes.POINT)
    ]

global Run
Run = False

def hook(nCode, wParam, lParam):
    if nCode == win32con.HC_ACTION:
        kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk_code = kb.vkCode

        if wParam == win32con.WM_KEYDOWN and vk_code == win32con.VK_RETURN:
            if Run:
                current_hwnd = win32gui.GetForegroundWindow()
                for hwnd, title, classname in enum_child(current_hwnd):
                    if classname == 'RICHEDIT50W':
                        message_hwnd = hwnd
                        message = get_text(message_hwnd)
                        win32gui.SendMessage(message_hwnd, win32con.WM_SETTEXT, 0, '')
                        if len(message) > 0:
                            makeimg(message)
                            SendImage()
                        return 1 

    return user32.CallNextHookEx(None, nCode, wParam, ctypes.c_void_p(lParam))

HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)
keyboard_proc = HOOKPROC(hook)

module_handle = win32api.GetModuleHandle(None)
module_handle = ctypes.c_void_p(module_handle)

hooked = user32.SetWindowsHookExW(win32con.WH_KEYBOARD_LL, keyboard_proc, module_handle, 0)

def run_program():
    global Run
    while True:
        key_title = "KakaoTalkShadowWnd"

        activetitle = active_title()
        Run = next_title(activetitle, key_title)

        try:
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        finally:
            user32.UnhookWindowsHookEx(hooked)

def toggle_run():
    global Run
    Run = not Run
    status_label.config(text=f"기능 {'활성화' if Run else '비활성화'}됨")

def on_closing():
    user32.UnhookWindowsHookEx(hooked)
    root.destroy()

root = tk.Tk()
root.title("기능 On/Off 설정")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

toggle_button = ttk.Button(main_frame, text="기능 On/Off", command=toggle_run)
toggle_button.grid(row=0, column=0, padx=5, pady=5)

status_label = ttk.Label(main_frame, text="기능 비활성화됨")
status_label.grid(row=1, column=0, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)

threading.Thread(target=run_program, daemon=True).start()

root.mainloop()