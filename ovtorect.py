from math import sqrt
import cv2
import numpy as np

h = 40
a, b = 200, 150
rect = []
n = int(2 * b / h)
    
for i in range(n):
    y = (i - n / 2) * h
    if i > n/2: l = sqrt(1 - ((y + h) / b) ** 2) * a
    else: l = sqrt(1 - (y / b) ** 2) * a
    
    if l >= 2 * h: rect.append((y, l))
print(rect)

img = np.zeros((480, 640, 3))

for y, l in rect:
    y, l = int(y), int(l)
    print(y, l)
    cv2.rectangle(img, (320 - l, y + 240 + h), (320 + l, y + 240), (0, 0, 255), 1)
cv2.ellipse(img, (320, 240), (a, b), 0, 0, 360, (0, 0, 255), 1)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()