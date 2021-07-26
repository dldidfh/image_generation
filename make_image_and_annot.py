from rotate2 import rotation_mosaic
from light_add_sub import light_add_and_sub
from utils import box_value_resize, hangulFilePathImageRead, hangulFilePathImageWrite
import os 
import cv2
import numpy as np
from configs import *



for file_name in os.listdir(annotation_path):
    root, child = os.path.splitext(file_name)
    if child == '.txt':
        for ext in extensions:
            if os.path.exists(annotation_path + root + ext):
                image_path = annotation_path + root + ext
                gt_path = annotation_path + file_name
                save_path = [output_path +'origin_rotation_' + root,
                                 output_path +'flip_rotation_' + root,
                                 output_path + 'add_mosaic_'  + root,
                                 output_path + 'sub_mosaic_' + root,]

                image = hangulFilePathImageRead(image_path)
                h, w = image.shape[:2]
                image = cv2.resize(image,resize_pactor)
                # resize_h, resize_w = image.shape[:2]
                origin_ground_truth_list = []

                with open(gt_path) as read:
                    boxes = read.readlines()
                    for box in boxes:
                        box = box.strip()
                        box = box.split()
                        class_num = int(box[0])
                        re_center_x, re_center_y, re_box_width, re_box_height = box_value_resize(box, resize_pactor, h, w)

                        # flip_center_x = 300 - re_center_x

                        xmin = re_center_x - re_box_width/2
                        ymin = re_center_y - re_box_height/2
                        xmax = re_center_x + re_box_width/2
                        ymax = re_center_y + re_box_height/2

                        origin_ground_truth_list.append([class_num, xmin, ymin, xmax, ymax])

                for count in range(count_range[0],count_range[1]):
                    if count <= 1:
                        twelve_images, result_box = rotation_mosaic(image, origin_ground_truth_list, count, image_batch_size)
                    elif count >= 2 and count <= 3:
                        twelve_images, result_box = light_add_and_sub(image, origin_ground_truth_list, count, image_batch_size)
                    else:
                        raise "Count의 허용범위를 초과하였습니다."
                    # encoded_image = hangulFilePathImageWrite(twelve_images, ext)
                    # with open(save_path[count] + ext, 'w+b') as image_wd:
                    #     encoded_image.tofile(image_wd)

                    cv2.imwrite(save_path[count] + ext ,twelve_images)
                    with open(save_path[count] + '.txt', 'w') as wd:
                        for one_box in result_box:            
                            string = "{} {} {} {} {}\n".format(one_box[0], one_box[1], one_box[2], one_box[3], one_box[4])
                            wd.write(string)

            