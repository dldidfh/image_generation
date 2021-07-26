import cv2
import os
import numpy as np
import shutil
from configs import *
# image_path = './test2.jpg'
# gt_path = './test2.txt'
# trans_gt_add_save_path = './add_result.txt'
# trans_gt_sub_save_path = './sub_result.txt'


def light_add_and_sub(image, origin_ground_truth_list, count, image_batch_size):
    w, h = image_batch_size
    # resize_rate_height = h / 300
    # resize_rate_width = w / 300
    result_box = []

    twelve_images = []
    # temp_sub_image = []
    index = 1
    ground_truth_list_len = len(origin_ground_truth_list)
    for num_1 in range(3):
        for num_2 in range(4):
            
            # if num_1==0 and num_2 == 0:
            #     three_image = image
                # three_image = image
                # continue
            for gt_index in range(ground_truth_list_len):
                box_width = origin_ground_truth_list[gt_index ][3]  - origin_ground_truth_list[gt_index ][1] 
                box_height = origin_ground_truth_list[gt_index ][4]  - origin_ground_truth_list[gt_index ][2] 
                center_x = origin_ground_truth_list[gt_index ][1] + box_width/2
                center_y = origin_ground_truth_list[gt_index ][2] + box_height/2 
                result_box.append([
                        origin_ground_truth_list[gt_index ][0], 
                            # rotate_center_x = round(((box_1.center_x + resize_pactor[0]*num_2) / (image_batch_size[0] * resize_pactor[0])) , 6)
                            # rotate_center_y = round(((box_1.center_y + resize_pactor[1]*num_1) / (image_batch_size[1] * resize_pactor[1])) ,6)
                        round((center_x + resize_pactor[0]*num_2 ) / (image_batch_size[0] * resize_pactor[0]) , 6),
                        round((center_y + resize_pactor[1]*num_1 ) / (image_batch_size[1] * resize_pactor[1]) , 6),
                        # (origin_ground_truth_list[gt_index][2] + resize_pactor[1]*num_1),
                        round(box_width / (image_batch_size[0] * resize_pactor[0]) ,6),
                        round(box_height / (image_batch_size[1] * resize_pactor[1]) ,6),
                    ])
            
            val = index * 2
            index += 1
            array = np.full(image.shape, (val,val,val), dtype=np.uint8)

            if count == 2:
                image = cv2.add(image, array)
            elif count == 3:
                image = cv2.subtract(image, array)
            if num_2 != 0:
                three_image = np.concatenate((three_image,image), axis=1)
                # three_sub_image = np.concatenate((three_sub_image,image), axis=1)
            else:
                three_image = image
                # three_sub_image = image

        if num_1 == 0 :
            twelve_images = three_image
            # temp_sub_image = three_sub_image
        else :
            twelve_images = np.concatenate((twelve_images, three_image), axis=0)
            # temp_sub_image = np.concatenate((temp_sub_image, three_sub_image), axis=0)
    return twelve_images, result_box

    # cv2.imwrite('add_result'+'.jpg', twelve_images)
    # cv2.imwrite('sub_result'+'.jpg', temp_sub_image)
    # resize_h, resize_w = twelve_images.shape[:2]

    # with open(trans_gt_add_save_path, 'w') as wd:
    #     for lines in ground_truth_list:
    #         string = "{} {} {} {} {}\n".format(
    #             lines[0], 
    #             round(lines[1] / resize_w , 6), 
    #             round(lines[2] / resize_h,6),
    #             round(lines[3] / resize_w,6),
    #             round(lines[4] / resize_h,6),
    #         )
    #         d = wd.write(string)
    # shutil.copy(trans_gt_add_save_path, trans_gt_sub_save_path)
