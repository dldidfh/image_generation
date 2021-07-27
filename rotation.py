# import cv2
# import os
# import numpy as np

# def retate_xyminmax_2(width, height, xmin, ymin, xmax, ymax, degree):
#     radian = degree / 180 * np.pi  # radian 으로 변환
#     point =[ (xmin,ymin), (xmin,ymax), (xmax,ymax), (xmax,ymin)]
#     # if degree < 90:

#     re_xmin = (xmin-width/2) * np.cos(radian) - (ymin-height/2)*np.sin(radian)
#     re_ymin = (xmin-width/2) * np.sin(radian) + (ymin-height/2)*np.cos(radian)
#     re_xmax = (xmax-width/2) * np.cos(radian) - (ymax-height/2)*np.sin(radian)
#     re_ymax = (xmax-width/2) * np.sin(radian) + (ymax-height/2)*np.cos(radian)
        
#         # re_right_bottom = ((xmax - width/2)*np.cos(radian) , (ymax - height/2)*np.sin(radian))
#     # if degree >= 90:
#     #     re_left_top = ((xmin - width/2)*np.sin(radian) , (ymin - height/2)*np.cos(radian))
#     #     re_right_bottom = ((xmax - width/2)*np.sin(radian) , (ymax - height/2)*np.cos(radian))

#     box_width = abs(re_xmax - re_xmin )
#     box_height = abs(re_ymax - re_ymin)
#     box_center_x = re_xmin + box_width/2
#     box_center_y = re_ymin + box_height/2

#     return box_center_x, box_center_y, box_width, box_height


# def rotate_xyminmax(width, height, xmin, ymin, xmax, ymax, degree):
#     # 출처 : https://blog.nerdfactory.ai/2020/09/10/image-augmentation-for-object-detection.html
#     # (width/2, height/2)를 중심으로 degree 회전
#     # radian = degree * (np.pi / 180)
#     # 회전하여 확장된 이미지 영역 re_width, re_height
#     # 픽셀 좌표는 정수형만 가능하므로 int로 자료형을 변환

#     radian = -degree / 360 * np.pi  # radian 으로 변환

#     # 회전하여 확장된 이미지 영역 re_width, re_height
#     # 픽셀 좌표는 정수형만 가능하므로 int로 자료형을 변환
#     re_width = width * np.cos(radian) - height * np.sin(radian) + width / 2
#     re_height = height * np.cos(radian) + width * np.sin(radian) + height / 2

#     # Bounding Box 좌상단을 첫번째 점으로 두고, 반시계방향으로 Box Point 4개를 지정
#     point = [(xmin - width / 2, height / 2 - ymin),  # P1
#              (xmin - width / 2, height / 2 - ymax),  # P2
#              (xmax - width / 2, height / 2 - ymax),  # P3
#              (xmax - width / 2, height / 2 - ymin)]  # P4

#     # 회전된 Box 의 좌표(P1', P2', P3', P4') 연산
#     rotation_point = []
#     for p in point:
#         x, y = p
#         rx = x * np.cos(radian) - y * np.sin(radian)
#         ry = y * np.cos(radian) + x * np.sin(radian)
#         # rx = rx + width / 2
#         # if rx <= 0:
#         #     rx = 0
#         # ry = ry + height / 2
#         # if ry <= 0:
#         #     ry = 0
#         rotation_point.append((rx, ry))

#     re_xmin = min(rotation_point[0][0], rotation_point[1][0], rotation_point[2][0], rotation_point[3][0]) + re_width / 2
#     re_xmax = max(rotation_point[0][0], rotation_point[1][0], rotation_point[2][0], rotation_point[3][0]) + re_width / 2
#     re_ymin = min(rotation_point[0][1], rotation_point[1][1], rotation_point[2][1], rotation_point[3][1]) + re_height / 2
#     re_ymax = max(rotation_point[0][1], rotation_point[1][1], rotation_point[2][1], rotation_point[3][1]) + re_height / 2

#     if re_xmax >= re_width:
#         re_xmax = re_width
#     if re_xmin <= 0 :
#         re_xmin = 0
#     if re_ymax >= re_height:
#         re_ymax = re_height
#     if re_ymin <= 0 :
#         re_ymin = 0

#     box_width = re_xmax - re_xmin
#     box_height = re_ymax - re_ymin
#     box_center_x = re_xmin + box_width/2
#     box_center_y = re_ymin + box_height/2

#     return box_center_x, box_center_y, box_width, box_height



# gt_path = './test2.txt'
# origin_rotate_gt_save_path = './origin_rotation_result.txt'
# flip_rotate_gt_save_path = './flip_rotation_result.txt'
# image = cv2.imread('./test2.jpg', cv2.IMREAD_COLOR)
# h, w = image.shape[:2]
# image = cv2.resize(image,(300,300))
# resize_h, resize_w = image.shape[:2]
# resize_rate_height = h / 300
# resize_rate_width = w / 300

# name_space = ['origin', 'flip']


# origin_ground_truth_list = []
# flip_ground_truth_list = []
# # fliped_x_min = width - original_x_min
# # fliped_x_max = width - original_x_max

# with open(gt_path) as fd:
#     boxes = fd.readlines()
#     for box in boxes:
#         box = box.strip()
#         box = box.split()
#         class_num = int(box[0])
#         center_x =  float(box[1]) * w / resize_rate_width
#         center_y = float(box[2]) * h  / resize_rate_height
#         box_width = float(box[3]) * w / resize_rate_width
#         box_height = float(box[4]) * h / resize_rate_height
#         flip_center_x = 300 - center_x
        
#         origin_ground_truth_list.append([class_num,center_x,center_y,box_width,box_height])
#         flip_ground_truth_list.append([class_num,flip_center_x,center_y,box_width,box_height])
# ground_truth_list_len = len(origin_ground_truth_list)

# for x in range(2):
#     temp_image = np.zeros((300,300))
#     index = 1
    
#     if x == 1:
#         image = cv2.flip(image, 1)
#     for i in range(3):
#         for j in range(4):
#             degree = index * 5
#             if i== 0 and j == 0 :
#                 three_images = image
#                 continue
#             for gt_index in range(ground_truth_list_len):
#                 class_num = origin_ground_truth_list[gt_index ][0]
#                 if x == 0:
#                     xmin = origin_ground_truth_list[gt_index ][1] - origin_ground_truth_list[gt_index ][3] // 2
#                     ymin = origin_ground_truth_list[gt_index ][2] - origin_ground_truth_list[gt_index ][4] // 2
#                     xmax = origin_ground_truth_list[gt_index ][1] + origin_ground_truth_list[gt_index ][3] // 2
#                     ymax = origin_ground_truth_list[gt_index ][2] + origin_ground_truth_list[gt_index ][4] // 2
#                     origin_rotate_center_x, origin_rotate_center_y, origin_rotate_width, origin_rotate_height = retate_xyminmax_2(300,300,xmin, ymin, xmax, ymax, degree)

#                     origin_ground_truth_list.append([
#                         class_num,
#                         origin_rotate_center_x + 300*j,
#                         origin_rotate_center_y + 300*i,
#                         origin_rotate_width,
#                         origin_rotate_height
#                     ])
#                 elif x == 1:
#                     xmin = flip_ground_truth_list[gt_index ][1] - flip_ground_truth_list[gt_index ][3] // 2
#                     ymin = flip_ground_truth_list[gt_index ][2] - flip_ground_truth_list[gt_index ][4] // 2
#                     xmax = flip_ground_truth_list[gt_index ][1] + flip_ground_truth_list[gt_index ][3] // 2
#                     ymax = flip_ground_truth_list[gt_index ][2] + flip_ground_truth_list[gt_index ][4] // 2
#                     flip_rotate_center_x, flip_rotate_center_y, flip_rotate_width, flip_rotate_height = retate_xyminmax_2(300,300,xmin, ymin, xmax, ymax, degree)
                    
#                     flip_ground_truth_list.append([
#                         class_num,
#                         flip_rotate_center_x + 300*j,
#                         flip_rotate_center_y + 300*i,
#                         flip_rotate_width,
#                         flip_rotate_height
#                     ])

#             M = cv2.getRotationMatrix2D((resize_w/2,resize_h/2), degree, 1)
#             index +=1
#             trans_image = cv2.warpAffine(image, M, (resize_w,resize_h))
#             if j != 0 :
#                 three_images = np.concatenate((three_images, trans_image), axis=1)
#             else :
#                 three_images = trans_image
                

#         print('three_images shape : \t', three_images.shape, temp_image.shape)
#         if i == 0:
#             temp_image = three_images
#         else :
#             temp_image = np.concatenate((temp_image,three_images), axis=0)

#     cv2.imwrite(name_space[x] + '_rotation_result'+'.jpg', temp_image)

# resize_h, resize_w = temp_image.shape[:2]
# print(resize_h, resize_w)


    
# with open(origin_rotate_gt_save_path, 'w') as wd:
#     for lines in origin_ground_truth_list:
#         string = "{} {} {} {} {}\n".format(
#             lines[0], 
#             round(lines[1] / resize_w , 6), 
#             round(lines[2] / resize_h,6),
#             round(lines[3] / resize_w,6),
#             round(lines[4] / resize_h,6),
#         )
#         d = wd.write(string)
# with open(flip_rotate_gt_save_path, 'w') as wd:
#     for lines in origin_ground_truth_list:
#         string = "{} {} {} {} {}\n".format(
#             lines[0], 
#             round(lines[1] / resize_w , 6), 
#             round(lines[2] / resize_h,6),
#             round(lines[3] / resize_w,6),
#             round(lines[4] / resize_h,6),
#         )
#         d = wd.write(string)
        