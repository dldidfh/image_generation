# from hangul_romanize import Transliter
# from hangul_romanize.rule import academic
import os
# transliter = Transliter(academic)
# print(transliter.translit(u'안녕하세요'))
# 윈도우에서는 대소문자를 같은 문자라고 인식하지만 
# 리눅스는 다른 문자라고 인식한다 
annot_path = './aug_outputs/'
for file_num in os.listdir(annot_path): # 디렉토리를 조회한다            
    file_path = os.path.join(annot_path, file_num)
    root, child = os.path.splitext(file_num)
    if child == '.txt':
        if os.path.exists(annot_path +'/'+ root  + '.jpg'):
            image_path = annot_path+'/' + root + '.jpg'
        elif os.path.exists(annot_path +'/'+ root  + '.png'):
            image_path = annot_path+'/' + root + '.png'
        elif os.path.exists(annot_path +'/'+ root  + '.bmp'):
            image_path = annot_path+'/' + root + '.bmp'
        else: print("이미지가 없고 텍스트만 있는 파일", file_num)