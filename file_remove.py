import os
import shutil
from tkinter import messagebox


def remove():
    dir_path = './dataset/'
    print('-'*75)
    print('[삭제한 폴더 및 사진]')
    file_list = os.listdir(dir_path)
    print(*file_list)
    for file in file_list:
        file_path = os.path.join(dir_path, file)
        if os.path.isdir(file_path):
            dir_path2 = file_path
            print(dir_path2)
            shutil.rmtree(dir_path2)
    
    file_list = os.listdir(dir_path)
    print(*file_list)
    print('='*75)
    #print('Remove Success!!!')
    print('-'*15 + '  체험자 이미지를 성공적으로 삭제 했습니다. ' + '-'*15)                
    messagebox.showinfo("스마트 도어 시스템","체험자의 모든 정보가 삭제되었습니다.")                 
    print('='*75)

#os.rmdir('/home/pi/Face_Recognition/dataset/daun')