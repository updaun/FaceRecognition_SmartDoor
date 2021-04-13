import os
import cv2
import numpy as np
from tkinter import messagebox
from tkinter import font
from PIL import ImageFont, ImageDraw, Image

# 얼굴 인식용 xml 파일
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def shot(name):

    if name == '':
        print('[오류] 체험자의 이름을 입력해주세요.\n')
        messagebox.showwarning("스마트 도어 시스템", "체험자의 이름을 입력해주세요.")
    elif name.encode().isalpha():
        def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print('[오류] 폴더 생성을 실패하였습니다.\n' + directory)
                messagebox.showwarning("스마트 도어 시스템", "[오류] 폴더 생성을 실패하였습니다.")

        createFolder('./dataset/'+name)
        print("[ 카메라를 준비하고 있습니다. ]\n")
        print(
            '[알림] 지금부터 체험자의 얼굴을 100장 촬영합니다.\n[알림] 카메라를 응시해 주세요.\n[ 스페이스바 ] 를 누르면 촬영을 중단할 수 있습니다. \n')
        messagebox.showinfo(
            "스마트 도어 시스템", "[ 확인 ] 버튼을 누르면 사진 촬영을 시작합니다. \n \n카메라를 응시해야만 촬영을 진행합니다.")
        messagebox.showinfo("스마트 도어 시스템", "[ 스페이스바 ] 를 누르면 촬영을 중단할 수 있습니다.")
        # 전체 사진에서 얼굴 부위만 잘라 리턴

        def face_extractor(img):
            # 흑백처리
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 얼굴 찾기
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            # 찾은 얼굴이 없으면 None으로 리턴
            if faces is ():
                return None
            # 얼굴들이 있으면
            for(x, y, w, h) in faces:
                # 해당 얼굴 크기만큼 cropped_face에 잘라 넣기
                # 근데... 얼굴이 2개 이상 감지되면??
                # 가장 마지막의 얼굴만 남을 듯
                cropped_face = img[y:y+h, x:x+w]
            # cropped_face 리턴
            return cropped_face

        # 카메라 실행
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        # 저장할 이미지 카운트 변수
        count = 0
        noneface_count = 0

        b, g, r, a = 255, 255, 255, 0
        fontpath = "fonts/H2HDRM.TTF"
        font = ImageFont.truetype(fontpath, 30)

        while True:
            k = cv2.waitKey(1)
            # 카메라로 부터 사진 1장 얻기
            ret, frame = cap.read()
            # 얼굴 감지 하여 얼굴만 가져오기
            if face_extractor(frame) is not None:
                count += 1
                # 얼굴 이미지 크기를 200x200으로 조정
                face = cv2.resize(face_extractor(frame), (200, 200))
                face_show = cv2.resize(frame, (500, 500))
                face_show = cv2.flip(face_show, 1)
                cv2.rectangle(face_show, (50, 60),
                              (450, 85), (200, 200, 200), 3)
                cv2.rectangle(face_show, (50, 60), ((
                    50+int(count+1)*4), 85), (200, 200, 200), cv2.FILLED)

                # 조정된 이미지를 흑백으로 변환
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                #face_show = cv2.cvtColor(face_show, cv2.COLOR_BGR2HSV)
                # faces폴더에 jpg파일로 저장
                # ex > faces/user0.jpg   faces/user1.jpg ....
                file_name_path = './dataset/' + \
                    name + '/user' + str(count)+'.jpg'
                cv2.imwrite(file_name_path, face)

                # 화면에 얼굴과 현재 저장 개수 표시
                # cv2.putText(face_show,str(count)+'%',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(250,250,250),2)

                img_pil = Image.fromarray(face_show)
                draw = ImageDraw.Draw(img_pil)
                draw.text(
                    (50, 20),  '[ 진행 정도 : ' + str(count)+'% ]', font=font, fill=(b, g, r, a))
                img = np.array(img_pil)
                cv2.imshow('Press   SPACE   key to exit', img)
                cv2.moveWindow("Press   SPACE   key to exit", 545, 0)
            else:
                #print("Face not Found")
                face_none = cv2.resize(frame, (500, 500))
                face_none = cv2.cvtColor(face_none, cv2.COLOR_BGR2GRAY)
                face_none = cv2.flip(face_none, 1)
                cv2.rectangle(face_none, (50, 60),
                              (450, 85), (200, 200, 200), 3)
                cv2.rectangle(face_none, (50, 60), ((
                    50+int(count+1)*4), 85), (200, 200, 200), cv2.FILLED)
                #cv2.putText(face_none, "FACE Can't Find", (220, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
                img_pil_2 = Image.fromarray(face_none)
                draw_2 = ImageDraw.Draw(img_pil_2)
                draw_2.text(
                    (50, 20),  '[ 진행 정도 : ' + str(count)+'% ]', font=font, fill=255)
                #draw_2.text((140, 50),  '[ 여기 보세요! ]', font=font, fill=250)
                img_2 = np.array(img_pil_2)
                cv2.imshow('Press   SPACE   key to exit', img_2)
                cv2.moveWindow("Press   SPACE   key to exit", 545, 0)
                noneface_count = noneface_count+1
                if(noneface_count == 20):
                    print(' '*75)
                    print(' [주의] 얼굴을 찾지 못했습니다. 카메라를 정면으로 응시해주세요. ')
                    print(' '*75)
                    noneface_count = 0
                pass

            if k % 256 == 27 or k % 256 == 32 or count == 100:
                break

        cap.release()
        #print('Colleting Samples Complete!!!')
        print('체험자 [ ' + name + ' ] 의 모든 사진 촬영을 종료합니다.\n인공지능 학습을 시작해주세요.\n')
        messagebox.showinfo("스마트 도어 시스템", "사진 촬영 종료합니다. \n \n인공지능 학습을 시작해주세요.")

        cv2.destroyAllWindows()
    else:
        print("[오류] 체험자의 이름을 영어로 입력해주세요.\n")
        messagebox.showwarning("스마트 도어 시스템", "체험자의 이름을 영어로 입력해주세요.")
