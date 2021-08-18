import shutil
import os
import re
from hangul_romanize import Transliter
from hangul_romanize.rule import academic

transliter = Transliter(academic)
# print(transliter.translit(u'안녕하세요'))

path = './annotations/'
# path = './aug_outputs/'
test_path = './path_test/'

file_names = os.listdir(path)

for file_name in file_names:
    copy_file_name = file_name
    hangles = re.compile('[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+').findall(file_name)
    print(hangles)
    for word in hangles:
        word_index = file_name.find(word)
        if word_index != -1:
            find_word = file_name[word_index:word_index+len(word)]
            if find_word == '시대':
                file_name = file_name.replace(find_word, 'h')
            elif find_word == '비':
                file_name = file_name.replace(find_word, 'raining')
    romanized_word = transliter.translit(file_name)

    spec_word = ['-','(',')','JPG']
    for word in spec_word:
        word_index = romanized_word.find(word)
        if word_index != -1:
            find_word = romanized_word[word_index:word_index+len(word)]
            if find_word == 'JPG':
                romanized_word = romanized_word.replace(find_word,'jpg')
            else :
                romanized_word = romanized_word.replace(find_word,'')

    shutil.move(path+copy_file_name,path+romanized_word)

