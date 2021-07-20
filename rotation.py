import cv2
import os
import numpy as np

image = cv2.imread('./chapter2/test2.jpg', cv2.IMREAD_COLOR)

image = cv2.resize(image,(300,300))
h, w = image.shape[:2]
temp_image = np.zeros((300,300))

for i in range(3):
    for j in range(4):
        if i== 0 and j == 0 :
            three_images = image
            continue
        
        M = cv2.getRotationMatrix2D((w/2,h/2), ((i+1)*(j+1))*30, 1)

        trans_image = cv2.warpAffine(image, M, (w,h))
        if j != 0 :
            three_images = np.concatenate((three_images, trans_image), axis=1)
        else :
            three_images = trans_image
            
        print(i,j,three_images.shape)

    print('three_images shape : \t', three_images.shape, temp_image.shape)
    if i == 0:
        temp_image = three_images
    else :
        temp_image = np.concatenate((temp_image,three_images), axis=0)
    print(temp_image.shape, three_images.shape)

print(temp_image.shape)

cv2.imshow("sdf", temp_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('result.jpg', temp_image)