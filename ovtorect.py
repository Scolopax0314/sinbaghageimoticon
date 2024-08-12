from math import sqrt
import cv2
import numpy as np
from PIL import Image, ImageGrab, ImageFont, ImageDraw
import os

def imageLoad(name):
    imagename = name + ".png"
    imagepath = os.path.join("images", imagename)
    image = Image.open(imagepath)
    return image

textbox = 0
baseimg = imageLoad("baseimg")
mid = (168, 54)
a, b = 55, 36
outputimg = baseimg.copy()
draw = ImageDraw.Draw(outputimg)
font_path = os.path.join("font", "malgunbd.ttf")
text = input()
text_size = 1
font_size = 255

while textbox <= text_size * 1.33:
    font = ImageFont.truetype(font_path, font_size / 1.33)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_size = (bbox[2] - bbox[0])
    rect = []
    n = int(2 * b / font_size)
    n -= (n+1) % 2
    for i in range(0, n, 2):
            y = i * font_size / 2
            l = sqrt(1 - ((y + font_size/2) / b) ** 2) * a - a*(a/b)/10
            y, l = int(y), int(l)
            if 1.8 * l >= font_size:
                rect.append((y, l))
                if y == 0: continue
                rect.append((-y, l))
    textbox = 2 * sum(yl[1] for yl in rect)
    font_size = int(0.95 * font_size)
    print(font_size, textbox, text_size)

rect = sorted(rect, key=lambda x: x[0])
print(rect)

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

output_path = os.path.join("images", 'output_image.png')
outputimg.save(output_path)
'''
position = (164, 50)
draw.text(position, text, fill="black", font=font)

output_path = os.path.join("images", 'output_image.png')
outputimg.save(output_path)
'''



img = np.zeros((225, 225, 3))

for y, l in rect:
    print(y, l)
    cv2.rectangle(img, (164 - l, y + 50 + font_size//2), (164 + l, y + 50 - font_size//2), (0, 0, 255), 1)
cv2.ellipse(img, (164, 50), (a, b), 0, 0, 360, (0, 0, 255), 1)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
