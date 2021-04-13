import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

from library.et_board import et_board
import appconfig

from tkinter import messagebox


def lock(name):
    et = et_board(appconfig.et_board_ipaddress)
    if name == '':
        print('[오류] 체험자의 이름을 입력해주세요.')
        messagebox.showinfo("스마트 도어 시스템", "체험자의 이름을 입력해주세요.")
    elif name.encode().isalpha():
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
        print("[로그] 스마트 도어 작동을 준비하는 중입니다.")

        face_classifier = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')

        def face_detector(img, size=0.5):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            if faces is ():
                return img, []
            for(x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
                roi = img[y:y+h, x:x+w]
                roi = cv2.resize(roi, (200, 200))
            return img, roi  # 검출된 좌표에 사각 박스 그리고(img), 검출된 부위를 잘라(roi) 전달

        # 카메라 열기
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        lock_count = 0
        unlock_count = 0

        while True:
            key = cv2.waitKey(1) & 0xFF
            # 카메라로 부터 사진 한장 읽기
            ret, frame = cap.read()
            # 얼굴 검출 시도
            image, face = face_detector(frame)
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
                if confidence > 83:
                    display_string = name + ' ' + \
                        str(confidence)+' % = Allow Access'
                    cv2.putText(image, display_string, (25, 50),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (40, 200, 40), 2)
                    cv2.putText(image, "Door OPEN", (25, 450),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow(
                        'Smart Door System, Press  ESC  key to exit', image)
                    cv2.moveWindow(
                        "Smart Door System, Press  ESC  key to exit", 370, 0)
                    #print('-'*15 + ' 3초를 유지하면, 스마트 도어가 열립니다.  ' + '-'*15)
                    unlock_count = unlock_count + 1
                    # print(unlock_count)
                    if(unlock_count == 20):
                        # et.run_servo(120)
                        print('='*75)
                        print('[ OPEN ! ] 스마트 도어가 열립니다. ' + '-'*40)
                        print('='*75)
                        unlock_count = 0

                else:
                    # 85 이하면 타인.. Locked!!!
                    display_string = '  Access Denied !! '
                    cv2.putText(image, display_string, (25, 50),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (40, 40, 200), 2)
                    cv2.putText(image, "Security System ON", (300, 450),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow(
                        'Smart Door System, Press  ESC  key to exit', image)
                    cv2.moveWindow(
                        "Smart Door System, Press  ESC  key to exit", 370, 0)

                    lock_count = lock_count + 1
                    # print(lock_count)
                    if(lock_count == 50):
                        # et.run_servo(40)
                        print('='*75)
                        print('[ CLOSE ! ] 스마트 도어 보안을 가동합니다. ' + '-'*30)
                        print('='*75)
                        lock_count = 0
            except:
                # 얼굴 검출 안됨
                #cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                cv2.putText(image, "FACE Can't Find", (200, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
                cv2.imshow('Smart Door System, Press  ESC  key to exit', image)
                cv2.moveWindow(
                    "Smart Door System, Press  ESC  key to exit", 370, 0)
                pass
            if key == 27 or key == 13:
                print('='*75)
                print('-'*15 + '  스마트 도어 시스템을 종료합니다. ' + '-'*15)
                messagebox.showinfo(
                    "스마트 도어 시스템", "스마트 도어 시스템을 종료합니다.\n다음 체험자를 위해 체험자 이미지를 삭제해주세요.")
                print('-'*75)
                print('-'*15 + '  다음 체험자를 위해 체험자 이미지를 삭제해주세요.  ' + '-'*15)
                print('='*75)
                # et.run_servo(40)
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("[오류] 체험자의 이름을 영어로 입력해주세요.")
        messagebox.showinfo("스마트 도어 시스템", "체험자의 이름을 영어로 입력해주세요.")
