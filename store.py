import ctypes, ctypes.wintypes
import win32con, win32api, win32gui, win32clipboard
from PIL import Image, ImageFont, ImageDraw
import io, os, re, time
import pyautogui
import threading
import tkinter as tk
from tkinter import ttk
from math import *

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, pyqtSignal

results = [[],[],[]]
for i in range(3):
    with open(f"images/imginf{i+1}.txt", 'r') as file:
        lines = file.read().splitlines()
    pattern = re.compile(r'\d+')
    for line in lines:
        numbers = list(map(int, pattern.findall(line)))
        if len(numbers) == 2:
            results[i].append(tuple(numbers))
        elif len(numbers) == 1:
            results[i].append(numbers[0])

app = None
#클릭가능한 객체 구조
class ClickableLabel(QLabel):
    clicked = pyqtSignal(int)

    def __init__(self, image_path, index):
        super().__init__()
        self.index = index
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)
            print(self.index)
            QApplication.quit()

#배치하려는 이미지 object의 구조
class ImageWindow(QWidget):
    def __init__(self, image_path, index):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = ClickableLabel(image_path, index)
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.resize(pixmap.width(), pixmap.height())
        self.img_width = int(pixmap.width())
        self.img_height = int(pixmap.height())

#직사각형 클래스
class RectangleWindow(QWidget):
    def __init__(self, parent, width, height, x, y, color=QColor(169, 169, 169, 150)):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setGeometry(x, y, width, height)

        self.color = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(0, 0, self.width(), self.height(), self.color)

#최상단 위치
def bring_to_top(window):
    hwnd = int(window.winId())
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
    )
#경로 다듬기
def image_path(image_path):
    new_path = 'images/' + image_path + '.png'
    return new_path


image_paths = ['baseimg1','baseimg2','baseimg3']  
copy_image_paths = []  
images = []

#보이는 사진 크기 재설정
def img_resize(path):
        baseimg = imageLoad(path)
        max_width = 0
        height = baseimg.size[1]
        if height > 200:
            rate = 200 / height
            outputimg = baseimg.resize((int(baseimg.size[0]*rate),200), Image.Resampling.LANCZOS)
            output_path = os.path.join("images", f"{path}_copy.png")
            outputimg.save(output_path)
            copy_image_paths.append(f"images/{path}_copy.png")

#사진 위치
def image_location(img1,img2,img3,hwnd):
    pos1x, pos1y, pos2x, pos2y = win32gui.GetWindowRect(hwnd)
    padding = int((pos2x - pos1x - img1.img_width - img2.img_width - img3.img_width) / 4)
    img1.move(pos1x + padding, pos2y - img1.img_height - 167)
    img2.move(pos1x + 2*padding + img1.img_width, pos2y - img2.img_height - 167)
    img3.move(pos1x + 3*padding + img1.img_width + img2.img_width, pos2y - img3.img_height - 167)

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
    imageLoad("outputimg").convert("RGB").save(bitmap, "BMP")
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

def makeimg(input, index):
    global results
    textbox = 0
    baseimg = imageLoad(image_paths[index])
    rate = 800 / baseimg.size[0]
    mid = results[index][0][0] * rate, results[index][0][1] * rate
    a, b = results[index][1][0] * rate, results[index][1][1] * rate
    outputimg = baseimg.copy().resize((800, int(baseimg.size[1]*rate)), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(outputimg)
    font_path = os.path.join(font_folder, selected_font.get() + '.ttf')
    text_size = 1
    font_size = results[index][2] * rate
    text = input

    while textbox < text_size * 1.33 :
        font = ImageFont.truetype(font_path, font_size / 1.33)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_size = bbox[2] - bbox[0]
        rect = []
        n = int(2 * b / font_size)
        n -= (n+1)%2
        for i in range(0, n, 2):
                y = i * font_size / 2
                l = sqrt(1 - ((y + font_size/2) / b) ** 2) * a - a*(a/b)/12
                y, l = int(y), int(l)
                if l >= font_size:
                    rect.append((y, l))
                    if y == 0: continue
                    rect.append((-y, l))
        textbox = 2 * sum(yl[1] for yl in rect)
        font_size = int(0.95 * font_size)

    rect = sorted(rect, key=lambda x: x[0])
    while textbox > text_size * 1.33:
        text = ' '+text+' '
        bbox = draw.textbbox((0, 0), text, font=font)
        text_size = (bbox[2] - bbox[0])
    for y, l in rect:
        position = (mid[0] - l, mid[1] + y - font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_size = (bbox[2] - bbox[0])
        prt = len(text)
        while text_size > 2 * l:
            bbox = draw.textbbox((0, 0), text[:prt], font=font)
            text_size = (bbox[2] - bbox[0])
            prt -= 1
        draw.text(position, text[:prt], fill="black", font=font)
        text = text[prt:]

    output_path = os.path.join("images", 'outputimg.png')
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

def img_func(message):
    global app
    if app is None:
        app = QApplication(sys.argv)

    for i, path in enumerate(image_paths):
        img_resize(path)
        img = ImageWindow(copy_image_paths[i], i)
        img.label.clicked.connect(lambda index, msg=message: on_image_clicked(msg, index)) 
        images.append(img)
    hwnd = win32gui.GetForegroundWindow()
    pos1x, pos1y, pos2x, pos2y = win32gui.GetWindowRect(hwnd)
    rect = RectangleWindow(None, pos2x-pos1x,250, 0, 0)
    rect.move(pos1x,pos2y-397)
    image_location(images[0], images[1], images[2], hwnd)

    rect.show()
    bring_to_top(rect)
    for i in images:
        i.show()
        bring_to_top(i)
    app.exec_()

def on_image_clicked(message, index):
    for img in images:
        img.hide()
    makeimg(message, index)
    SendImage()


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

def hook(nCode, wParam, lParam):
    if nCode == win32con.HC_ACTION:
        kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk_code = kb.vkCode
        if wParam == win32con.WM_KEYDOWN and vk_code == win32con.VK_RETURN:
            if Run:
                current_hwnd = win32gui.GetForegroundWindow()
                for hwnd, title, classname in enum_child(current_hwnd):
                    if classname == 'RICHEDIT50W':
                        images.clear()
                        message_hwnd = hwnd
                        message = get_text(message_hwnd)
                        win32gui.SendMessage(message_hwnd, win32con.WM_SETTEXT, 0, '')
                        if len(message) > 0:
                            img_func(message)
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

Run = False
root = tk.Tk()
root.title("기능 On/Off 설정")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

toggle_button = ttk.Button(main_frame, text="기능 On/Off", command=toggle_run)
toggle_button.grid(row=0, column=0, padx=5, pady=5)

status_label = ttk.Label(main_frame, text="기능 비활성화됨")
status_label.grid(row=1, column=0, padx=5, pady=5)

font_folder = "font"
fonts = [os.path.splitext(f)[0] for f in os.listdir(font_folder) if f.endswith('.ttf')]
selected_font = tk.StringVar(value=fonts[0])

font_label = ttk.Label(main_frame, text="폰트 선택:")
font_label.grid(row=2, column=0, padx=5, pady=5)

font_menu = ttk.Combobox(main_frame, textvariable=selected_font, values=fonts)
font_menu.grid(row=3, column=0, padx=5, pady=5)
font_menu.current(0) 

root.protocol("WM_DELETE_WINDOW", on_closing)

threading.Thread(target=run_program, daemon=True).start()

root.mainloop()