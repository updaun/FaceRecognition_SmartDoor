from tkinter import *
import tkinter.font
from tkinter import messagebox


from dir_make import make
from face_shot import shot
from train_model import train
from face_lock import lock
from file_remove import remove


def test():
    if inputText.get().encode().isalpha():
        make(inputText.get())
    else:
        print("[오류] 체험자의 이름을 영어로 입력해주세요.")
        messagebox.showinfo("스마트 도어 시스템", "체험자의 이름을 영어로 입력해주세요.")
        inputText.delete(0, END)


projectTitle = '스마트 도어 시스템 v1.0'

bgcolor = '#9fd0f0'
btncolor = '#0d4d96'

root = Tk()
root.geometry("480x820+1050+0")
root.resizable(False, False)
# root.iconbitmap('face_recognition.ico')
root.iconphoto(False, PhotoImage(file='face_recognition.png'))
root.configure(bg=bgcolor)
root.title("스마트 도어 시스템")
#root.title("Smart Door System")

# 사용 색상


#font=tkinter.font.Font(family="돋움", size=20, slant="italic")

font = tkinter.font.Font(family="KoPubWorld돋움체 Medium",
                         size=15, weight=tkinter.font.BOLD)  # 버튼 폰트
font05 = tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=1)  # 공백 폰트
font25 = tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=25)  # 공백 폰트
font0 = tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=7)  # 공백 폰트
font1 = tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=11)  # 설명 폰트
font2 = tkinter.font.Font(family="KoPubWorld돋움체 Medium", size=18)  # TEXT 박스
font3 = tkinter.font.Font(family="KoPubWorld돋움체 Medium",
                          size=18, weight=tkinter.font.BOLD)  # Title 폰트

image1 = PhotoImage(file="face_recognition.png")
photoimage1 = image1.subsample(6, 6)
imgLabel1 = Label(root, image=photoimage1, width=85,
                  height=85, background=bgcolor)

image2 = PhotoImage(file="ci_logo.png")
photoimage2 = image2.subsample(3, 3)
imgLabel2 = Label(root, image=photoimage2, width=500,
                  height=100, background=bgcolor)

# btn1 = Button(root, text = "체험자 폴더 생성", width=25, height=1, font = font, foreground='white', background='#2f3640', command=lambda: make(inputText.get(1.0, END+"-1c")))
# btn1 = Button(root, text = "체험자 폴더 생성", width=20, height=1, font = font, foreground='white', background='#2f3640', command=lambda: make(inputText.get()))
btn1 = Button(root, text="체험자 이름 등록", width=20, height=1, font=font,
              foreground='white', background=btncolor, command=test)
btn2 = Button(root, text="체험자 사진 촬영", width=20, height=1, font=font,
              foreground='white', background=btncolor, command=lambda: shot(inputText.get()))
btn3 = Button(root, text="인공지능 학습", width=20, height=1, font=font,
              foreground='white', background=btncolor, command=lambda: train(inputText.get()))
btn4 = Button(root, text="스마트 도어 작동", width=20, height=1, font=font,
              foreground='white', background=btncolor, command=lambda: lock(inputText.get()))
btn5 = Button(root, text="체험자 사진 삭제", width=20, height=1, font=font,
              foreground='white', background=btncolor, command=remove)

label000 = Label(root, text='', anchor="sw", width=40,
                 height=1, font=font25, background=bgcolor)
label001 = Label(root, text='', anchor="sw", width=40,
                 height=1, font=font0, background=bgcolor)
label002 = Label(root, text='', anchor="sw", width=40,
                 height=1, font=font05, background=bgcolor)
label003 = Label(root, text='', anchor="sw", width=40,
                 height=1, font=font0, background=bgcolor)
label004 = Label(root, text='', anchor="sw", width=40,
                 height=1, font=font0, background=bgcolor)
label005 = Label(root, text='', anchor="sw", width=40,
                 height=1, font=font0, background=bgcolor)
label006 = Label(root, text='', anchor="sw", width=40,
                 height=1, font=font0, background=bgcolor)
label007 = Label(root, text='', anchor="sw", width=40,
                 height=1, font=font0, background=bgcolor)


# label1 = Label(root, text='Step 1. 체험자의 이름을 영어로 입력하세요.', anchor = "sw" , width=40, height=1, font = font1, background='#FFFFDE', padx = 100)

systemTitle = Label(root, text=projectTitle, anchor="center",
                    width=40, height=1, font=font3, background=bgcolor, fg='#2f3640')

# label2 = Label(root, text='Step 2. 인공지능 학습을 위한 사진을 촬영하세요.', anchor = "sw" , width=40, height=1, font = font1, background='#FFFFDE', padx = 100)
label2 = Label(root, text='Step 1. 체험자의 이름을 영어로 입력하세요.', anchor="sw",
               width=40, height=1, font=font1, background=bgcolor, padx=100)

label3 = Label(root, text='Step 2. 체험자의 사진을 학습시켜주세요.', anchor="sw",
               width=40, height=1, font=font1, background=bgcolor, padx=100)

label4 = Label(root, text='Step 3. 스마트 도어를 작동해주세요.', anchor="sw",
               width=40, height=1, font=font1, background=bgcolor, padx=100)

label5 = Label(root, text='Step 4. 다음 체험자를 위해 사진을 삭제해주세요.', anchor="sw",
               width=40, height=1, font=font1, background=bgcolor, padx=100)

ci = Label(root, text='(주)한국공학기술연구원', anchor="s", width=40,
           height=2, font=font2, background=bgcolor)

inputText = Entry(root, width=18, font=font2,
                  background='azure', relief='solid')


label000.pack()

imgLabel1.pack()

label001.pack()

systemTitle.pack()

label006.pack()

label2.pack()

inputText.pack()

label002.pack()

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

label007.pack()

#2021.05.25 logo
#imgLabel2.pack()

root.bind('<Return>', lambda event=None: btn2.invoke())
root.mainloop()
