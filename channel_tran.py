import cv2
import os
import numpy as np

# image = cv2.imread('./test2.jpg', cv2.IMREAD_COLOR)

# image = cv2.resize(image,(300,300))
# h, w = image.shape[:2]
# channel_type = [cv2.COLOR_RGB2BGR, 'flip']

# for x in range(len(channel_type)):

#     pass


flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
for i in flags:
    print(i)