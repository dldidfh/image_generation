import cv2
import numpy as np



def box_value_resize(box, resize_pactor, h , w):
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
    