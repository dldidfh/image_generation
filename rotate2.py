# import cv2
from imgaug.augmenters.flip import Fliplr
from imgaug.augmenters.geometric import Affine
import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
# import imageio
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from configs import *


def rotation_mosaic(image, origin_ground_truth_list, count, image_batch_size):
    
    imgaug_bounding_boxes = []
    # if count ==0:
    for box in origin_ground_truth_list:
        imgaug_bounding_boxes.append(ia.BoundingBox(x1=box[1],y1=box[2],x2=box[3],y2=box[4],label=box[0]))
    bbs = ia.BoundingBoxesOnImage(imgaug_bounding_boxes,shape=image.shape)
    index = 0
    result_box = []
    for num_1 in range(image_batch_size[1]):
        three_images = np.zeros(image.shape)
        for num_2 in range(image_batch_size[0]):
            degree = index * 7.5
            index += 1  
            if count == 0:
                seq = iaa.Sequential([
                    iaa.Affine(rotate=degree),
                ])
            elif count==1:
                seq = iaa.Sequential([
                    iaa.Fliplr(1.0),
                    iaa.Affine(rotate=degree),
                ])
            image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)
            bbs_aug = bbs_aug.remove_out_of_image().clip_out_of_image()
            # 바운딩박스 좌표값 수정해서 새로운 배열에 추가 
            for box_1 in bbs_aug:
                rotate_box_width = round(box_1.width / (image_batch_size[0] * resize_pactor[0]),6)
                rotate_box_height = round(box_1.height / (image_batch_size[1] * resize_pactor[1]), 6)
                rotate_center_x = round(((box_1.center_x + resize_pactor[0]*num_2) / (image_batch_size[0] * resize_pactor[0])) , 6)
                rotate_center_y = round(((box_1.center_y + resize_pactor[1]*num_1) / (image_batch_size[1] * resize_pactor[1])) ,6)
                if rotate_box_height < 0.03 and rotate_box_width < 0.03:
                    continue
                result_box.append([
                    box_1.label, rotate_center_x, rotate_center_y, rotate_box_width, rotate_box_height
                ])
            
            if num_2 == 0:
                three_images = image_aug
            else:
                three_images = np.concatenate((three_images,image_aug), axis=1)
        if num_1 == 0:
            twelve_images = three_images
        else:
            twelve_images = np.concatenate((twelve_images,three_images), axis=0)
    return twelve_images, result_box


