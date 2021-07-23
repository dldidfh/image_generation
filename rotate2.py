import cv2
from imgaug.augmenters.flip import Fliplr
from imgaug.augmenters.geometric import Affine
import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
import imageio
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

def box_value_resize(center_x, center_y, box_width, box_height, resize_pactor):
    resize_rate_height = h / resize_pactor[1]
    resize_rate_width = w / resize_pactor[0]

    re_center_x =  float(box[1]) * w / resize_rate_width
    re_center_y = float(box[2]) * h  / resize_rate_height
    re_box_width = float(box[3]) * w / resize_rate_width
    re_box_height = float(box[4]) * h / resize_rate_height

    return re_center_x, re_center_y, re_box_width, re_box_height

image_path = './test2.jpg'
gt_path = './test2.txt'
origin_rotate_gt_save_path = './origin_rotation_result.txt'
flip_rotate_gt_save_path = './flip_rotation_result.txt'

image = cv2.imread('./test2.jpg', cv2.IMREAD_COLOR)
h, w = image.shape[:2]

resize_pactor = (300,300)
resize_h, resize_w = image.shape[:2]
image = cv2.resize(image,resize_pactor)


name_space = ['origin', 'flip']

origin_ground_truth_list = []
flip_ground_truth_list = []

with open(gt_path) as read:
    boxes = read.readlines()
    for box in boxes:
        box = box.strip()
        box = box.split()
        class_num = int(box[0])
        re_center_x, re_center_y, re_box_width, re_box_height = box_value_resize(box[1],box[2],box[3],box[4], resize_pactor)

        flip_center_x = 300 - re_center_x

        xmin = re_center_x - re_box_width/2
        ymin = re_center_y - re_box_height/2
        xmax = re_center_x + re_box_width/2
        ymax = re_center_y + re_box_height/2
        flip_xmax = flip_center_x + re_box_width/2
        flip_xmin = flip_center_x - re_box_width/2
    
        origin_ground_truth_list.append([class_num, xmin, ymin, xmax, ymax])
        flip_ground_truth_list.append([class_num,flip_xmin, ymin,flip_xmax,ymax])
temp_list = [origin_ground_truth_list,flip_ground_truth_list]
origin_imgaug_bounding_boxes = []
flip_imgaug_bounding_boxes = []
for count,temp in enumerate(temp_list):
    imgaug_bounding_boxes = []
    # if count ==0:
    for box in temp:
        imgaug_bounding_boxes.append(ia.BoundingBox(x1=box[1],y1=box[2],x2=box[3],y2=box[4],label=box[0]))
    bbs = ia.BoundingBoxesOnImage(imgaug_bounding_boxes,shape=image.shape)
    if count == 0:
        seq = iaa.Sequential([
            iaa.Affine(rotate=20),
        ])
    elif count==1:
        seq = iaa.Sequential([
            iaa.Fliplr(1.0),
            iaa.Affine(rotate=20),
        ])
    image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)
    if count==0:
        cv2.imwrite('./origin_rotate.jpg',image_aug)
        with open('./origin_rotate.txt', 'w') as wd:
            for one_box in bbs_aug:
                rotate_box_width = one_box.width / resize_w
                rotate_box_height = one_box.height / resize_h
                rotate_center_x = one_box.center_x / resize_w
                rotate_center_y = one_box.center_y / resize_h
                string = "{} {} {} {} {}\n".format(one_box.label, rotate_center_x, rotate_center_y, rotate_box_width, rotate_box_height)
                wd.write(string)
    elif count==1 : 
        cv2.imwrite('./flip_rotate.jpg',image_aug)
        with open('./flip_rotate.txt', 'w') as wd:
            for one_box in bbs_aug:
                rotate_box_width = one_box.width / resize_w
                rotate_box_height = one_box.height / resize_h
                rotate_center_x = one_box.center_x / resize_w
                rotate_center_y = one_box.center_y / resize_h
                string = "{} {} {} {} {}\n".format(one_box.label, rotate_center_x, rotate_center_y, rotate_box_width, rotate_box_height)
                wd.write(string)


    # elif count == 1:
    #     for box in temp:
    #         flip_imgaug_bounding_boxes.append(ia.BoundingBox(x1=box[1],y1=box[2],x2=box[3],y2=box[4],label=box[0]))
