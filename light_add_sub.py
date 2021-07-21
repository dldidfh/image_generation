import cv2
import os
import numpy as np

image = cv2.imread('./test2.jpg', cv2.IMREAD_COLOR)

image = cv2.resize(image,(300,300))
h, w = image.shape[:2]

name_space = ['origin', 'flip']
temp_add_image = np.zeros((300,300))
temp_sub_image = np.zeros((300,300))
# for x in range(2):
for i in range(4):
    for j in range(3):
        if i==0 and j == 0:
            three_add_image = image
            three_sub_image = image
            continue
        val = (i+1)*(j+1) * 10
        print("val 값 \t : {}".format(val) )        
        array = np.full(image.shape, (val,val,val), dtype=np.uint8)
        print(image.shape, array.shape)
        add_image = cv2.add(image, array)
        sub_image = cv2.subtract(image, array)
        if j != 0:
            three_add_image = np.concatenate((three_add_image,add_image), axis=1)
            three_sub_image = np.concatenate((three_sub_image,sub_image), axis=1)
        else:
            three_add_image = add_image
            three_sub_image = sub_image

    if i == 0 :
        temp_add_image = three_add_image
        temp_sub_image = three_sub_image
    else :
        temp_add_image = np.concatenate((temp_add_image, three_add_image), axis=0)
        temp_sub_image = np.concatenate((temp_sub_image, three_sub_image), axis=0)



cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('add_result'+'.jpg', temp_add_image)
cv2.imwrite('sub_result'+'.jpg', temp_sub_image)