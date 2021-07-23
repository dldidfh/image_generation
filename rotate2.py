import cv2
from imgaug.augmenters.flip import Fliplr
from imgaug.augmenters.geometric import Affine
import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
import imageio
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import os


def box_value_resize(center_x, center_y, box_width, box_height, resize_pactor):
    resize_rate_height = h / resize_pactor[1]
    resize_rate_width = w / resize_pactor[0]

    re_center_x =  float(box[1]) * w / resize_rate_width
    re_center_y = float(box[2]) * h  / resize_rate_height
    re_box_width = float(box[3]) * w / resize_rate_width
    re_box_height = float(box[4]) * h / resize_rate_height

    return re_center_x, re_center_y, re_box_width, re_box_height

def hangulFilePathImageRead ( filePath ) : 
    # 출처: https://zzdd1558.tistory.com/228 [YundleYundle]
    stream = open( filePath.encode("utf-8") , "rb") 
    bytes = bytearray(stream.read()) 
    numpyArray = np.asarray(bytes, dtype=np.uint8) 
    return cv2.imdecode(numpyArray , cv2.IMREAD_UNCHANGED)

def hangulFilePathImageWrite(image, extension):
    result, encoded_img = cv2.imencode(extension, image)
    if result:
        return encoded_img
    else: return '이거슨 실패'

annotation_path = './annotations/'
output_path = './aug_outputs/'
extensions = ['.jpg', '.png', '.bmp']
resize_pactor = (300,300)
image_batch_size = (4,3)

for file_name in os.listdir(annotation_path):
    root, child = os.path.splitext(file_name)
    if child == '.txt':
        for ext in extensions:
            if os.path.exists(annotation_path + root + ext):
                image_path = annotation_path + root + ext
                gt_path = annotation_path + file_name
                save_path = [output_path +'origin_rotation_' + root, output_path +'flip_rotation_' + root]
                image = hangulFilePathImageRead(image_path)
                h, w = image.shape[:2]
                image = cv2.resize(image,resize_pactor)
                resize_h, resize_w = image.shape[:2]
                origin_ground_truth_list = []

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

                        origin_ground_truth_list.append([class_num, xmin, ymin, xmax, ymax])

                temp_list = [origin_ground_truth_list,origin_ground_truth_list]

                # temp list에는 각각 원본의 
                for count in range(2):
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
                            # 바운딩박스 좌표값 수정해서 새로운 배열에 추가 
                            for box_1 in bbs_aug:
                                rotate_box_width = round(box_1.width / (image_batch_size[0] * resize_w),6)
                                rotate_box_height = round(box_1.height / (image_batch_size[1] * resize_h), 6)
                                rotate_center_x = round(((box_1.center_x + resize_w*num_2) / (image_batch_size[0] * resize_w)) , 6)
                                rotate_center_y = round(((box_1.center_y + resize_h*num_1) / (image_batch_size[1] * resize_h)) ,6)
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
                    encoded_image = hangulFilePathImageWrite(twelve_images, ext)
                    with open(save_path[count] + ext, 'w+b') as image_wd:
                        encoded_image.tofile(image_wd)
                    cv2.imwrite(save_path[count] + ext ,twelve_images)
                    with open(save_path[count] + '.txt', 'w') as wd:
                        for one_box in result_box:            
                            string = "{} {} {} {} {}\n".format(one_box[0], one_box[1], one_box[2], one_box[3], one_box[4])
                            wd.write(string)
                