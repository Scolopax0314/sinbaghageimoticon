from math import sqrt
import cv2
import numpy as np
import fontTools

h = 20
a, b = 55, 36
rect = []
n = int(2 * b / h)

if n % 2:
    for i in range(0, n, 2):
        y = i * h / 2
        l = sqrt(1 - ((y + h/2) / b) ** 2) * a
        rect.append((y, l))
        if i == 1: continue
        rect.append((-y, l))
else:
    for i in range(1, n, 2):
        y = i * h / 2
        l = sqrt(1 - ((y + h/2) / b) ** 2) * a
        rect.append((y, l))
        rect.append((-y, l))

print(rect)

img = np.zeros((225, 225, 3))

for y, l in rect:
    y, l = int(y), int(l)
    print(y, l)
    cv2.rectangle(img, (164 - l, y + 50 + h//2), (164 + l, y + 50 - h//2), (0, 0, 255), 1)
cv2.ellipse(img, (164, 50), (a, b), 0, 0, 360, (0, 0, 255), 1)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()