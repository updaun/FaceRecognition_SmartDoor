import os
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
from tkinter import messagebox


def train(name):
    if name == '':
        print('[오류] 체험자의 이름을 입력해주세요.\n')
        messagebox.showwarning("스마트 도어 시스템", "체험자의 이름을 입력해주세요.")
    elif os.path.exists('./dataset/'+name) == False:
        print('[오류] 학습 시킬 데이터가 없습니다. 다시 사진을 촬영해주세요.\n')
        messagebox.showwarning(
            "스마트 도어 시스템", "학습 시킬 데이터가 없습니다.\n다시 사진을 촬영해주세요.")
    elif os.path.isfile('./dataset/'+name+'/user1.jpg') == False:
        print('[오류] 학습 시킬 데이터가 없습니다. 다시 사진을 촬영해주세요.\n')
        messagebox.showwarning(
            "스마트 도어 시스템", "학습 시킬 데이터가 없습니다.\n다시 사진을 촬영해주세요.")
    elif name.encode().isalpha():
        print(' '*75)
        print("[ 인공지능 학습을 시작합니다. ]\n")
        data_path = 'dataset/' + name + '/'
        # faces폴더에 있는 파일 리스트 얻기
        onlyfiles = [f for f in listdir(
            data_path) if isfile(join(data_path, f))]
        # 데이터와 매칭될 라벨 변수
        Training_Data, Labels = [], []
        # 파일 개수 만큼 루프
        for i, files in enumerate(onlyfiles):
            image_path = data_path + onlyfiles[i]
            # 이미지 불러오기
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            # 이미지 파일이 아니거나 못 읽어 왔다면 무시
            if images is None:
                continue
            # Training_Data 리스트에 이미지를 바이트 배열로 추가
            Training_Data.append(np.asarray(images, dtype=np.uint8))
            # Labels 리스트엔 카운트 번호 추가
            Labels.append(i)
            print("[상태] 인공지능 학습 진행중 {}%".format(i + 1))
            print(' '*75)

        # 훈련할 데이터가 없다면 종료.
        if len(Labels) == 0:
            #print("There is no data to train.")
            print("[오류] 학습 시킬 데이터가 없습니다. 다시 사진을 촬영해주세요.\n")
            messagebox.showwarning(
                "스마트 도어 시스템", "학습 시킬 데이터가 없습니다.\n다시 사진을 촬영해주세요.")
        # Labels를 32비트 정수로 변환
        Labels = np.asarray(Labels, dtype=np.int32)
        # 모델 생성
        model = cv2.face.LBPHFaceRecognizer_create()
        # 학습 시작
        model.train(np.asarray(Training_Data), np.asarray(Labels))
        print('='*75+'\n')
        #print("[Finish!] Training Done!")
        print("[ 인공지능 학습을 완료하였습니다. ]\n")
        print('='*75)
        messagebox.showinfo("스마트 도어 시스템", "인공지능 학습을 완료하였습니다.")

    else:
        print("[오류] 체험자의 이름을 영어로 입력해주세요.\n")
        messagebox.showwarning("스마트 도어 시스템", "체험자의 이름을 영어로 입력해주세요.")
