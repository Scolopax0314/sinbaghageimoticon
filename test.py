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
from math import *
import re

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
hwnd = win32gui.GetForegroundWindow()
time.sleep(1)
pos1x, pos1y, pos2x, pos2y = win32gui.GetWindowRect(hwnd)
print(pos2x - pos1x, pos2y - pos1y)

#min width: 475, 1920
#min height: 562, 1020