

annotation_path = './annotations/'
# annotation_path = './samples/'
output_path = './aug_outputs/'
extensions = ['.jpg', '.png', '.bmp']  # windows에서는 확장자의 대소문자를 같다고 인식하지만 Linux는 다르다고 인식 
resize_pactor = (300,300)
count_range = (2,4) # 0 = rotation만  # 1 = rotation + flip # 2 = rotation + flip + 밝기 높이기 # 3 = rotation + flip + 밝기 높이기 + 밝기 줄이기
image_batch_size = (4,3)