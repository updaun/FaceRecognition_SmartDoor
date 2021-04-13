import os
from tkinter import messagebox

def make(name):
    if  name == '':
        print('[오류] 체험자의 이름을 입력해주세요.')
        messagebox.showinfo("스마트 도어 시스템","체험자의 이름을 입력해주세요.") 

    else:
        def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print ('Error: Creating directory. ' +  directory)
                
        createFolder('./dataset/'+name)

        print('='*75)
        print('-'*15 + '  체험자 폴더  [ ' + name + ' ]이(가) 생성되었습니다.' + '-'*15)
        print('='*75)
        messagebox.showinfo("스마트 도어 시스템","체험자 폴더가 생성되었습니다.") 
