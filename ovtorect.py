from math import sqrt
import cv2
import numpy as np

h = 10
a, b = 55, 36
rect = []
n = int(2 * b / h)
    
for i in range(n):
    y = (i - n / 2) * h
    if i > n/2: l = sqrt(1 - ((y + h) / b) ** 2) * a
    else: l = sqrt(1 - (y / b) ** 2) * a
    
    if l >= 2 * h: rect.append((y, l))
print(rect)

img = np.zeros((225, 225, 3))

for y, l in rect:
    y, l = int(y), int(l)
    print(y, l)
    cv2.rectangle(img, (164 - l, y + 50 + h), (164 + l, y + 50), (0, 0, 255), 1)
cv2.ellipse(img, (164, 50), (a, b), 0, 0, 360, (0, 0, 255), 1)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()