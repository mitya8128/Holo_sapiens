
# coding: utf-8

import numpy as np
import cv2


def start_new_scanning():
    name = input()
    scanning(name)
    #play_video()
    #combineFaces(faces, w=100, h=100, numPerRow=5)
    #eigenVector = cv2.PCACompute(data, mean=None, maxComponents=10)
    #сохранить данные в csv_файл
    
def play_video():
    import numpy as np
    import cv2

    cap = cv2.VideoCapture('Holo Sapiens.mp4')

    while(cap.isOpened()):
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
   
    cap.release()
    cv2.destroyAllWindows()

def destroy_all():
    cap2.release()
    cv2.destroyAllWindows()


#функция, выделяющая лицо человека
def scanning(name):
    import cv2
    import sys

    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    cap2 = cv2.VideoCapture(0)
  
    while cap2.isOpened():
        
        ret, frame = cap2.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        flags=0
                        )

    # Нарисуем прямоугольник вокруг faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        #нужно собрать data matrix
        #mean, eigenVectors = cv2.PCACompute(data, mean=None, maxComponents=10)
        
        
        cv2.imshow('Video', frame)
        cv2.imwrite('%s.png' % name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap2.release()
    cv2.destroyAllWindows()



#собирает кадры матрицу данных
def combineFaces(faces, w=100, h=100, numPerRow=5):
    small_img = []
    row_img = []
    count = 0
    for img in faces:
        small_img.append(cv2.resize(img, (w, h)))
        count += 1
        if count % numPerRow == 0:
            count = 0
            row_img.append(np.concatenate(small_img, axis=1))
            small_img = []
    if len(small_img) > 0:
        for x in range (0, numPerRow-len(small_img)):
            small_img.append(np.zeros((h,w), np.uint8))
        row_img.append(np.concatenate(small_img, axis=1))
    
    data = np.concatenate(row_img, axis=0)
    return data

