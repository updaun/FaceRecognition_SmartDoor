from tkinter import *
import tkinter.font
from tkinter import messagebox


from dir_make import make
from face_shot import shot
from train_model import train
from face_lock import lock
from file_remove import remove

def test():
    if textExample.get().encode().isalpha():
        make(textExample.get())
    else:
        print("[오류] 체험자의 이름을 영어로 입력해주세요.")
        messagebox.showinfo("스마트 도어 시스템","체험자의 이름을 영어로 입력해주세요.") 
        textExample.delete(0,END)

def isEnglishOrKorean(input_s):
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return "k" if k_count>1 else "e"

root = Tk()
root.geometry("480x720+875+0")
root.resizable(False, False)
#root.iconbitmap('face_recognition.ico')
root.iconphoto(False, PhotoImage(file='face_recognition.png'))
root.configure(bg='#FFFFDE')
root.title("스마트 도어 시스템")
#root.title("Smart Door System")


#font=tkinter.font.Font(family="돋움", size=20, slant="italic")

font=tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=15, weight=tkinter.font.BOLD) # 버튼 폰트
font0=tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=1 ) # 공백 폰트
font1=tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=11) # 설명 폰트
font2=tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=18) # TEXT 박스, CI 폰트
font3=tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=18, weight=tkinter.font.BOLD) # Title 폰트

image1 = PhotoImage(file = "face_recognition.png")
photoimage1 = image1.subsample(10, 10)
imgLabel1 = Label(root, image=photoimage1, width=50, height=50, background='#FFFFDE')

#btn1 = Button(root, text = "체험자 폴더 생성", width=25, height=1, font = font, foreground='white', background='#2f3640', command=lambda: make(textExample.get(1.0, END+"-1c")))
#btn1 = Button(root, text = "체험자 폴더 생성", width=20, height=1, font = font, foreground='white', background='#2f3640', command=lambda: make(textExample.get()))
btn1 = Button(root, text = "체험자 이름 등록", width=20, height=1, font = font, foreground='white', background='#2f3640', command=test)
btn2 = Button(root, text = "체험자 사진 촬영", width=20, height=1, font = font, foreground='white', background='#2f3640', command=lambda: shot(textExample.get()))
btn3 = Button(root, text = "인공지능 학습", width=20, height=1, font = font, foreground='white', background='#2f3640', command=train)
btn4 = Button(root, text = "스마트 도어 작동", width=20, height=1, font = font, foreground='white', background='#2f3640', command=lock)
btn5 = Button(root, text = "체험자 사진 삭제", width=20, height=1, font = font, foreground='white', background='#2f3640', command=remove)

label000 = Label(root, text='', anchor = "sw" , width=40, height=1, font = font0, background='#FFFFDE')
label001 = Label(root, text='', anchor = "sw" , width=40, height=1, font = font0, background='#FFFFDE')
label002 = Label(root, text='', anchor = "sw" , width=40, height=1, font = font0, background='#FFFFDE')
label003 = Label(root, text='', anchor = "sw" , width=40, height=1, font = font0, background='#FFFFDE')
label004 = Label(root, text='', anchor = "sw" , width=40, height=1, font = font0, background='#FFFFDE')
label005 = Label(root, text='', anchor = "sw" , width=40, height=1, font = font0, background='#FFFFDE')

label1 = Label(root, text='1. 체험자의 이름을 영어로 입력하세요.', anchor = "sw" , width=40, height=1, font = font1, background='#FFFFDE', padx = 100)

systemTitle = Label(root, text='스마트 도어 시스템', anchor = "center" , width=40, height=1, font = font3, background='#FFFFDE', fg='#2f3640')

label2 = Label(root, text='2. 스페이스 바로 사진을 촬영하세요.(종료 - ESC)', anchor = "sw" , width=40, height=1, font = font1, background='#FFFFDE', padx = 100)

label3 = Label(root, text='3. 사진 개수에 따라 학습 시간이 다릅니다.', anchor = "sw" , width=40, height=1, font = font1, background='#FFFFDE', padx = 100)

label4 = Label(root, text='4. 학습된 스마트 도어가 작동합니다.(종료 - ESC)', anchor = "sw" , width=40, height=1, font = font1, background='#FFFFDE', padx = 100)

label5 = Label(root, text='5. 체험을 종료하고, 사진을 삭제합니다.', anchor = "sw" , width=40, height=1, font = font1, background='#FFFFDE', padx = 100)

ci = Label(root, text='(주)한국공학기술연구원', anchor = "s" , width=40, height=2, font = font2, background='#FFFFDE')


    
      
label000.pack()
imgLabel1.pack()
systemTitle.pack()

label1.pack()

textExample = Entry(root, width=18, font = font2, background='azure', relief='solid')
textExample.pack()

label001.pack()

btn1.pack()


label002.pack()
label2.pack()
btn2.pack()

label003.pack()
label3.pack()
btn3.pack()

label004.pack()
label4.pack()
btn4.pack()

label005.pack()
label5.pack()
btn5.pack()

ci.pack()

root.mainloop()