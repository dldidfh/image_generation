import cv2
import os
import numpy as np
import shutil

image_path = './test2.jpg'
gt_path = './test2.txt'
trans_gt_add_save_path = './add_result.txt'
trans_gt_sub_save_path = './sub_result.txt'
origin_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
h, w = origin_image.shape[:2]
image = cv2.resize(origin_image,(300,300))

resize_rate_height = h / 300
resize_rate_width = w / 300
ground_truth_list = []
with open(gt_path) as fd:
    boxes = fd.readlines()
    for box in boxes:
        box = box.strip()
        box = box.split()
        class_num = int(box[0])
        center_x =  float(box[1]) * w / resize_rate_width
        center_y = float(box[2]) * h  / resize_rate_height
        box_width = float(box[3]) * w / resize_rate_width
        box_height = float(box[4]) * h / resize_rate_height
        ground_truth_list.append([class_num,center_x,center_y,box_width,box_height])
temp_add_image = np.zeros((300,300))
temp_sub_image = np.zeros((300,300))
index = 1
ground_truth_list_len = len(ground_truth_list)
for i in range(3):
    for j in range(4):
        
        if i==0 and j == 0:
            three_add_image = image
            three_sub_image = image
            continue
        for gt_index in range(ground_truth_list_len):
            ground_truth_list.append([
                    ground_truth_list[gt_index ][0], 
                    ground_truth_list[gt_index][1] + 300*j,
                    ground_truth_list[gt_index][2] + 300*i,
                    ground_truth_list[gt_index][3],
                    ground_truth_list[gt_index][4],
                ])
        
        val = index * 10
        index += 1
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
resize_h, resize_w = temp_add_image.shape[:2]
print(resize_h, resize_w)

with open(trans_gt_add_save_path, 'w') as wd:
    for lines in ground_truth_list:
        string = "{} {} {} {} {}\n".format(
            lines[0], 
            round(lines[1] / resize_w , 6), 
            round(lines[2] / resize_h,6),
            round(lines[3] / resize_w,6),
            round(lines[4] / resize_h,6),
        )
        d = wd.write(string)
shutil.copy(trans_gt_add_save_path, trans_gt_sub_save_path)