import os
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
from PIL import ImageFont, ImageDraw, Image
from time import sleep

from library.et_board import et_board
import appconfig

from tkinter import messagebox


def lock(name):
    et = et_board(appconfig.et_board_ipaddress)
    if name == '':
        print('[오류] 체험자의 이름을 입력해주세요.\n')
        messagebox.showwarning("스마트 도어 시스템", "체험자의 이름을 입력해주세요.")

    elif os.path.exists('./dataset/'+name) == False:
        print('[오류] 학습 대상과 이름이 일치하지 않습니다. 다시 사진을 촬영해주세요.\n')
        messagebox.showwarning(
            "스마트 도어 시스템", "학습 대상과 이름이 일치하지 않습니다.\n \n다시 사진을 촬영해주세요.")

    elif os.path.isfile('./dataset/'+name+'/user1.jpg') == False:
        print('[오류] 학습 시킬 데이터가 없습니다. 다시 사진을 촬영해주세요.\n')
        messagebox.showwarning(
            "스마트 도어 시스템", "학습 시킬 데이터가 없습니다.\n다시 사진을 촬영해주세요.")

    elif name.encode().isalpha():

        b, g, r, a = 255, 255, 255, 0
        fontpath = "./fonts/H2HDRM.TTF"
        font = ImageFont.truetype(fontpath, 30)
        font2 = ImageFont.truetype(fontpath, 10)

        messagebox.showinfo(
            "스마트 도어 시스템", "'확인' 버튼을 누르면 체험을 시작합니다.\n \n체험 중 [ 스페이스바 ] 를 누르면 체험을 중단할 수 있습니다.")
        messagebox.showinfo("스마트 도어 시스템", "[ 엔터 ] 버튼을 누르면 문을 닫습니다.")
        data_path = 'dataset/' + name + '/'
        onlyfiles = [f for f in listdir(
            data_path) if isfile(join(data_path, f))]
        Training_Data, Labels = [], []
        for i, files in enumerate(onlyfiles):
            image_path = data_path + onlyfiles[i]
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if images is None:
                continue
            Training_Data.append(np.asarray(images, dtype=np.uint8))
            Labels.append(i)
        if len(Labels) == 0:
            print("There is no data to train.")
            exit()
        Labels = np.asarray(Labels, dtype=np.int32)
        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(np.asarray(Training_Data), np.asarray(Labels))
        print("[로그] 스마트 도어 작동을 준비하는 중입니다.\n")

        face_classifier = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')

        def face_detector(img, size=0.5):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            if faces is ():
                return img, []
            for(x, y, w, h) in faces:
                #cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
                #cv2.rectangle(img, (x-150,y-150),(x+150,y+150),(20,220,20),4)
                roi = img[y:y+h, x:x+w]
                roi = cv2.resize(roi, (250, 250))
            return img, roi  # 검출된 좌표에 사각 박스 그리고(img), 검출된 부위를 잘라(roi) 전달
            # return roi
        # 카메라 열기
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        lock_count = 0
        unlock_count = 0
        noface_count = 0

        while True:
            key = cv2.waitKey(1) & 0xFF
            # 카메라로 부터 사진 한장 읽기
            ret, frame = cap.read()
            # 얼굴 검출 시도
            image, face = face_detector(frame)
            #face = face_detector(frame)
            try:
                # 검출된 사진을 흑백으로 변환
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                # 위에서 학습한 모델로 예측시도
                result = model.predict(face)
                # result[1]은 신뢰도이고 0에 가까울수록 자신과 같다는 뜻이다.
                if result[1] < 500:
                    # ????? 어쨋든 0~100표시하려고 한듯
                    confidence = int(100*(1-(result[1])/300))
                    # 유사도 화면에 표시
                    #display_string = str(confidence)+'% ' + name
                #cv2.putText(image,display_string,(50,50), cv2.FONT_HERSHEY_DUPLEX,1,(20,20,20),2)
                # 85 보다 크면 동일 인물로 간주해 UnLocked!
                if confidence > 87:

                    display_string = '[ 출입 허용 ]   ' + \
                        name + '   ' + str(confidence)+'%'
                    image = cv2.resize(image, (500, 500))
                    image = cv2.flip(image, 1)
                    cv2.rectangle(image, (75, 75),
                                  (75+350, 75+350), (0, 255, 0), 2)
                    img_pil = Image.fromarray(image)
                    draw = ImageDraw.Draw(img_pil)
                    #draw.text((25, 50), display_string, font=font, fill=(0,255,50,0))
                    #draw.text((25, 420),  '[ 스마트 도어가 열립니다. ]', font=font, fill=(0,255,50,0))
                    img = np.array(img_pil)

                    #cv2.putText(image,display_string,(25,50), cv2.FONT_HERSHEY_DUPLEX,1,(40,200,40),2)
                    #cv2.putText(image, "Door OPEN", (25, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow(
                        'Smart Door System, Press  SPACE  key to exit', img)
                    cv2.moveWindow(
                        "Smart Door System, Press  SPACE  key to exit", 545, 0)
                    unlock_count = unlock_count + 1
                    if unlock_count == 50:
                        et.run_servo(120)
                        et.run_digital(2, 1)
                        et.run_digital(3, 1)
                        print(' '*75)
                        print('[ 체험자 얼굴 인증 성공! ]\n')
                        lock_count = 0
                        unlock_count = 0
                        noface_count = 0

                else:
                    # 85 이하면 타인.. Locked!!!
                    display_string = '[ 출입 불가 ]'
                    image = cv2.resize(image, (500, 500))
                    image = cv2.flip(image, 1)
                    cv2.rectangle(image, (75, 75),
                                  (75+350, 75+350), (0, 0, 255), 2)
                    img_pil = Image.fromarray(image)
                    draw = ImageDraw.Draw(img_pil)
                    #draw.text((25, 50), display_string, font=font, fill=(0,0,204,0))
                    #draw.text((25, 420),  '[ 스마트 도어가 닫힙니다. ]', font=font, fill=(0,0,204,0))
                    img = np.array(img_pil)

                    #cv2.putText(image,display_string,(25,50), cv2.FONT_HERSHEY_DUPLEX,1,(40,40,200),2)
                    #cv2.putText(image, "Security System ON", (300, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow(
                        'Smart Door System, Press  SPACE  key to exit', img)
                    cv2.moveWindow(
                        "Smart Door System, Press  SPACE  key to exit", 545, 0)

                    lock_count = lock_count + 1
                    # print(lock_count)
                    if lock_count == 60:
                        # et.run_servo(40)
                        # et.run_digital(2,0)
                        # et.run_digital(3,0)
                        print(' '*75)
                        print('[ 체험자 미감지 ! ]\n')
                        lock_count = 0
                        unlock_count = 0
                        noface_count = 0

            except:
                # 얼굴 검출 안됨
                #cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                display_string = '[ 감지 실패 ]'

                image = cv2.resize(image, (500, 500))
                image = cv2.flip(image, 1)
                #cv2.rectangle(image, (100,100),(100+300,100+300),(255,255,255),3)
                cv2.rectangle(image, (75, 75), (75+350, 75+350),
                              (255, 255, 255), 2)

                #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                img_pil = Image.fromarray(image)
                draw = ImageDraw.Draw(img_pil)
                #draw.text((25, 50), display_string, font=font, fill=(255,50,50,0))
                #draw.text((50, 140),  '[ 얼굴이 감지되지 않습니다. ]', font=font, fill=(255,50,0,0))
                img = np.array(img_pil)
                #cv2.putText(image, "FACE Can't Find", (200, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

                cv2.imshow('Smart Door System, Press  SPACE  key to exit', img)
                cv2.moveWindow(
                    "Smart Door System, Press  SPACE  key to exit", 545, 0)

                noface_count = noface_count + 1
                if noface_count == 60:
                    # et.run_servo(40)
                    # et.run_digital(2,0)
                    # et.run_digital(3,0)
                    print(' '*75)
                    print('[ 체험자 미감지 ! ]\n')
                    lock_count = 0
                    noface_count = 0
                pass
            if key == 13:
                et.run_servo(40)
                et.run_digital(2, 0)
                et.run_digital(3, 0)

            if key == 27 or key == 32:
                print(' '*75)
                print('스마트 도어 시스템을 종료합니다.\n')
                print('다음 체험자를 위해 체험자 이미지를 삭제해주세요.\n')
                messagebox.showinfo(
                    "스마트 도어 시스템", "스마트 도어 시스템을 종료합니다.\n \n다음 체험자를 위해 체험자 이미지를 삭제해주세요.")
                et.run_servo(40)
                et.run_digital(2, 0)
                et.run_digital(3, 0)
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("[오류] 체험자의 이름을 영어로 입력해주세요.\n")
        messagebox.showwarning("스마트 도어 시스템", "체험자의 이름을 영어로 입력해주세요.")
